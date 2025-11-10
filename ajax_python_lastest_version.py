
# -*- coding: UTF-8 -*-
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_file
# from flask_cors import CORS
from pymongo import MongoClient
from urllib import quote_plus
from bson.objectid import ObjectId
from bson import ObjectId
from bson import json_util
import pandas as pd
import os 
import csv
import io
import logging
from manage import app


app.config['GWAS_png'] = {
    'Breast': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/1.breast.all',
    'Prostate': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/2.prostate.all',
    'Melanoma': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/3.cutaneousMelanoma.all',
    'Colon': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/4.colon.all',
    'Cervical': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/5.cervical.all',
    'Lung': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/6.bronchialAndLung.all',
    'Bladder': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/7.bladder.all',
    'Rectal': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/8.rectal.all',
    'Uterine': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/9.uterine.all',
    'Kidney': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/10.kidney.all',
    'Ovarian': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/11.ovarian.all',
    'Pancreatic': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/12.pancreatic.all',
    'Esophagus': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/13.esophagus.all',
    'Stomach': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/14.stomach.all',
    'Brain': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/15.brain.all',
    'Liver': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/16.liverAndIntrahepaticBileDucts.all'   
}
app.config['GWAS_pdf'] = {
    'Breast': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/1.breast.all',
    'Prostate': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/2.prostate.all',
    'Melanoma': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/3.cutaneousMelanoma.all',
    'Colon': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/4.colon.all',
    'Cervical': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/5.cervical.all',
    'Lung': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/6.bronchialAndLung.all',
    'Bladder': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/7.bladder.all',
    'Rectal': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/8.rectal.all',
    'Uterine': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/9.uterine.all',
    'Kidney': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/10.kidney.all',
    'Ovarian': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/11.ovarian.all',
    'Pancreatic': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/12.pancreatic.all',
    'Esophagus': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/13.esophagus.all',
    'Stomach': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/14.stomach.all',
    'Brain': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/15.brain.all',
    'Liver': '/home/wuxh/SSIdb3/EpiSNP-db/src/assets/01.GWAS.plot/16.liverAndIntrahepaticBileDucts.all'  
}
# CORS(app)  # Enable CORS

username = quote_plus('wuxh')
password = quote_plus('GlKj5t3NToQIevggauyt')
mongo_uri = 'mongodb://{}:{}@localhost:30000/wuxh_database'.format(username, password)
client = MongoClient(mongo_uri)

db = client['wuxh_database']
# collection_GWASres = db['GWASres']

collection_GWASres = db['epiSNPGWASres']

collection_SnpEpistasisRes = db['SnpEpistasisRes']
collection_GWAS_Annovar = db['SnpGwasAnnovar']
collection_Epistasis_Annovar = db['SnpEpistasisAnnovar']

collection_SingleAdditiveSurvival = db['SingleAdditiveSurvival']
collection_SingleRecessiveSurvival = db['SingleRecessiveSurvival']
collection_SingleDominantSurvival = db['SingleDominantSurvival']

collection_TwoDominantSurvival = db['TwoDominantSurvival']
collection_TwoAdditiveSurvival = db['TwoAdditiveSurvival']
collection_TwoRecessiveSurvival = db['TwoRecessiveSurvival']

collection_mutation=db['MutationRes']

@app.route('/api/quickSearchSnp', methods=['GET'])
def quick_search_snp():
    query_id = request.args.get('queryID')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 8))
    skip = (page - 1) * per_page

    # 查询GWAS数据
    query = {"SNP": {"$regex": query_id, "$options": "i"}} if query_id else {}
    results = list(collection_GWASres.find(query).skip(skip).limit(per_page))
    total_count = collection_GWASres.count_documents(query)
    for result in results:
        if '_id' in result:
            result['_id'] = str(result['_id'])

    # 查询SNP Epistasis数据
    epi_query = {"$or": [{"SNP1": query_id}, {"SNP2": query_id}]} if query_id else {}
    epi_results = list(collection_SnpEpistasisRes.find(epi_query))
    epi_table_results = []
    epi_network_results = []
    
    for epi_result in epi_results:
        if '_id' in epi_result:
            epi_result['_id'] = str(epi_result['_id'])
        epi_table_results.append({
            "Cancertype": epi_result.get("Cancertype"),
            "SNPepi": epi_result.get("SNPepi"),
            "Chr1": epi_result.get("Chr1"),
            "pos1": epi_result.get("pos1"),
            "Chr2": epi_result.get("Chr2"),
            "pos2": epi_result.get("pos2"),
            "OR": epi_result.get("OR_INT"),
            "STAT": epi_result.get("STAT"),
            "P": epi_result.get("P"),
            "Best_snp": epi_result.get("Best_snp"),
            "saige_p": epi_result.get("saige_p"),
            "sample": epi_result.get("sample")
        })
        epi_network_results.append({
            "SNPepi": epi_result.get("SNPepi")
        })

    return jsonify({
        "SNPGWAS": results,
        "SNPEpiTable": epi_table_results,
        "SNPEpiNetwork": epi_network_results,
        "recordsNumber": total_count
    })

@app.route('/api/getPdf', methods=['GET'])
def get_pdf():
    cancertype = request.args.get('Cancertype')
    snp = request.args.get('SNP')
    if cancertype in app.config['GWAS_png']:
        image_file_name = '{}_{}.png'.format(cancertype, snp)
        image_file_path = os.path.join(app.config['GWAS_png'][cancertype], image_file_name)

        # 文件存在性验证
        if os.path.exists(image_file_path):
            return send_file(image_file_path, mimetype='image/png')  
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400


@app.route('/api/downloadPdf', methods=['GET'])
def download_pdf():
    cancertype = request.args.get('Cancertype')
    snp = request.args.get('SNP')
    if not cancertype or not snp:
        return jsonify({"error": "Missing required parameters"}), 400
    if cancertype in app.config['GWAS_pdf']:
        pdf_file_name = "{}_{}.pdf".format(cancertype, snp)
        pdf_file_path = os.path.join(app.config['GWAS_pdf'][cancertype], pdf_file_name)
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400


@app.route('/api/snpGWASdownloadCSV', methods=['GET'])
def snpGWAS_download_csv():
    query_id = request.args.get('queryID')
    query = {"SNP": {"$regex": query_id, "$options": "i"}} if query_id else {}
    results = list(collection_GWASres.find(query))
    if not results:
        return jsonify({"error": "No data found"}), 404
    
    si = io.StringIO()
    cw = csv.writer(si)
    # 写入CSV头部
    cw.writerow(['Cancertype', 'SNP', 'Position', 'Alleles(A/a)', 'MAF', 'A1', 'A2', 'AF1', 'Beta', 'P_value', 'Sample'])
    for result in results:
        position = "{}:{}".format(result['Pos'], result['POS'])
        cw.writerow([result['Cancertype'], result['SNP'], position, 
                     result['Alleles'], result['MAF'], result['A1'], 
                     result['A2'], result['AF1'], result['BETA'], 
                     result['P'], result['N']])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename={}_GWAS_res.csv".format(query_id)
    output.headers["Content-type"] = "text/csv"
    return output


