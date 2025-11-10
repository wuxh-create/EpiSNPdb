# -*- coding: UTF-8 -*-
from flask import Flask, jsonify, request, send_file, abort, Response, make_response
from pymongo import MongoClient
from urllib.parse import quote_plus
# from bson.objectid import ObjectId
# from bson import json_util
import os 
import csv
import io
import logging
from app_temp import app
#app = Flask(__name__)
app.config['GWAS_png'] = {
    'Breast': '/app/EpiSNPdb/src/assets/01.GWAS.plot/1.breast.all',
    'Prostate': '/app/EpiSNPdb/src/assets/01.GWAS.plot/2.prostate.all',
    'Melanoma': '/app/EpiSNPdb/src/assets/01.GWAS.plot/3.cutaneousMelanoma.all',
    'Colon': '/app/EpiSNPdb/src/assets/01.GWAS.plot/4.colon.all',
    'Cervical': '/app/EpiSNPdb/src/assets/01.GWAS.plot/5.cervical.all',
    'Lung': '/app/EpiSNPdb/src/assets/01.GWAS.plot/6.bronchialAndLung.all',
    'Bladder': '/app/EpiSNPdb/src/assets/01.GWAS.plot/7.bladder.all',
    'Rectal': '/app/EpiSNPdb/src/assets/01.GWAS.plot/8.rectal.all',
    'Uterine': '/app/EpiSNPdb/src/assets/01.GWAS.plot/9.uterine.all',
    'Kidney': '/app/EpiSNPdb/src/assets/01.GWAS.plot/10.kidney.all',
    'Ovarian': '/app/EpiSNPdb/src/assets/01.GWAS.plot/11.ovarian.all',
    'Pancreatic': '/app/EpiSNPdb/src/assets/01.GWAS.plot/12.pancreatic.all',
    'Esophagus': '/app/EpiSNPdb/src/assets/01.GWAS.plot/13.esophagus.all',
    'Stomach': '/app/EpiSNPdb/src/assets/01.GWAS.plot/14.stomach.all',
    'Brain': '/app/EpiSNPdb/src/assets/01.GWAS.plot/15.brain.all',
    'Liver': '/app/EpiSNPdb/src/assets/01.GWAS.plot/16.liverAndIntrahepaticBileDucts.all'   
}
app.config['GWAS_pdf'] = {
    'Breast': '/app/EpiSNPdb/src/assets/01.GWAS.plot/1.breast.all',
    'Prostate': '/app/EpiSNPdb/src/assets/01.GWAS.plot/2.prostate.all',
    'Melanoma': '/app/EpiSNPdb/src/assets/01.GWAS.plot/3.cutaneousMelanoma.all',
    'Colon': '/app/EpiSNPdb/src/assets/01.GWAS.plot/4.colon.all',
    'Cervical': '/app/EpiSNPdb/src/assets/01.GWAS.plot/5.cervical.all',
    'Lung': '/app/EpiSNPdb/src/assets/01.GWAS.plot/6.bronchialAndLung.all',
    'Bladder': '/app/EpiSNPdb/src/assets/01.GWAS.plot/7.bladder.all',
    'Rectal': '/app/EpiSNPdb/src/assets/01.GWAS.plot/8.rectal.all',
    'Uterine': '/app/EpiSNPdb/src/assets/01.GWAS.plot/9.uterine.all',
    'Kidney': '/app/EpiSNPdb/src/assets/01.GWAS.plot/10.kidney.all',
    'Ovarian': '/app/EpiSNPdb/src/assets/01.GWAS.plot/11.ovarian.all',
    'Pancreatic': '/app/EpiSNPdb/src/assets/01.GWAS.plot/12.pancreatic.all',
    'Esophagus': '/app/EpiSNPdb/src/assets/01.GWAS.plot/13.esophagus.all',
    'Stomach': '/app/EpiSNPdb/src/assets/01.GWAS.plot/14.stomach.all',
    'Brain': '/app/EpiSNPdb/src/assets/01.GWAS.plot/15.brain.all',
    'Liver': '/app/EpiSNPdb/src/assets/01.GWAS.plot/16.liverAndIntrahepaticBileDucts.all'  
}

