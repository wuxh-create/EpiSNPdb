from pymongo import MongoClient
from urllib.parse import quote_plus
import csv

# 替换为自己的用户名和密码
username = quote_plus('wuxh')
password = quote_plus('wuxh')

# 创建MongoClient实例并提供认证信息
client = MongoClient(f'mongodb://{username}:{password}@127.0.0.1:30000/wuxh_database', authSource='wuxh_database', authMechanism='SCRAM-SHA-1')
db = client['wuxh_database']  # 数据库名

# 检查 MongoDB 中已有的集合名称，防止重名
existing_collections = db.list_collection_names()
print("现有集合:", existing_collections)

# # 删除所有已有的集合（可选）
# for collection_name in existing_collections:
#     db[collection_name].drop()
#     print(f"已删除集合：{collection_name}")

# 指明数据的绝对路径和文件名
input_file_path = '/home/wuxh/EpiSNPdb/data/06.Genecor/CorResultFinal2'  # 请替换为您的实际文件路径
collection_name = 'GeneCor'  # 在 MongoDB 中显示的表格名称

# 定义导入功能
def import_gene_correlation_data(input_file_path):
    insert_count = 0  # 初始化计数器
    error_count = 0   # 错误计数器
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            
            for row_num, row in enumerate(reader, start=2):  # 从第2行开始计数（考虑header）
                try:
                    # 基础字符串字段处理
                    processed_row = {
                        'Cancertype': str(row['Cancertype']).strip(),
                        'Gene1': str(row['Gene.refGene1']).strip(),
                        'Gene2': str(row['Gene.refGene2']).strip(),
                    }
                    
                    # correlation字段处理（可能包含NA）
                    corr_value = str(row['cor_spearman_format']).strip()
                    if corr_value == 'NA':
                        processed_row['correlation'] = 'NA'
                    elif corr_value:
                        processed_row['correlation'] = float(corr_value)
                    else:
                        processed_row['correlation'] = None
                    
                    # P_value字段处理（可能包含NA）
                    pvalue_value = str(row['pvalue_spearman_format']).strip()
                    if pvalue_value == 'NA':
                        processed_row['P_value'] = 'NA'
                    elif pvalue_value:
                        processed_row['P_value'] = float(pvalue_value)
                    else:
                        processed_row['P_value'] = None
                    
                    # coexpression字段处理
                    coexp_value = str(row['coexpression']).strip()
                    if coexp_value == 'NA':
                        processed_row['coexpression'] = 'NA'
                    elif coexp_value:
                        processed_row['coexpression'] = coexp_value
                    else:
                        processed_row['coexpression'] = None
                    
                    # textmining_transferred字段处理
                    textmining_value = str(row['textmining_transferred']).strip()
                    if textmining_value == 'NA':
                        processed_row['textmining_transferred'] = 'NA'
                    elif textmining_value:
                        processed_row['textmining_transferred'] = float(textmining_value)
                    else:
                        processed_row['textmining_transferred'] = None
                    
                    # combined_score字段处理
                    combined_value = str(row['combined_score']).strip()
                    if combined_value == 'NA':
                        processed_row['combined_score'] = 'NA'
                    elif combined_value:
                        processed_row['combined_score'] = float(combined_value)
                    else:
                        processed_row['combined_score'] = None
                    
                    # 添加Type字段用于首次加载筛选（可根据需要调整逻辑）
                    # 这里假设某些特定条件的数据设为True，用于首次加载展示
                    type_value = str(row['Type']).strip().lower()
                    processed_row['Type'] = type_value == 'true'
                    
                    # 数据插入数据库
                    db[collection_name].insert_one(processed_row)
                    insert_count += 1  # 每插入一条数据，计数器加1
                    
                    # 每1000条数据输出一次进度
                    if insert_count % 1000 == 0:
                        print(f"已插入 {insert_count} 条数据...")
                        
                except ValueError as ve:
                    error_count += 1
                    print(f"第{row_num}行数据转换错误: {ve}")
                    continue
                except KeyError as ke:
                    error_count += 1
                    print(f"第{row_num}行缺少必要字段: {ke}")
                    continue
                except Exception as e:
                    error_count += 1
                    print(f"第{row_num}行处理出错: {e}")
                    continue
    
    except FileNotFoundError:
        print(f"文件未找到: {input_file_path}")
        return
    except Exception as e:
        print(f"文件读取错误: {e}")
        return
    
    # 输出插入的数据条数
    print(f"数据导入完成！")
    print(f"成功插入: {insert_count} 条数据")
    print(f"错误记录: {error_count} 条数据")

# 创建索引
def create_indexes():
    print("正在创建索引...")
    
    # 为指定字段创建索引
    db[collection_name].create_index([('Cancertype', 1)])
    db[collection_name].create_index([('Gene1', 1)])
    db[collection_name].create_index([('Gene2', 1)])
    db[collection_name].create_index([('correlation', 1)])
    db[collection_name].create_index([('P_value', 1)])
    
    # 创建复合索引以提高查询效率
    db[collection_name].create_index([('Cancertype', 1), ('Gene1', 1)])
    db[collection_name].create_index([('Cancertype', 1), ('Gene2', 1)])
    db[collection_name].create_index([('Gene1', 1), ('Gene2', 1)])
    db[collection_name].create_index([('correlation', -1), ('P_value', 1)])  # 按相关性降序，P值升序
    db[collection_name].create_index([('Type', 1)])  # 用于首次加载筛选
    
    print("索引创建完成！")

# 验证导入数据
def verify_import():
    print("\n=== 数据验证 ===")
    total_count = db[collection_name].count_documents({})
    print(f"总记录数: {total_count}")
    
    # 验证各癌症类型的数据量
    pipeline = [
        {"$group": {"_id": "$Cancertype", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    cancer_stats = list(db[collection_name].aggregate(pipeline))
    print("\n各癌症类型数据量:")
    for stat in cancer_stats:
        print(f"  {stat['_id']}: {stat['count']} 条记录")
    
    # 查看样本数据
    sample_data = list(db[collection_name].find({}).limit(3))
    print(f"\n样本数据 (前3条):")
    for i, doc in enumerate(sample_data, 1):
        doc.pop('_id', None)  # 移除_id字段以便于查看
        print(f"  记录{i}: {doc}")

# 主程序入口
if __name__ == "__main__":
    print("开始导入Gene Correlation数据...")
    
    # 导入数据
    import_gene_correlation_data(input_file_path)
    
    # 创建索引
    create_indexes()
    
    # 验证导入结果
    verify_import()
    
    print("\n程序执行完成！")