# 通过染色体的位置区间进行搜索。
@app.route('/api/quickSearchPosition', methods=['GET'])
def search_chromosome_range():
    try:
        chromosome = request.args.get('chromosome')
        start = int(request.args.get('start'))
        end = int(request.args.get('end'))
        if not all([chromosome, start, end]):
            return jsonify({"error": "Missing required parameters"}), 400
        
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('perPage', 8))
        skip = (page - 1) * per_page

        # 查询GWAS数据
        query = {
            "Pos": chromosome,
            "POS": {"$gte": start, "$lte": end}
        }
        results = list(collection_GWASres.find(query).sort([("P",1)]).skip(skip).limit(per_page))
        total_count = collection_GWASres.count_documents(query)
        for result in results:
            if '_id' in result:
                result['_id'] = str(result['_id'])

        # 查询SNP Epistasis数据
        epi_query = {
            "$or": [
                {"Chr1": chromosome, "pos1": {"$gte": start, "$lte": end}},
                {"Chr2": chromosome, "pos2": {"$gte": start, "$lte": end}}
            ]
        }
        epi_results = list(collection_SnpEpistasisRes.find(epi_query).sort([("ORstatus",-1),("P",1)]).skip(skip).limit(per_page))
        total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)
        epi_table_results = []
        epi_network_results = []

        for epi_result in epi_results:
            if '_id' in epi_result:
                epi_result['_id'] = str(epi_result['_id'])
            epi_table_results.append({
                "Cancertype": epi_result.get("Cancertype"),
                "SNPepi": epi_result.get("SNP_epi"),
                "Chr1": epi_result.get("Chr1"),
                "pos1": epi_result.get("pos1"),
                "Chr2": epi_result.get("Chr2"),
                "pos2": epi_result.get("pos2"),
                "OR": epi_result.get("OR_INT"),
                "STAT": epi_result.get("STAT"),
                "P": epi_result.get("P"),
                "Best_snp": epi_result.get("Best_snp"),
                "saige_p": epi_result.get("saige_p"),
                "sample": epi_result.get("sample")
            })
            epi_network_results.append({
                "SNPepi": epi_result.get("SNP_epi"),
                "pos1": epi_result.get("pos1"),
                "pos2": epi_result.get("pos2")
            })

        return jsonify({
            "SNPGWASPosition": results,
            "SNPEpiTable": epi_table_results,
            "SNPEpiNetwork": epi_network_results,
            "recordsNumber": total_count,
            "epiRecordsNumber": total_epi_count
        })
    except ValueError:
        return jsonify({"error": "Invalid parameters"}), 400





@app.route('/api/downloadCurrentPageGWASPosition', methods=['POST'])
def download_current_page_gwas():
    data = request.json.get('data')  # 接收前端发送的当前页数据
    chromosome = request.json.get('chromosome')
    start = request.json.get('start')
    end = request.json.get('end')
    currentPage = request.json.get('currentPage')
    if not data:
        return jsonify({"error": "No data provided"}), 400
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Cancertype', 'SNP', 'Position', 'Alleles(A/a)', 'MAF', 'A1', 'A2', 'AF1', 'Beta', 'P_value', 'Sample'])
    for item in data:
        position = "{}:{}".format(item['Pos'], item['POS'])  # 合并Pos和POS为Position
        cw.writerow([item['Cancertype'], item['SNP'], position, 
                     item['Alleles'], item['MAF'], item['A1'], 
                     item['A2'], item['AF1'], item['BETA'], 
                     item['P'], item['N']])
    filename = "{}_{}-{}_Page_{}_GWAS.csv".format(chromosome, start, end, currentPage)
    output = Response(si.getvalue(), mimetype="text/csv")
    output.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    return output


@app.route('/api/quickSearchCancer', methods=['GET'])
def quick_search_cancer():
    cancertype = request.args.get('cancertype')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 8))
    skip = (page - 1) * per_page

    gwas_query = {"Cancertype": {"$regex": cancertype, "$options": "i"}} if cancertype else {}
    epi_query = gwas_query

    gwas_results = list(collection_GWASres.find(gwas_query).sort([("P",1)]).skip(skip).limit(per_page))
    total_gwas_count = collection_GWASres.count_documents(gwas_query)

    epi_results = list(collection_SnpEpistasisRes.find(epi_query).sort([("ORstatus",-1),("P",1)]).skip(skip).limit(per_page))
    total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)

    for result in gwas_results + epi_results:
        if '_id' in result:
            result['_id'] = str(result['_id'])

    epi_table_results = [{
        "Cancertype": epi_result.get("Cancertype"),
        "SNPepi": epi_result.get("SNP_epi"),
        "Chr1": epi_result.get("Chr1"),
        "pos1": epi_result.get("pos1"),
        "Chr2": epi_result.get("Chr2"),
        "pos2": epi_result.get("pos2"),
        "OR": epi_result.get("OR_INT"),
        "ORstatus": epi_result.get("ORstatus"),
        "P": epi_result.get("P"),
        "Best_snp": epi_result.get("Best_snp"),
        "saige_p": epi_result.get("saige_p"),
        "STAT": epi_result.get("STAT"),
        "sample": epi_result.get("sample")
    } for epi_result in epi_results]

    epi_network_results = [{
        "SNPepi": epi_result.get("SNP_epi"),
        "pos1": epi_result.get("pos1"),
        "pos2": epi_result.get("pos2")
    } for epi_result in epi_results]

    return jsonify({
        "CancerGWAS": gwas_results,
        "SNPEpiTable": epi_table_results,
        "SNPEpiNetwork": epi_network_results,
        "recordsNumber": total_gwas_count,
        "epiRecordsNumber": total_epi_count
    })

@app.route('/api/QuickCancerinteresting', methods=['GET'])
def quick_cancer_interesting():
    cancertype = request.args.get('cancertype')
    epistasis = request.args.get('queryRsid1')
    
    # 分割epistasis参数
    epistasis_parts = epistasis.split('_') if '_' in epistasis else [epistasis]

    # 查询SnpEpistasisRes集合
    epi_query = {
        "Cancertype": cancertype,
        "$or": [
            {"SNP1": {"$in": epistasis_parts}},
            {"SNP2": {"$in": epistasis_parts}}
        ]
    }
    epi_results = list(collection_SnpEpistasisRes.find(epi_query))
    total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)

    # 查询GWASres集合
    gwas_query = {
        "Cancertype": cancertype,
        "SNP": {"$in": epistasis_parts}
    }
    gwas_results = list(collection_GWASres.find(gwas_query))
    total_gwas_count = collection_GWASres.count_documents(gwas_query)

    for result in gwas_results + epi_results:
        if '_id' in result:
            result['_id'] = str(result['_id'])

    epi_table_results = [{
        "Cancertype": epi_result.get("Cancertype"),
        "SNPepi": epi_result.get("SNP_epi"),
        "Chr1": epi_result.get("Chr1"),
        "pos1": epi_result.get("pos1"),
        "Chr2": epi_result.get("Chr2"),
        "pos2": epi_result.get("pos2"),
        "OR": epi_result.get("OR_INT"),
        "ORstatus": epi_result.get("ORstatus"),
        "P": epi_result.get("P"),
        "Best_snp": epi_result.get("Best_snp"),
        "saige_p": epi_result.get("saige_p"),
        "STAT": epi_result.get("STAT"),
        "sample": epi_result.get("sample")
    } for epi_result in epi_results]

    epi_network_results = [{
        "SNPepi": epi_result.get("SNP_epi"),
        "pos1": epi_result.get("pos1"),
        "pos2": epi_result.get("pos2")
    } for epi_result in epi_results]

    return jsonify({
        "CancerGWAS": gwas_results,
        "SNPEpiTable": epi_table_results,
        "SNPEpiNetwork": epi_network_results,
        "recordsNumber": total_gwas_count,
        "epiRecordsNumber": total_epi_count
    })