username = quote_plus('wuxh')
password = quote_plus('wuxh')
mongo_uri = f'mongodb://{username}:{password}@mongodb:27017/wuxh_database'
client = MongoClient(mongo_uri)

db = client['wuxh_database']
collection_GWASres = db['epiSNPGWASres']
collection_SnpEpistasisRes = db['NewSnpEpistasisRes']
collection_GWAS_Annovar = db['SnpGwasAnnovar']
collection_Epistasis_Annovar = db['SnpEpistasisAnnovar']
collection_SingleAdditiveSurvival = db['SingleAdditiveSurvival']
collection_SingleRecessiveSurvival = db['SingleRecessiveSurvival']
collection_SingleDominantSurvival = db['SingleDominantSurvival']
collection_TwoDominantSurvival = db['TwoDominantSurvival']
collection_TwoAdditiveSurvival = db['TwoAdditiveSurvival']
collection_TwoRecessiveSurvival = db['TwoRecessiveSurvival']
collection_mutation = db['MutationRes']
collection_GeneCor = db['GeneCor']

BASE_PATH = '/app/EpiSNPdb/src/assets/02.Epistasis.plot/OR'
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

BASE_PATH2 = '/app/EpiSNPdb/src/assets/02.Epistasis.plot/Sample/'
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

@app.route('/api/quickSearchSnp', methods=['GET'])
def quick_search_snp():
    query_id = request.args.get('queryID')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('perPage', 8))
    skip = (page - 1) * per_page

    # GWAS查询
    gwas_query = {"SNP": {"$regex": query_id, "$options": "i"}} if query_id else {}
    gwas_results = list(collection_GWASres.find(gwas_query).sort([("P", 1)]).skip(skip).limit(per_page))
    total_gwas_count = collection_GWASres.count_documents(gwas_query)

    # Epistasis查询 - 添加分页和排序
    epi_query = {"$or": [{"SNP1": query_id}, {"SNP2": query_id}]} if query_id else {}
    epi_results = list(collection_SnpEpistasisRes.find(epi_query).sort([("ORstatus", -1), ("P", 1)]).skip(skip).limit(per_page))
    total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)
    
    # 处理所有结果的_id字段
    for result in gwas_results + epi_results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
    
    # 处理epistasis结果的特殊字段（参考成功API的处理方式）
    for result in epi_results:
        if 'IsSPA' in result:
            if isinstance(result['IsSPA'], str):
                result['IsSPA'] = result['IsSPA'].lower() == 'true'
            else:
                result['IsSPA'] = bool(result['IsSPA'])

    # 直接使用原始结果，不进行字段映射转换
    epi_table_results = epi_results
    
    # 网络图数据处理
    epi_network_results = [{
        "SNPepi": epi_result.get("SNP_epi"),  # 注意字段名可能是SNP_epi
        "pos1": epi_result.get("pos1"),
        "pos2": epi_result.get("pos2")
    } for epi_result in epi_results]

    return jsonify({
        "SNPGWAS": gwas_results,
        "SNPEpiTable": epi_table_results,
        "SNPEpiNetwork": epi_network_results,
        "recordsNumber": total_gwas_count,
        "epiRecordsNumber": total_epi_count  # 添加epistasis结果总数
    })


@app.route('/api/getPdf', methods=['GET'])
def get_pdf():
    cancertype = request.args.get('Cancertype')
    snp = request.args.get('SNP')
    if cancertype in app.config['GWAS_png']:
        image_file_name = f'{cancertype}_{snp}.png'
        image_file_path = os.path.join(app.config['GWAS_png'][cancertype], image_file_name)

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
        pdf_file_name = f"{cancertype}_{snp}.pdf"
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
    cw.writerow(['Cancertype', 'SNP', 'Position', 'Alleles(A/a)', 'MAF', 'A1', 'A2', 'AF1', 'Beta', 'P_value', 'Sample'])
    for result in results:
        position = f"{result['Pos']}:{result['POS']}"
        cw.writerow([result['Cancertype'], result['SNP'], position, 
                     result['Alleles'], result['MAF'], result['A1'], 
                     result['A2'], result['AF1'], result['BETA'], 
                     result['P'], result['N']])
    
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = f"attachment; filename={query_id}_GWAS_res.csv"
    output.headers["Content-type"] = "text/csv"
    return output


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

        # GWAS查询
        query = {
            "Pos": chromosome,
            "POS": {"$gte": start, "$lte": end}
        }
        results = list(collection_GWASres.find(query).sort([("P",1)]).skip(skip).limit(per_page))
        total_count = collection_GWASres.count_documents(query)

        # Epistasis查询
        epi_query = {
            "$or": [
                {"Chr1": chromosome, "pos1": {"$gte": start, "$lte": end}},
                {"Chr2": chromosome, "pos2": {"$gte": start, "$lte": end}}
            ]
        }
        epi_results = list(collection_SnpEpistasisRes.find(epi_query).sort([("ORstatus",-1),("P",1)]).skip(skip).limit(per_page))
        total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)

        # 处理所有结果的_id字段和特殊字段
        for result in results + epi_results:
            if '_id' in result:
                result['_id'] = str(result['_id'])

        # 处理epistasis结果的特殊字段（参考成功API的处理方式）
        for result in epi_results:
            if 'IsSPA' in result:
                if isinstance(result['IsSPA'], str):
                    result['IsSPA'] = result['IsSPA'].lower() == 'true'
                else:
                    result['IsSPA'] = bool(result['IsSPA'])

        # 直接使用原始结果，不进行字段映射转换
        epi_table_results = epi_results
        
        # 网络结果只提取需要的字段
        epi_network_results = [{
            "SNPepi": epi_result.get("SNP_epi"),
            "pos1": epi_result.get("pos1"),
            "pos2": epi_result.get("pos2")
        } for epi_result in epi_results]

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
    data = request.json.get('data')
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
        position = f"{item['Pos']}:{item['POS']}"
        cw.writerow([item['Cancertype'], item['SNP'], position, 
                     item['Alleles'], item['MAF'], item['A1'], 
                     item['A2'], item['AF1'], item['BETA'], 
                     item['P'], item['N']])
    filename = f"{chromosome}_{start}-{end}_Page_{currentPage}_GWAS.csv"
    output = Response(si.getvalue(), mimetype="text/csv")
    output.headers["Content-Disposition"] = f"attachment; filename={filename}"
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

    # 处理所有结果的_id字段和特殊字段
    for result in gwas_results + epi_results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
    
    # 处理epistasis结果的特殊字段（参考成功API的处理方式）
    for result in epi_results:
        if 'IsSPA' in result:
            if isinstance(result['IsSPA'], str):
                result['IsSPA'] = result['IsSPA'].lower() == 'true'
            else:
                result['IsSPA'] = bool(result['IsSPA'])

    # 直接使用原始结果，不进行字段映射转换
    epi_table_results = epi_results

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
    
    epistasis_parts = epistasis.split('_') if '_' in epistasis else [epistasis]

    epi_query = {
        "Cancertype": cancertype,
        "$or": [
            {"SNP1": {"$in": epistasis_parts}},
            {"SNP2": {"$in": epistasis_parts}}
        ]
    }
    epi_results = list(collection_SnpEpistasisRes.find(epi_query))
    total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)

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
        per_page = int(request.args.get('perPage', 20))
        skip = (page - 1) * per_page

        yi, er = query_id.split('_')

        epi_query = {
            "$or": [
                {"SNP1": yi, "SNP2": er},
                {"SNP1": er, "SNP2": yi}
            ]
        }
        epi_results = list(collection_SnpEpistasisRes.find(epi_query).sort([("ORstatus", -1), ("P", 1)]).skip(skip).limit(per_page))
        total_epi_count = collection_SnpEpistasisRes.count_documents(epi_query)

        gwas_query = {
            "SNP": {"$in": [yi, er]}
        }
        gwas_results = list(collection_GWASres.find(gwas_query).sort([("P", 1)]).skip(skip).limit(per_page))
        gwas_total_count = collection_GWASres.count_documents(gwas_query)

        # 处理所有结果的_id字段和特殊字段
        for result in gwas_results + epi_results:
            if '_id' in result:
                result['_id'] = str(result['_id'])
        
        # 处理epistasis结果的特殊字段（参考成功API的处理方式）
        for result in epi_results:
            if 'IsSPA' in result:
                if isinstance(result['IsSPA'], str):
                    result['IsSPA'] = result['IsSPA'].lower() == 'true'
                else:
                    result['IsSPA'] = bool(result['IsSPA'])

        # 直接使用原始结果，不进行字段映射转换
        epi_table_results = epi_results

        epi_network_results = [{
            "SNPepi": epi_result.get("SNP_epi"),
            "pos1": epi_result.get("pos1"),
            "pos2": epi_result.get("pos2")
        } for epi_result in epi_results]

        return jsonify({
            "SNPGWASPosition": gwas_results,
            "SNPEpiTable": epi_table_results,
            "SNPEpiNetwork": epi_network_results,
            "recordsNumber": gwas_total_count,
            "epiRecordsNumber": total_epi_count
        })
    except ValueError:
        return jsonify({"error": "Invalid parameters"}), 400