@app.route('/api/quickSearchSnpEpistasis', methods=['GET'])
def quick_search_snp_epistasis():
    try:
        query_id = request.args.get('queryID')

        if not query_id:
            return jsonify({"error": "Missing queryID parameter"}), 400

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('perPage', 8))
        skip = (page - 1) * per_page

        yi, er = query_id.split('_')

        # 查询SNP Epistasis数据
        epi_query = {
            "$or": [
                {"SNP1": yi, "SNP2": er},
                {"SNP1": er, "SNP2": yi}
            ]
        }
        epi_results = list(collection_SnpEpistasisRes.find(epi_query).skip(skip).limit(per_page))
        total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)
        
        epi_table_results = []
        epi_network_results = []

        for epi_result in epi_results:
            if '_id' in epi_result:
                epi_result['_id'] = str(epi_result['_id'])
            epi_table_results.append({
                "Cancertype": epi_result.get("Cancertype"),
                "SNPepi": epi_result.get("SNP_epi"),
                "Chr1": epi_result.get("Chr1"),
                "pos1": epi_result.get("pos1"),
                "Chr2": epi_result.get("Chr2"),
                "pos2": epi_result.get("pos2"),
                "OR": epi_result.get("OR_INT"),
                "STAT": epi_result.get("STAT"),
                "P": epi_result.get("P"),
                "Best_snp": epi_result.get("Best_snp"),
                "saige_p": epi_result.get("saige_p"),
                "sample": epi_result.get("sample")
            })
            epi_network_results.append({
                "SNPepi": epi_result.get("SNP_epi"),
                "pos1": epi_result.get("pos1"),
                "pos2": epi_result.get("pos2")
            })


        # 查询GWAS数据
        gwas_query = {
            "SNP": {"$in": [yi, er]}
        }
        gwas_results = list(collection_GWASres.find(gwas_query).skip(skip).limit(per_page))
        gwas_total_count = collection_GWASres.count_documents(gwas_query)

        for result in gwas_results:
            if '_id' in result:
                result['_id'] = str(result['_id'])  # Converting ObjectId to string for JSON serialization

        return jsonify({
            "SNPGWASPosition": gwas_results,
            "SNPEpiTable": epi_table_results,
            "SNPEpiNetwork": epi_network_results,
            "recordsNumber": gwas_total_count,
            "epiRecordsNumber": total_epi_count  # 新增返回总数
        })
    except ValueError:
        return jsonify({"error": "Invalid parameters"}), 400



def convert_objectid_to_str(doc):
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

# @app.route('/api/SnpGwasSearchThreeWay', methods=['POST'])
# def search():
#     data = request.json
#     search_type = data.get('queryType')
#     page = int(data.get('page', 1))
#     perPage = int(data.get('pageSize', 8))
#     p_value_threshold = float(data.get('pValue', 0.05))
#     cancer_type = data.get('cancerType', 'All')
#     chromosome_range = data.get('chromosomeRange')
#     snp_id = data.get('snp')
#     offset = (page - 1) * perPage
#     SnpGwasSearchThreeWayResult = {
#         'results': [],
#         'total': 0
#     }
#     query = {'P': {'$lte': p_value_threshold}}

#     if search_type == 'SNP':
#         if snp_id is None:
#             return jsonify({'error': 'Missing SNP ID'}), 400
#         query['SNP'] = snp_id
#         if cancer_type != 'All':
#             query['Cancertype'] = cancer_type
#     elif search_type == 'Chromosome Range':
#         if chromosome_range is None:
#             return jsonify({'error': 'Missing chromosome range'}), 400
#         chr, positions = chromosome_range.split(':')
#         start, end = map(int, positions.split('-'))
#         query['Pos'] = chr
#         query['POS'] = {'$gte': start, '$lte': end}
#         if cancer_type != 'All':
#             query['Cancertype'] = cancer_type
#     elif search_type == 'CancerType':
#         if cancer_type is None:
#             return jsonify({'error': 'Missing cancer type'}), 400
#         if cancer_type != 'All':
#             query['Cancertype'] = cancer_type
#     else:
#         return jsonify({'error': 'Invalid search type'}), 400

#     total = collection_GWASres.count_documents(query)
#     results = list(collection_GWASres.find(query).sort([("P",1)]).skip(offset).limit(perPage))
#     results = [convert_objectid_to_str(doc) for doc in results]
#     SnpGwasSearchThreeWayResult = {
#         'results': results,
#         'total': total
#     }
#     return jsonify(SnpGwasSearchThreeWayResult)


# @app.route('/api/SnpGwasSearchThreeWay', methods=['POST'])
# def search():
#     data = request.json

#     if 'Type' in data:
#         query = {'Type': True}
#         total = collection_GWASres.count_documents(query)
#         results = list(collection_GWASres.find(query).sort([("P", 1)]))
#         results = [convert_objectid_to_str(doc) for doc in results]
#         SnpGwasSearchThreeWayResult = {
#             'results': results,
#             'total': total
#         }
#         return jsonify(SnpGwasSearchThreeWayResult)

#     search_type = data.get('queryType', "SNP")
#     page = int(data.get('page', 1))
#     perPage = int(data.get('perPage', 8))
#     p_value_threshold = float(data.get('pValue', 0.05))
#     cancer_type = data.get('cancerType', 'All')
#     chromosome_range = data.get('chromosomeRange')
#     snp_id = data.get('snp')
#     offset = (page - 1) * perPage
#     SnpGwasSearchThreeWayResult = {
#         'results': [],
#         'total': 0
#     }
#     query = {'P': {'$lte': p_value_threshold}}

#     if search_type == 'SNP':
#         if not snp_id:
#             return jsonify({'error': 'Missing SNP ID'}), 400
#         query['SNP'] = snp_id
#         if cancer_type != 'All':
#             query['Cancertype'] = cancer_type
#     elif search_type == 'Chromosome range':
#         if not chromosome_range:
#             return jsonify({'error': 'Missing chromosome range'}), 400
#         try:
#             chr, positions = chromosome_range.split(':')
#             start, end = map(int, positions.split('-'))
#             query['Pos'] = chr
#             query['POS'] = {'$gte': start, '$lte': end}
#         except ValueError:
#             return jsonify({'error': 'Invalid chromosome range format'}), 400
#         if cancer_type != 'All':
#             query['Cancertype'] = cancer_type
#     elif search_type == 'Cancer Type':
#         if not cancer_type:
#             return jsonify({'error': 'Missing cancer type'}), 400
#         if cancer_type != 'All':
#             query['Cancertype'] = cancer_type
#     else:
#         return jsonify({'error': 'Invalid search type'}), 400

#     total = collection_GWASres.count_documents(query)
#     results = list(collection_GWASres.find(query).sort([("P", 1)]).skip(offset).limit(perPage))
#     results = [convert_objectid_to_str(doc) for doc in results]
#     SnpGwasSearchThreeWayResult = {
#         'results': results,
#         'total': total
#     }
#     return jsonify(SnpGwasSearchThreeWayResult)