# def convert_objectid_to_str(doc):
    # if '_id' in doc and isinstance(doc['_id'], ObjectId):
    #     doc['_id'] = str(doc['_id'])
    # return doc

@app.route('/api/SnpGwasSearchThreeWay', methods=['POST'])
def search():
    data = request.json

    if 'Type' in data:
        query = {'Type': True}
        total = collection_GWASres.count_documents(query)
        results = list(collection_GWASres.find(query).sort([("P", 1)]))
        # results = [convert_objectid_to_str(doc) for doc in results]
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
    # results = [convert_objectid_to_str(doc) for doc in results]
    SnpGwasSearchThreeWayResult = {
        'results': results,
        'total': total
    }
    return jsonify(SnpGwasSearchThreeWayResult)

@app.route('/api/SnpEpistasis', methods=['GET'])
def get_snp_epistasis():
    select_cancer_type = request.args.get('selectCancerType', 'All')
    p_value_threshold = float(request.args.get('pValueThreshold', '0.05'))
    query_rsid1 = request.args.get('queryRsid1', '').strip()
    select_query_type = request.args.get('selectQueryType', 'SNP')
    current_page = int(request.args.get('currentPage', '1'))
    per_page = int(request.args.get('perPage', '8'))
    is_first_load = request.args.get('isFirstLoad', 'false').lower() == 'true'

    query = {}
    
    p_value_conditions = []
    if p_value_threshold != 100:
        p_value_conditions.append({'P_epistasis': {'$lt': p_value_threshold, '$ne': 100}})
        p_value_conditions.append({'P_joint': {'$lt': p_value_threshold, '$ne': 100}})
        p_value_conditions.append({'P_boost': {'$lt': p_value_threshold, '$ne': 100}})

    if p_value_conditions:
        query['$or'] = p_value_conditions
    
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

    total_count = collection_SnpEpistasisRes.count_documents(query)
    skip_records = (current_page - 1) * per_page
    results = list(collection_SnpEpistasisRes.find(query).sort([("ORstatus",-1),("P",1)]).skip(skip_records).limit(per_page))

    for result in results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
        if 'IsSPA' in result:
            if isinstance(result['IsSPA'], str):
                result['IsSPA'] = result['IsSPA'].lower() == 'true'
            else:
                result['IsSPA'] = bool(result['IsSPA'])

    return jsonify({
        'SnpEpistasis_results': results,
        'total_count': total_count
    })


BASE_PATH = '/app/EpiSNPdb/src/assets/06.GeneCor'
app.config['GeneCor_png'] = {
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
app.config['GeneCor_pdf'] = {
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
@app.route('/api/GeneCorrelation', methods=['GET'])
def get_gene_correlation():
    select_cancer_type = request.args.get('selectCancerType', 'All')
    correlation_threshold = float(request.args.get('correlationThreshold', '0.1'))
    query_gene1 = request.args.get('queryGene1', '').strip()
    select_query_type = request.args.get('selectQueryType', 'Gene')
    current_page = int(request.args.get('currentPage', '1'))
    per_page = int(request.args.get('perPage', '8'))
    is_first_load = request.args.get('isFirstLoad', 'false').lower() == 'true'

    query = {}
    
    # Add correlation threshold filter - 排除NA值并进行数值比较
    if correlation_threshold != 0:
        query['$and'] = [
            {'correlation': {'$ne': 'NA'}},  # 排除NA值
            {'$or': [
                {'correlation': {'$gte': correlation_threshold}},
                {'correlation': {'$lte': -correlation_threshold}}
            ]}
        ]
    
    if is_first_load:
        if '$and' in query:
            query['$and'].append({'Type': True})
        else:
            query['Type'] = True
    else:
        if select_cancer_type != 'All':
            if '$and' in query:
                query['$and'].append({'Cancertype': select_cancer_type})
            else:
                query['Cancertype'] = select_cancer_type
        
        if select_query_type == 'Gene':
            if query_gene1:
                gene_filter = {'$or': [
                    {'Gene1': query_gene1},
                    {'Gene2': query_gene1}
                ]}
                if '$and' in query:
                    query['$and'].append(gene_filter)
                else:
                    query.update(gene_filter)
        
        elif select_query_type == 'Gene epistasis':
            if query_gene1 and '_' in query_gene1:
                gene1, gene2 = query_gene1.split('_', 1)
                epistasis_filter = {'$or': [
                    {'Gene1': gene1, 'Gene2': gene2},
                    {'Gene1': gene2, 'Gene2': gene1}
                ]}
                if '$and' in query:
                    query['$and'].append(epistasis_filter)
                else:
                    query.update(epistasis_filter)
        
        elif select_query_type == 'Cancer type':
            # Only cancer type and correlation threshold filters apply
            pass

    total_count = collection_GeneCor.count_documents(query)
    skip_records = (current_page - 1) * per_page
    
    # Sort by absolute correlation value descending, then by p-value ascending
    # 但需要处理NA值的排序问题
    results = list(collection_GeneCor.find(query).sort([
        ("correlation", -1), 
        ("P_value", 1)
    ]).skip(skip_records).limit(per_page))

    for result in results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
        
        # 安全地处理可能包含'NA'的数值字段
        def safe_float_convert(value):
            """安全地将值转换为float，如果是'NA'则保持不变"""
            if value is None or value == 'NA':
                return value
            try:
                return float(value)
            except (ValueError, TypeError):
                return value
        
        # 处理各个可能包含NA的字段
        if 'correlation' in result:
            result['correlation'] = safe_float_convert(result['correlation'])
        
        if 'P_value' in result:
            result['P_value'] = safe_float_convert(result['P_value'])
        
        if 'textmining_transferred' in result:
            result['textmining_transferred'] = safe_float_convert(result['textmining_transferred'])
        
        if 'combined_score' in result:
            result['combined_score'] = safe_float_convert(result['combined_score'])

    return jsonify({
        'GeneCorrelation_results': results,
        'total_count': total_count
    })

# 同时需要修改图片获取的API
@app.route('/api/GeneCorrelationPlot', methods=['GET'])
def get_gene_correlation_plot():
    cancertype = request.args.get('Cancertype')
    gene1 = request.args.get('Gene1')
    gene2 = request.args.get('Gene2')
    
    if not cancertype or not gene1 or not gene2:
        return jsonify({"error": "Missing required parameters"}), 400
    
    if cancertype in app.config['GeneCor_png']:
        image_file_name = f"{cancertype}_{gene1}_{gene2}.png"
        image_file_path = os.path.join(app.config['GeneCor_png'][cancertype], image_file_name)
        
        # Also try the reverse gene order
        if not os.path.exists(image_file_path):
            image_file_name = f"{cancertype}_{gene2}_{gene1}.png"
            image_file_path = os.path.join(app.config['GeneCor_png'][cancertype], image_file_name)

        if os.path.exists(image_file_path):
            return send_file(image_file_path, mimetype='image/png')
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400

@app.route('/api/GeneCorrelationPlotDownload', methods=['GET'])
def download_gene_correlation_plot():
    cancertype = request.args.get('Cancertype')
    gene1 = request.args.get('Gene1')
    gene2 = request.args.get('Gene2')
    
    if not cancertype or not gene1 or not gene2:
        return jsonify({"error": "Missing required parameters"}), 400
    
    if cancertype in app.config['GeneCor_pdf']:
        pdf_file_name = f"{cancertype}_{gene1}_{gene2}.pdf"
        pdf_file_path = os.path.join(app.config['GeneCor_pdf'][cancertype], pdf_file_name)
        
        # Also try the reverse gene order
        if not os.path.exists(pdf_file_path):
            pdf_file_name = f"{cancertype}_{gene2}_{gene1}.pdf"
            pdf_file_path = os.path.join(app.config['GeneCor_pdf'][cancertype], pdf_file_name)
        
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400

@app.route('/api/SnpEpistasisCancerTypeAnnovar', methods=['POST'])
def search_epistasis_cancer_type_annovar():
    try:
        data = request.json
        cancer_type = data.get('selectCancerType')
        p_value_threshold = float(data.get('pValueThreshold', '0.05'))
        page = int(data.get('currentPage', '1'))
        perPage = int(data.get('perPage', '7'))
        
        if not cancer_type:
            return jsonify({'error': 'Missing required parameters'}), 400
            
        # 修复：使用 P_epistasis 而不是 P
        query = {
            'P_epistasis': {'$lte': p_value_threshold},
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type
        
        offset = (page - 1) * perPage
        total = collection_Epistasis_Annovar.count_documents(query)
        results = list(collection_Epistasis_Annovar.find(query, {'_id': 0}).sort([("Type", -1), ("P_epistasis", 1)]).skip(offset).limit(perPage))
        
        # 添加 P 字段用于前端显示
        for result in results:
            result['P'] = result.get('P_epistasis')

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
        # 修复：统一使用 perPage
        perPage = int(data.get('perPage', '7'))

        if not cancer_type:
            return jsonify({'error': 'Missing required parameters'}), 400

        query = {
            'P': {'$lte': p_value_threshold}
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type

        offset = (page - 1) * perPage
        total = collection_GWAS_Annovar.count_documents(query)
        results = list(collection_GWAS_Annovar.find(query, {'_id': 0}).sort([("Type", -1), ("P", 1)]).skip(offset).limit(perPage))

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
        results = list(collection_GWAS_Annovar.find(query, {'_id': 0}).sort([("Type", 1), ("P", 1)]).skip(offset).limit(perPage))

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
        # 修复：使用 P_epistasis 而不是 P
        query = {
            'P_epistasis': {'$lte': p_value_threshold},
            '$or': [
                {'SNP1': snp1, 'SNP2': snp2},
                {'SNP1': snp2, 'SNP2': snp1}
            ]
        }
        if cancer_type and cancer_type.lower() != 'all':
            query['Cancertype'] = cancer_type
            
        offset = (page - 1) * perPage
        total = collection_Epistasis_Annovar.count_documents(query)
        results = list(collection_Epistasis_Annovar.find(query, {'_id': 0}).sort([("Type", -1), ("P_epistasis", 1)]).skip(offset).limit(perPage))
        
        # 添加 P 字段用于前端显示（如果需要）
        for result in results:
            result['P'] = result.get('P_epistasis')

        response = {
            'SnpEpistasisAnnovarResult': results,
            'total': total
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/SnpEpistasisORgetPdf', methods=['GET'])
def SnpEpistasisORget_pdf():
    cancertype = request.args.get('Cancertype')
    snp_epi = request.args.get('SNPepi')
    if cancertype in app.config['Epistasis_ORpng']:
        image_file_name = f"{cancertype}_{snp_epi}.png"
        image_file_path = os.path.join(app.config['Epistasis_ORpng'][cancertype], image_file_name)

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
        pdf_file_name = f"{cancertype}_{snp_epi}.pdf"
        pdf_file_path = os.path.join(app.config['Epistasis_ORpdf'][cancertype], pdf_file_name)
        if os.path.exists(pdf_file_path):
            return send_file(pdf_file_path, as_attachment=True)
        else:
            return '', 204
    else:
        return jsonify({"error": "Invalid cancer type"}), 400

@app.route('/api/SnpEpistasisSamplegetPdf', methods=['GET'])
def SnpEpistasisSampleget_pdf():
    cancertype = request.args.get('Cancertype')
    snp_epi = request.args.get('SNPepi')
    if cancertype in app.config['Epistasis_Samplepng']:
        image_file_name = f"{cancertype}_{snp_epi}.png"
        image_file_path = os.path.join(app.config['Epistasis_Samplepng'][cancertype], image_file_name)

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
        pdf_file_name = f"{cancertype}_{snp_epi}.pdf"
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

@app.route('/api/SnpSurvival', methods=['POST'])
def snp_survival():
    data = request.get_json()
    
    if 'Type' in data:
        query = {'Type': True}
        results = collection_SingleAdditiveSurvival.find(query).sort([("N",-1)])
        result_list = list(results)
        for result in result_list:
            result['_id'] = str(result['_id'])
        return jsonify({'collection_SingleAdditiveSurvivalResult': result_list})
    
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
    base_path = "/app/EpiSNPdb/src/assets/04.Survival.plot/"
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
    logging.debug(f"Received parameters for PDF fetch: cancertype={cancertype}, model={model}, snp={snp}")
    if not cancertype or not model or not snp:
        return jsonify({"error": "Missing required parameters"}), 400

    image_file_path = get_survival_path(cancertype, model, snp, "png")
    logging.debug(f"Image file path: {image_file_path}")
    if not image_file_path:
        logging.error("Invalid parameters provided.")
        return jsonify({"error": "Invalid parameters"}), 400

    image_file_name = f"{snp}.png"
    image_file_full_path = os.path.join(image_file_path, image_file_name)
    logging.debug(f"Full image file path: {image_file_full_path}")

    if os.path.exists(image_file_full_path):
        logging.info(f"Serving image file: {image_file_full_path}")
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
    logging.debug(f"PDF file path: {pdf_file_path}")
    if not pdf_file_path:
        logging.error("Invalid parameters provided.")
        return jsonify({"error": "Invalid parameters"}), 400

    pdf_file_name = f"{snp}.pdf"
    pdf_file_full_path = os.path.join(pdf_file_path, pdf_file_name)
    logging.debug(f"Full PDF file path: {pdf_file_full_path}")
    if os.path.exists(pdf_file_full_path):
        logging.info(f"Serving PDF file: {pdf_file_full_path}")
        return send_file(pdf_file_full_path, as_attachment=True)
    else:
        logging.error("File not found.")
        return jsonify({"error": "File not found"}), 404

# 配置文件存储路径
FILE_STORAGE_PATH = '/app/EpiSNPdb/src/assets/02.Epistasis.plot'

@app.route('/api/DownloadFile', methods=['POST'])
def download_file():
    """
    直接下载预处理好的文件
    """
    try:
        # 获取请求参数
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        category = data.get('category')
        cancer_type = data.get('cancerType')
        
        # 验证必需参数
        if not category or not cancer_type:
            return jsonify({'error': 'Missing required parameters: category and cancerType'}), 400
        
        # 验证category参数
        if category not in ['Epistasis', 'GWAS']:
            return jsonify({'error': 'Invalid category. Must be "Epistasis" or "GWAS"'}), 400
        
        # 验证cancer_type参数（可选，增加安全性）
        valid_cancer_types = [
            "Breast", "Prostate", "Melanoma", "Colon", "Cervical", "Lung", 
            "Bladder", "Rectal", "Uterine", "Kidney", "Ovarian", "Pancreatic",
            "Esophagus", "Stomach", "Brain", "Liver"
        ]
        
        if cancer_type not in valid_cancer_types:
            return jsonify({'error': f'Invalid cancer type: {cancer_type}'}), 400
        
        # 构建文件路径
        filename = f"{category}_{cancer_type}.csv"
        file_path = os.path.join(FILE_STORAGE_PATH, filename)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")  # 日志记录
            return jsonify({'error': f'File not found: {filename}'}), 404
        
        # 检查文件是否可读
        if not os.access(file_path, os.R_OK):
            print(f"File not readable: {file_path}")  # 日志记录
            return jsonify({'error': f'File not accessible: {filename}'}), 403
        
        # 记录下载日志
        print(f"Downloading file: {file_path}")
        
        # 返回文件
        return send_file(
            file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename  # 使用download_name而不是attachment_filename（Flask 2.0+）
        )
        
    except Exception as e:
        print(f"Error in download_file: {str(e)}")  # 日志记录
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/ListAvailableFiles', methods=['GET'])
def list_available_files():
    """
    可选的API：列出所有可用的文件
    """
    try:
        if not os.path.exists(FILE_STORAGE_PATH):
            return jsonify({'error': 'Storage path not found'}), 404
        
        # 获取所有CSV文件
        files = []
        for filename in os.listdir(FILE_STORAGE_PATH):
            if filename.endswith('.csv'):
                # 解析文件名
                try:
                    category, cancer_type = filename[:-4].split('_', 1)  # 移除.csv后缀并分割
                    files.append({
                        'filename': filename,
                        'category': category,
                        'cancerType': cancer_type,
                        'size': os.path.getsize(os.path.join(FILE_STORAGE_PATH, filename))
                    })
                except ValueError:
                    # 如果文件名不符合预期格式，跳过
                    continue
        
        return jsonify({
            'files': files,
            'total_count': len(files)
        })
        
    except Exception as e:
        print(f"Error in list_available_files: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/CheckFileExists', methods=['POST'])
def check_file_exists():
    """
    可选的API：检查特定文件是否存在
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        category = data.get('category')
        cancer_type = data.get('cancerType')
        
        if not category or not cancer_type:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        filename = f"{category}_{cancer_type}.csv"
        file_path = os.path.join(FILE_STORAGE_PATH, filename)
        
        exists = os.path.exists(file_path)
        size = os.path.getsize(file_path) if exists else 0
        
        return jsonify({
            'exists': exists,
            'filename': filename,
            'size': size
        })
        
    except Exception as e:
        print(f"Error in check_file_exists: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


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
        result['_id'] = str(result['_id'])
    
    return jsonify({'results': result_list, 'total': total})

mutation_path = "/app/EpiSNPdb/src/assets/05.mutation"

@app.route('/api/mutationPng', methods=['GET'])
def get_mutation_png():
    cancertype = request.args.get('Cancertype')
    mutation_x = request.args.get('Mutation_X')
    mutation_y = request.args.get('Mutation_Y')
    
    if not all([cancertype, mutation_x, mutation_y]):
        return abort(400, description="Missing parameters")

    filename = f"{cancertype}_{mutation_x}_{mutation_y}.png"
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

    filename = f"{cancertype}_{mutation_x}_{mutation_y}.pdf"
    file_path = os.path.join(mutation_path, filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return abort(404, description="File not found")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