def convert_objectid_to_str(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@app.route('/api/SnpGwasSearchThreeWay', methods=['POST'])
def search():
    data = request.json

    if 'Type' in data:
        query = {'Type': True}
        total = collection_GWASres.count_documents(query)
        results = list(collection_GWASres.find(query).sort([("P", 1)]))
        results = [convert_objectid_to_str(doc) for doc in results]
        SnpGwasSearchThreeWayResult = {
            'results': results,
            'total': total
        }
        return jsonify(SnpGwasSearchThreeWayResult)

    search_type = data.get('queryType', "SNP")
    page = int(data.get('page', 1))
    perPage = int(data.get('perPage', 8))
    p_value_threshold = float(data.get('pValue', 0.05))
    cancer_type = data.get('cancerType', 'All')
    chromosome_range = data.get('chromosomeRange')
    snp_id = data.get('snp')
    offset = (page - 1) * perPage
    SnpGwasSearchThreeWayResult = {
        'results': [],
        'total': 0
    }
    query = {'P': {'$lte': p_value_threshold}}

    if search_type == 'SNP':
        if not snp_id:
            return jsonify({'error': 'Missing SNP ID'}), 400
        query['SNP'] = snp_id
        if cancer_type != 'All':
            query['Cancertype'] = cancer_type
    elif search_type == 'Chromosome range':
        if not chromosome_range:
            return jsonify({'error': 'Missing chromosome range'}), 400
        try:
            chr, positions = chromosome_range.split(':')
            start, end = map(int, positions.split('-'))
            query['Pos'] = chr
            query['POS'] = {'$gte': start, '$lte': end}
        except ValueError:
            return jsonify({'error': 'Invalid chromosome range format'}), 400
        if cancer_type != 'All':
            query['Cancertype'] = cancer_type
    elif search_type == 'Cancer type':
        if not cancer_type:
            return jsonify({'error': 'Missing cancer type'}), 400
        if cancer_type != 'All':
            query['Cancertype'] = cancer_type
    else:
        return jsonify({'error': 'Invalid search type'}), 400

    total = collection_GWASres.count_documents(query)
    results = list(collection_GWASres.find(query).sort([("P", 1)]).skip(offset).limit(perPage))
    results = [convert_objectid_to_str(doc) for doc in results]
    SnpGwasSearchThreeWayResult = {
        'results': results,
        'total': total
    }
    return jsonify(SnpGwasSearchThreeWayResult)




# @app.route('/api/SnpEpistasis', methods=['GET'])
# def get_snp_epistasis():
#     select_cancer_type = request.args.get('selectCancerType', 'All')  # Default to 'All' if not provided
#     p_value_threshold = float(request.args.get('pValueThreshold', '0.05'))
#     query_rsid1 = request.args.get('queryRsid1', '').strip()
#     select_query_type = request.args.get('selectQueryType', 'SNP')
#     current_page = int(request.args.get('currentPage', '1'))  # 当前页码
#     per_page = int(request.args.get('perPage', '8'))  # 每页展示的记录数

#     query = {
#         'P': {'$lt': p_value_threshold}
#     }
#     if select_cancer_type != 'All':
#         query['Cancertype'] = select_cancer_type
#     if select_query_type == 'SNP' or select_query_type == 'SNP Epistasis':
#         if query_rsid1:
#             if '_' in query_rsid1:
#                 snp1, snp2 = query_rsid1.split('_')
#                 query['$or'] = [
#                     {'SNP1': snp1, 'SNP2': snp2},
#                     {'SNP1': snp2, 'SNP2': snp1}
#                 ]
#             else:
#                 query['$or'] = [
#                     {'SNP1': query_rsid1},
#                     {'SNP2': query_rsid1}
#                 ]
#     total_count = collection_SnpEpistasisRes.count_documents(query)
#     skip_records = (current_page - 1) * per_page
#     results = list(collection_SnpEpistasisRes.find(query).sort([("ORstatus",-1),("P",1)]).skip(skip_records).limit(per_page))

#     # Convert ObjectId to string
#     for result in results:
#         if '_id' in result:
#             result['_id'] = str(result['_id'])
#         # Ensure IsSPA is boolean
#         if 'IsSPA' in result:
#             if isinstance(result['IsSPA'], str):
#                 result['IsSPA'] = result['IsSPA'].lower() == 'true'
#             else:
#                 result['IsSPA'] = bool(result['IsSPA'])

#     return jsonify({
#         'SnpEpistasis_results': results,
#         'total_count': total_count
#     })



# @app.route('/api/SnpEpistasis', methods=['GET'])
# def get_snp_epistasis():
#     select_cancer_type = request.args.get('selectCancerType', 'All')  # Default to 'All' if not provided
#     p_value_threshold = float(request.args.get('pValueThreshold', '0.05'))
#     query_rsid1 = request.args.get('queryRsid1', '').strip()
#     select_query_type = request.args.get('selectQueryType', 'SNP')
#     current_page = int(request.args.get('currentPage', '1'))  # 当前页码
#     per_page = int(request.args.get('perPage', '8'))  # 每页展示的记录数
#     example = request.args.get('example', 'false').lower() == 'true'  # 获取example参数

#     # 创建查询条件
#     query = {
#         'P': {'$lt': p_value_threshold}
#     }

#     # 如果传递了example参数，则只筛选Type列为true的记录
#     if example:
#         query['Type'] = True
#     else:
#         if select_cancer_type != 'All':
#             query['Cancertype'] = select_cancer_type
#         if select_query_type == 'SNP' or select_query_type == 'SNP Epistasis':
#             if query_rsid1:
#                 if '_' in query_rsid1:
#                     snp1, snp2 = query_rsid1.split('_')
#                     query['$or'] = [
#                         {'SNP1': snp1, 'SNP2': snp2},
#                         {'SNP1': snp2, 'SNP2': snp1}
#                     ]
#                 else:
#                     query['$or'] = [
#                         {'SNP1': query_rsid1},
#                         {'SNP2': query_rsid1}
#                     ]

#     # 计算总记录数
#     total_count = collection_SnpEpistasisRes.count_documents(query)

#     # 分页查询
#     skip_records = (current_page - 1) * per_page
#     results = list(collection_SnpEpistasisRes.find(query).sort([("ORstatus",-1),("P",1)]).skip(skip_records).limit(per_page))

#     # 将 ObjectId 转换为字符串
#     for result in results:
#         if '_id' in result:
#             result['_id'] = str(result['_id'])
#         # 确保 IsSPA 是布尔值
#         if 'IsSPA' in result:
#             if isinstance(result['IsSPA'], str):
#                 result['IsSPA'] = result['IsSPA'].lower() == 'true'
#             else:
#                 result['IsSPA'] = bool(result['IsSPA'])

#     return jsonify({
#         'SnpEpistasis_results': results,
#         'total_count': total_count
#     })


# @app.route('/api/SnpEpistasis', methods=['GET'])
# def get_snp_epistasis():
#     select_cancer_type = request.args.get('selectCancerType', 'All')  # Default to 'All' if not provided
#     p_value_threshold = float(request.args.get('pValueThreshold', '0.05'))
#     query_rsid1 = request.args.get('queryRsid1', '').strip()
#     select_query_type = request.args.get('selectQueryType', 'SNP')
#     current_page = int(request.args.get('currentPage', '1'))  # 当前页码
#     per_page = int(request.args.get('perPage', '8'))  # 每页展示的记录数
#     is_first_load = request.args.get('isFirstLoad', 'false').lower() == 'true'  # 获取isFirstLoad参数

#     # 创建查询条件
#     query = {
#         'P': {'$lt': p_value_threshold}
#     }

#     # 如果是首次加载，则筛选Type列为true的记录
#     if is_first_load:
#         query['Type'] = True
#     else:
#         if select_cancer_type != 'All':
#             query['Cancertype'] = select_cancer_type
#         if select_query_type == 'SNP':
#             if query_rsid1:
#                 query['$or'] = [
#                     {'SNP1': query_rsid1},
#                     {'SNP2': query_rsid1}
#                 ]
#         elif select_query_type == 'SNP epistasis':
#             if query_rsid1 and '_' in query_rsid1:
#                 snp1, snp2 = query_rsid1.split('_')
#                 query['$or'] = [
#                     {'SNP1': snp1, 'SNP2': snp2},
#                     {'SNP1': snp2, 'SNP2': snp1}
#                 ]

#     # 计算总记录数
#     total_count = collection_SnpEpistasisRes.count_documents(query)

#     # 分页查询
#     skip_records = (current_page - 1) * per_page
#     results = list(collection_SnpEpistasisRes.find(query).sort([("ORstatus",-1),("P",1)]).skip(skip_records).limit(per_page))

#     # 将 ObjectId 转换为字符串
#     for result in results:
#         if '_id' in result:
#             result['_id'] = str(result['_id'])
#         # 确保 IsSPA 是布尔值
#         if 'IsSPA' in result:
#             if isinstance(result['IsSPA'], str):
#                 result['IsSPA'] = result['IsSPA'].lower() == 'true'
#             else:
#                 result['IsSPA'] = bool(result['IsSPA'])

#     return jsonify({
#         'SnpEpistasis_results': results,
#         'total_count': total_count
#     })

@app.route('/api/SnpEpistasis', methods=['GET'])
def get_snp_epistasis():
    select_cancer_type = request.args.get('selectCancerType', 'All')  # Default to 'All' if not provided
    p_value_threshold = float(request.args.get('pValueThreshold', '0.05'))
    query_rsid1 = request.args.get('queryRsid1', '').strip()
    select_query_type = request.args.get('selectQueryType', 'SNP')
    current_page = int(request.args.get('currentPage', '1'))  # 当前页码
    per_page = int(request.args.get('perPage', '8'))  # 每页展示的记录数
    is_first_load = request.args.get('isFirstLoad', 'false').lower() == 'true'  # 获取isFirstLoad参数

    # 创建查询条件
    query = {
        'P': {'$lt': p_value_threshold}
    }

    # 如果是首次加载，则筛选Type列为true的记录
    if is_first_load:
        query['Type'] = True
    else:
        if select_cancer_type != 'All':
            query['Cancertype'] = select_cancer_type
        
        if select_query_type == 'SNP':
            if query_rsid1:
                query['$or'] = [
                    {'SNP1': query_rsid1},
                    {'SNP2': query_rsid1}
                ]
        
        elif select_query_type == 'SNP epistasis':
            if query_rsid1 and '_' in query_rsid1:
                snp1, snp2 = query_rsid1.split('_')
                query['$or'] = [
                    {'SNP1': snp1, 'SNP2': snp2},
                    {'SNP1': snp2, 'SNP2': snp1}
                ]

    # 计算总记录数
    total_count = collection_SnpEpistasisRes.count_documents(query)

    # 分页查询
    skip_records = (current_page - 1) * per_page
    results = list(collection_SnpEpistasisRes.find(query).sort([("ORstatus",-1),("P",1)]).skip(skip_records).limit(per_page))

    # 将 ObjectId 转换为字符串
    for result in results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
        # 确保 IsSPA 是布尔值
        if 'IsSPA' in result:
            if isinstance(result['IsSPA'], str):
                result['IsSPA'] = result['IsSPA'].lower() == 'true'
            else:
                result['IsSPA'] = bool(result['IsSPA'])

    return jsonify({
        'SnpEpistasis_results': results,
        'total_count': total_count
    })

# 辅助函数：转换ObjectId为字符串
def convert_objectid_to_str(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

@app.route('/api/SnpEpistasisCancerTypeAnnovar', methods=['POST'])
def search_epistasis_cancer_type_annovar():
    try:
        data = request.json
        cancer_type = data.get('selectCancerType')
        snp_epistasis_id = data.get('queryRsid1')
        p_value_threshold = float(data.get('pValueThreshold', '0.05'))
        page = int(data.get('currentPage', '1'))
        perPage = int(data.get('perPage', '7'))
        if not cancer_type:
            return jsonify({'error': 'Missing required parameters'}), 400
        query = {
            'P': {'$lte': p_value_threshold},
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type
        
        offset = (page - 1) * perPage
        total = collection_Epistasis_Annovar.count_documents(query)
        results = list(collection_Epistasis_Annovar.find(query).sort([("Type",-1),("P",1)]).skip(offset).limit(perPage))
        results = [convert_objectid_to_str(doc) for doc in results]
        response = {
            'SnpEpistasisCancerTypeAnnovarResult': results,
            'total': total
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/SnpCancerTypeAnnovar', methods=['POST'])
def search_cancer_type_annovar():
    try:
        data = request.json
        cancer_type = data.get('selectCancerType')
        p_value_threshold = float(data.get('pValueThreshold', '0.05'))
        page = int(data.get('currentPage', '1'))
        perPage = int(data.get('pageSize', '7'))

        if not cancer_type:
            return jsonify({'error': 'Missing required parameters'}), 400

        query = {
            'P': {'$lte': p_value_threshold}
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type

        offset = (page - 1) * perPage
        total = collection_GWAS_Annovar.count_documents(query)
        results = list(collection_GWAS_Annovar.find(query).sort([("Type",-1),("P",1)]).skip(offset).limit(perPage))
        results = [convert_objectid_to_str(doc) for doc in results]
        response = {
            'SnpCancerTypeAnnovarResult': results,
            'total': total
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/SnpAnnovar', methods=['POST'])
def search_snp_annovar():
    try:
        data = request.json
        cancer_type = data.get('selectCancerType')
        snp_id = data.get('queryRsid1')
        p_value_threshold = float(data.get('pValueThreshold', '0.05'))
        page = int(data.get('currentPage', '1'))
        perPage = int(data.get('perPage', '7'))
        if not cancer_type or not snp_id:
            return jsonify({'error': 'Missing required parameters'}), 400

        query = {
            'SNP': snp_id,
            'P': {'$lte': p_value_threshold}
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type

        offset = (page - 1) * perPage
        total = collection_GWAS_Annovar.count_documents(query)
        results = list(collection_GWAS_Annovar.find(query).sort([("Type",1),("P",1)]).skip(offset).limit(perPage))
        results = [convert_objectid_to_str(doc) for doc in results]

        response = {
            'SnpAnnovarResult': results,
            'total': total
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/SnpEpistasisAnnovar', methods=['POST'])
def search_epistasis_annovar():
    try:
        data = request.json
        cancer_type = data.get('selectCancerType')
        snp_epistasis_id = data.get('queryRsid1')
        p_value_threshold = float(data.get('pValueThreshold', '0.05'))
        page = int(data.get('currentPage', '1'))
        perPage = int(data.get('perPage', '7'))
        if not cancer_type or not snp_epistasis_id:
            return jsonify({'error': 'Missing required parameters'}), 400

        snp1, snp2 = snp_epistasis_id.split('_')
        query = {
            'P': {'$lte': p_value_threshold},
            '$or': [
                {'SNP1': snp1, 'SNP2': snp2},
                {'SNP1': snp2, 'SNP2': snp1}
            ]
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type
        offset = (page - 1) * perPage
        total = collection_Epistasis_Annovar.count_documents(query)
        results = list(collection_Epistasis_Annovar.find(query).sort([("Type",-1),("P",1)]).skip(offset).limit(perPage))
        results = [convert_objectid_to_str(doc) for doc in results]
        response = {
            'SnpEpistasisAnnovarResult': results,
            'total': total
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


BASE_PATH = '/home/wuxh/SSIdb2/ssidb/src/assets/02.Epistasis.plot/OR'
app.config['Epistasis_ORpng'] = {
    'Breast': os.path.join(BASE_PATH, '1.breast.all'),
    'Prostate': os.path.join(BASE_PATH, '2.prostate.all'),
    'Melanoma': os.path.join(BASE_PATH, '3.cutaneousMelanoma.all'),
    'Colon': os.path.join(BASE_PATH, '4.colon.all'),
    'Cervical': os.path.join(BASE_PATH, '5.cervical.all'),
    'Lung': os.path.join(BASE_PATH, '6.bronchialAndLung.all'),
    'Bladder': os.path.join(BASE_PATH, '7.bladder.all'),
    'Rectal': os.path.join(BASE_PATH, '8.rectal.all'),
    'Uterine': os.path.join(BASE_PATH, '9.uterine.all'),
    'Kidney': os.path.join(BASE_PATH, '10.kidney.all'),
    'Ovarian': os.path.join(BASE_PATH, '11.ovarian.all'),
    'Pancreatic': os.path.join(BASE_PATH, '12.pancreatic.all'),
    'Esophagus': os.path.join(BASE_PATH, '13.esophagus.all'),
    'Stomach': os.path.join(BASE_PATH, '14.stomach.all'),
    'Brain': os.path.join(BASE_PATH, '15.brain.all'),
    'Liver': os.path.join(BASE_PATH, '16.liverAndIntrahepaticBileDucts.all'),
}

app.config['Epistasis_ORpdf'] = {
    'Breast': os.path.join(BASE_PATH, '1.breast.all'),
    'Prostate': os.path.join(BASE_PATH, '2.prostate.all'),
    'Melanoma': os.path.join(BASE_PATH, '3.cutaneousMelanoma.all'),
    'Colon': os.path.join(BASE_PATH, '4.colon.all'),
    'Cervical': os.path.join(BASE_PATH, '5.cervical.all'),
    'Lung': os.path.join(BASE_PATH, '6.bronchialAndLung.all'),
    'Bladder': os.path.join(BASE_PATH, '7.bladder.all'),
    'Rectal': os.path.join(BASE_PATH, '8.rectal.all'),
    'Uterine': os.path.join(BASE_PATH, '9.uterine.all'),
    'Kidney': os.path.join(BASE_PATH, '10.kidney.all'),
    'Ovarian': os.path.join(BASE_PATH, '11.ovarian.all'),
    'Pancreatic': os.path.join(BASE_PATH, '12.pancreatic.all'),
    'Esophagus': os.path.join(BASE_PATH, '13.esophagus.all'),
    'Stomach': os.path.join(BASE_PATH, '14.stomach.all'),
    'Brain': os.path.join(BASE_PATH, '15.brain.all'),
    'Liver': os.path.join(BASE_PATH, '16.liverAndIntrahepaticBileDucts.all'),
}

@app.route('/api/SnpEpistasisORgetPdf', methods=['GET'])
def SnpEpistasisORget_pdf():
    cancertype = request.args.get('Cancertype')
    snp_epi = request.args.get('SNPepi')
    if cancertype in app.config['Epistasis_ORpng']:
        image_file_name = "{}_{}.png".format(cancertype, snp_epi)
        image_file_path = os.path.join(app.config['Epistasis_ORpng'][cancertype], image_file_name)

        # 文件存在性验证
        if os.path.exists(image_file_path):
            return send_file(image_file_path, mimetype='image/png')
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400

@app.route('/api/SnpEpistasisORdownloadPdf', methods=['GET'])
def SnpEpistasisORdownload_pdf():
    cancertype = request.args.get('Cancertype')
    snp_epi = request.args.get('SNPepi')
    if not cancertype or not snp_epi:
        return jsonify({"error": "Missing required parameters"}), 400
    if cancertype in app.config['Epistasis_ORpdf']:
        pdf_file_name = "{}_{}.pdf".format(cancertype, snp_epi)
        pdf_file_path = os.path.join(app.config['Epistasis_ORpdf'][cancertype], pdf_file_name)
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400





BASE_PATH2 = '/home/wuxh/new_test/epidatabase/src/assets/02.Epistasis.plot/Sample/'
app.config['Epistasis_Samplepng'] = {
    'Breast': os.path.join(BASE_PATH2, '1.breast.all'),
    'Prostate': os.path.join(BASE_PATH2, '2.prostate.all'),
    'Melanoma': os.path.join(BASE_PATH2, '3.cutaneousMelanoma.all'),
    'Colon': os.path.join(BASE_PATH2, '4.colon.all'),
    'Cervical': os.path.join(BASE_PATH2, '5.cervical.all'),
    'Lung': os.path.join(BASE_PATH2, '6.bronchialAndLung.all'),
    'Bladder': os.path.join(BASE_PATH2, '7.bladder.all'),
    'Rectal': os.path.join(BASE_PATH2, '8.rectal.all'),
    'Uterine': os.path.join(BASE_PATH2, '9.uterine.all'),
    'Kidney': os.path.join(BASE_PATH2, '10.kidney.all'),
    'Ovarian': os.path.join(BASE_PATH2, '11.ovarian.all'),
    'Pancreatic': os.path.join(BASE_PATH2, '12.pancreatic.all'),
    'Esophagus': os.path.join(BASE_PATH2, '13.esophagus.all'),
    'Stomach': os.path.join(BASE_PATH2, '14.stomach.all'),
    'Brain': os.path.join(BASE_PATH2, '15.brain.all'),
    'Liver': os.path.join(BASE_PATH2, '16.liverAndIntrahepaticBileDucts.all'),
}

app.config['Epistasis_Samplepdf'] = {
    'Breast': os.path.join(BASE_PATH2, '1.breast.all'),
    'Prostate': os.path.join(BASE_PATH2, '2.prostate.all'),
    'Melanoma': os.path.join(BASE_PATH2, '3.cutaneousMelanoma.all'),
    'Colon': os.path.join(BASE_PATH2, '4.colon.all'),
    'Cervical': os.path.join(BASE_PATH2, '5.cervical.all'),
    'Lung': os.path.join(BASE_PATH2, '6.bronchialAndLung.all'),
    'Bladder': os.path.join(BASE_PATH2, '7.bladder.all'),
    'Rectal': os.path.join(BASE_PATH2, '8.rectal.all'),
    'Uterine': os.path.join(BASE_PATH2, '9.uterine.all'),
    'Kidney': os.path.join(BASE_PATH2, '10.kidney.all'),
    'Ovarian': os.path.join(BASE_PATH2, '11.ovarian.all'),
    'Pancreatic': os.path.join(BASE_PATH2, '12.pancreatic.all'),
    'Esophagus': os.path.join(BASE_PATH2, '13.esophagus.all'),
    'Stomach': os.path.join(BASE_PATH2, '14.stomach.all'),
    'Brain': os.path.join(BASE_PATH2, '15.brain.all'),
    'Liver': os.path.join(BASE_PATH2, '16.liverAndIntrahepaticBileDucts.all'),
}

@app.route('/api/SnpEpistasisSamplegetPdf', methods=['GET'])
def SnpEpistasisSampleget_pdf():
    cancertype = request.args.get('Cancertype')
    snp_epi = request.args.get('SNPepi')
    if cancertype in app.config['Epistasis_Samplepng']:
        image_file_name = "{}_{}.png".format(cancertype, snp_epi)
        image_file_path = os.path.join(app.config['Epistasis_Samplepng'][cancertype], image_file_name)

        # 文件存在性验证
        if os.path.exists(image_file_path):
            return send_file(image_file_path, mimetype='image/png')
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400

@app.route('/api/SnpEpistasisSampledownloadPdf', methods=['GET'])
def SnpEpistasisSampledownload_pdf():
    cancertype = request.args.get('Cancertype')
    snp_epi = request.args.get('SNPepi')
    if not cancertype or not snp_epi:
        return jsonify({"error": "Missing required parameters"}), 400
    if cancertype in app.config['Epistasis_Samplepdf']:
        pdf_file_name = "{}_{}.pdf".format(cancertype, snp_epi)
        pdf_file_path = os.path.join(app.config['Epistasis_Samplepdf'][cancertype], pdf_file_name)
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400




def get_collection(model, type='single'):
    if type == 'single':
        return {
            'Additive': collection_SingleAdditiveSurvival,
            'Recessive': collection_SingleRecessiveSurvival,
            'Dominant': collection_SingleDominantSurvival
        }.get(model)
    elif type == 'two':
        return {
            'Additive': collection_TwoAdditiveSurvival,
            'Recessive': collection_TwoRecessiveSurvival,
            'Dominant': collection_TwoDominantSurvival  
        }.get(model)

# @app.route('/api/SnpSurvival', methods=['POST'])
# def snp_survival():
#     data = request.get_json()
#     query_type = data.get('queryType')
#     cancer_type = data.get('cancerType')
#     model = data.get('model')
#     snp = data.get('snp')
#     page = int(data.get('page', 1))
#     page_size = int(data.get('pageSize', 8))
#     collection = get_collection(model, type='single')
#     if collection is None:
#         return jsonify({'error': 'Invalid model type'}), 400

#     query = {}
#     if snp:
#         query['SNP'] = snp
#     if cancer_type and cancer_type.lower() != 'all':
#         query['Cancertype'] = cancer_type

#     results = collection.find(query).sort([("P_Value",1)]).skip((page - 1) * page_size).limit(page_size)
#     total = collection.count_documents(query)
#     result_list = list(results)
#     for result in result_list:
#         result['_id'] = str(result['_id'])

#     return jsonify({'SnpSurvivalResult': result_list, 'total': total})


@app.route('/api/SnpSurvival', methods=['POST'])
def snp_survival():
    data = request.get_json()
    
    # 检查是否传递了初始化参数
    initial_param = data.get('Type')
    
    if initial_param is not None:
        
        query = {'Type': True}
        
        results = collection_SingleAdditiveSurvival.find(query).sort([("N",-1)])
        result_list = list(results)
        for result in result_list:
            result['_id'] = str(result['_id'])
        
        return jsonify({'collection_SingleAdditiveSurvivalResult': result_list})
    
    # 正常的参数处理
    query_type = data.get('queryType')
    cancer_type = data.get('cancerType')
    model = data.get('model')
    snp = data.get('snp')
    page = int(data.get('page', 1))
    page_size = int(data.get('pageSize', 8))
    collection = get_collection(model, type='single')
    if collection is None:
        return jsonify({'error': 'Invalid model type'}), 400

    query = {}
    if snp:
        query['SNP'] = snp
    if cancer_type and cancer_type.lower() != 'all':
        query['Cancertype'] = cancer_type

    results = collection.find(query).sort([("P_Value",1)]).skip((page - 1) * page_size).limit(page_size)
    total = collection.count_documents(query)
    result_list = list(results)
    for result in result_list:
        result['_id'] = str(result['_id'])

    return jsonify({'SnpSurvivalResult': result_list, 'total': total})





@app.route('/api/SnpCancerTypeSurvival', methods=['POST'])
def snp_cancer_type_survival():
    data = request.get_json()
    cancer_type = data.get('cancerType')
    model = data.get('model')
    snp = data.get('snp')
    page = int(data.get('page', '1'))
    page_size = int(data.get('pageSize', '8'))
    collection = get_collection(model, type='single')
    if collection is None:
        return jsonify({'error': 'Invalid model type'}), 400

    query = {}
    if cancer_type and cancer_type.lower() != 'all':
        query['Cancertype'] = cancer_type
    if snp:
        query['SNP'] = snp

    results = collection.find(query).sort([("P_Value",1)]).skip((page - 1) * page_size).limit(page_size)
    total = collection.count_documents(query)
    result_list = list(results)
    for result in result_list:
        result['_id'] = str(result['_id'])

    return jsonify({'SnpCancerTypeSurvivalResult': result_list, 'total': total})


@app.route('/api/SnpEpistasisSurvival', methods=['POST'])
def snp_epistasis_survival():
    data = request.get_json()
    cancer_type = data.get('cancerType')
    model = data.get('model')
    snp_epistasis = data.get('snp')
    page = int(data.get('page', '1'))
    page_size = int(data.get('pageSize', '8'))
    collection = get_collection(model, type='two')
    if collection is None:
        return jsonify({'error': 'Invalid model type'}), 400

    query = {}
    if snp_epistasis:
        snp_list = snp_epistasis.split('_')
        query['$or'] = [{'SNP1': {'$in': snp_list}}, {'SNP2': {'$in': snp_list}}]
    if cancer_type and cancer_type.lower() != 'all':
        query['Cancertype'] = cancer_type

    results = collection.find(query).sort([("P_Value",1)]).skip((page - 1) * page_size).limit(page_size)
    total = collection.count_documents(query)

    result_list = list(results)
    for result in result_list:
        result['_id'] = str(result['_id'])

    return jsonify({'SnpEpistasisSurvivalResult': result_list, 'total': total})

@app.route('/api/SnpEpistasisCancerTypeSurvival', methods=['POST'])
def snp_epistasis_cancer_type_survival():
    data = request.get_json()
    cancer_type = data.get('cancerType')
    model = data.get('model')
    snp_epistasis = data.get('snp')
    page = int(data.get('page', '1'))
    page_size = int(data.get('pageSize', '8'))
    collection = get_collection(model, type='two')
    if collection is None:
        return jsonify({'error': 'Invalid model type'}), 400

    query = {}
    if cancer_type.lower() != 'all':
        query['Cancertype'] = cancer_type
    if snp_epistasis:
        snp_list = snp_epistasis.split('_')
        query['SNP1'] = {'$in': snp_list}
        query['SNP2'] = {'$in': snp_list}

    results = collection.find(query).sort([("P_Value",1)]).skip((page - 1) * page_size).limit(page_size)
    total = collection.count_documents(query)
    result_list = list(results)
    for result in result_list:
        result['_id'] = str(result['_id'])

    return jsonify({'SnpEpistasisCancerTypeSurvivalResult': result_list, 'total': total})



app.config['Survival_png'] = {
    'Breast': '1.breast.all',
    'Prostate': '2.prostate.all',
    'Melanoma':'3.cutaneousMelanoma.all',
    'Colon': '4.colon.all',
    'Cervical': '5.cervical.all',
    'Lung': '6.bronchialAndLung.all',
    'Bladder': '7.bladder.all',
    'Rectal': '8.rectal.all',
    'Uterine': '9.uterine.all',
    'Kidney': '10.kidney.all',
    'Ovarian': '11.ovarian.all',
    'Pancreatic': '12.pancreatic.all',
    'Esophagus': '13.esophagus.all',
    'Stomach': '14.stomach.all',
    'Brain': '15.brain.all',
    'Liver': '16.liverAndIntrahepaticBileDucts.all',
}
app.config['Survival_pdf'] = {
    'Breast': '1.breast.all',
    'Prostate': '2.prostate.all',
    'Melanoma':'3.cutaneousMelanoma.all',
    'Colon': '4.colon.all',
    'Cervical': '5.cervical.all',
    'Lung': '6.bronchialAndLung.all',
    'Bladder': '7.bladder.all',
    'Rectal': '8.rectal.all',
    'Uterine': '9.uterine.all',
    'Kidney': '10.kidney.all',
    'Ovarian': '11.ovarian.all',
    'Pancreatic': '12.pancreatic.all',
    'Esophagus': '13.esophagus.all',
    'Stomach': '14.stomach.all',
    'Brain': '15.brain.all',
    'Liver': '16.liverAndIntrahepaticBileDucts.all',
}
def get_survival_path(cancertype, model, snp, filetype):
    base_path = "/home/wuxh/SSIdb2/ssidb/src/assets/04.Survival.plot"
    path_mapping = {
        ('additive', True): "04.two_additive_plot",
        ('dominant', True): "05.two_dominant_plot",
        ('recessive', True): "06.two_recessive_plot",
        ('additive', False): "01.Additive_plot",
        ('dominant', False): "02.Dominant_plot",
        ('recessive', False): "03.Recessive_plot"
    }
    key = (model, '_' in snp)
    subdir = path_mapping.get(key)
    if not subdir:
        return None

    return os.path.join(base_path, subdir, app.config['Survival_png'][cancertype], filetype)


@app.route('/api/SurvivalgetPdf', methods=['GET'])
def Survivalget_pdf():
    cancertype = request.args.get('Cancertype')
    model = request.args.get('Model')
    snp = request.args.get('SNP')
    logging.debug("Received parameters for PDF fetch: cancertype={}, model={}, snp={}".format(cancertype, model, snp))
    if not cancertype or not model or not snp:
        return jsonify({"error": "Missing required parameters"}), 400

    image_file_path = get_survival_path(cancertype, model, snp, "png")
    logging.debug("Image file path: {}".format(image_file_path))
    if not image_file_path:
        logging.error("Invalid parameters provided.")
        return jsonify({"error": "Invalid parameters"}), 400

    image_file_name = "{}.png".format(snp)
    image_file_full_path = os.path.join(image_file_path, image_file_name)
    logging.debug("Full image file path: {}".format(image_file_full_path))

    if os.path.exists(image_file_full_path):
        logging.info("Serving image file: {}".format(image_file_full_path))
        return send_file(image_file_full_path, mimetype='image/png')
    else:
        logging.error("File not found.")
        return '', 204


@app.route('/api/SurvivaldownloadPdf', methods=['GET'])
def Survivaldownload_pdf():
    cancertype = request.args.get('Cancertype')
    model = request.args.get('Model')
    snp = request.args.get('SNP')
    if not cancertype or not model or not snp:
        return jsonify({"error": "Missing required parameters"}), 400

    pdf_file_path = get_survival_path(cancertype, model, snp, "pdf")
    logging.debug("PDF file path: {}".format(pdf_file_path))
    if not pdf_file_path:
        logging.error("Invalid parameters provided.")
        return jsonify({"error": "Invalid parameters"}), 400

    pdf_file_name = "{}.pdf".format(snp)
    pdf_file_full_path = os.path.join(pdf_file_path, pdf_file_name)
    logging.debug("Full PDF file path: {}".format(pdf_file_full_path))
    if os.path.exists(pdf_file_full_path):
        logging.info("Serving PDF file: {}".format(pdf_file_full_path))
        return send_file(pdf_file_full_path, as_attachment=True)
    else:
        logging.error("File not found.")
        return jsonify({"error": "File not found"}), 404


@app.route('/api/DownloadPage', methods=['POST'])
def download_page():
    data = request.get_json()
    category = data.get('category')
    cancer_type = data.get('cancerType')
    if category == 'Epistasis':
        collection = collection_SnpEpistasisRes
        columns_to_return = ['Cancertype', 'SNP_epi', 'OR_INT', 'P', 'Best_snp', 'saige_p']
        # columns_to_return = ['Best_snp','Cancertype', 'OR_INT', 'P','SNP_epi', 'saige_p']
    elif category == 'GWAS':
        collection = collection_GWASres
        columns_to_return = ['Cancertype', 'SNP', 'BETA', 'P', 'case', 'control']
        # columns_to_return = ['P', 'Cancertype', 'BETA', 'SNP', 'case', 'control']
    else:
        return jsonify({'error': 'Invalid category'}), 400

    query = {'Cancertype': cancer_type}
    results = collection.find(query, {col: 1 for col in columns_to_return})
    result_list = []
    for result in results:
        result_filtered = {col: result.get(col) for col in columns_to_return}
        result_list.append(result_filtered)

    df = pd.DataFrame(result_list)
    if category == 'GWAS':
        # df.columns = ['Cancer Type', 'SNP', 'BETA', 'P-value', 'case', 'control']
        df.columns = ['BETA', 'Cancer Type', 'P-value', 'SNP', 'case', 'control']
    elif category == 'Epistasis':
        # df.columns = ['Cancer Type', 'SNP Epistasis', 'OR', 'P-value', 'Best Snp', 'P-saige']
        df.columns = ['Best Snp','Cancer Type', 'OR', 'P-value','SNP Epistasis', 'P-saige']

    csv_data = df.to_csv(index=False)
    return send_file(
        io.BytesIO(csv_data.encode()),
        mimetype='text/csv',
        as_attachment=True,
        attachment_filename="{}_{}.csv".format(category, cancer_type)
    )





@app.route('/api/mutationRequest', methods=['POST'])
def mutation_request():
    data = request.get_json()
    query_type = data.get('queryType')
    page = int(data.get('page', 1))
    per_page = int(data.get('perPage', 8))
    
    query = {}
    if query_type == 'Cancer type':
        cancer_type = data.get('cancerType', 'All')
        if cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type
    elif query_type == 'Gene':
        gene = data.get('gene', '').strip()
        if gene:
            query['$or'] = [{'Gene_X': gene}, {'Gene_Y': gene}]
    
    total = collection_mutation.count_documents(query)
    results = collection_mutation.find(query).sort([("Pvalue",1)]).skip((page - 1) * per_page).limit(per_page)
    
    result_list = list(results)
    for result in result_list:
        result['_id'] = str(result['_id'])  # 转换ObjectId为字符串
    
    return jsonify({'results': result_list, 'total': total})
    

mutation_path = "/home/wuxh/SSIdb3/EpiSNP-db/src/assets/05.mutation"

@app.route('/api/mutationPng', methods=['GET'])
def get_mutation_png():
    cancertype = request.args.get('Cancertype')
    mutation_x = request.args.get('Mutation_X')
    mutation_y = request.args.get('Mutation_Y')
    
    if not all([cancertype, mutation_x, mutation_y]):
        return abort(400, description="Missing parameters")

    filename = "{}_{}_{}.png".format(cancertype, mutation_x, mutation_y)
    file_path = os.path.join(mutation_path, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/png')
    else:
        return abort(404, description="File not found")

@app.route('/api/mutationPdf', methods=['GET'])
def download_mutation_pdf():
    cancertype = request.args.get('Cancertype')
    mutation_x = request.args.get('Mutation_X')
    mutation_y = request.args.get('Mutation_Y')

    if not all([cancertype, mutation_x, mutation_y]):
        return abort(400, description="Missing parameters")

    filename = "{}_{}_{}.pdf".format(cancertype, mutation_x, mutation_y)
    file_path = os.path.join(mutation_path, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return abort(404, description="File not found")


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=50000)












