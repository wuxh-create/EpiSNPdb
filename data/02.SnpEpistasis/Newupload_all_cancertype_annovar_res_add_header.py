from pymongo import MongoClient
from urllib.parse import quote_plus
import csv
import pandas as pd
import numpy as np

# 替换为自己的用户名和密码
username = quote_plus('wuxh')
password = quote_plus('wuxh')

# 创建MongoClient实例并提供认证信息
client = MongoClient(f'mongodb://{username}:{password}@127.0.0.1:30000/wuxh_database', authSource='wuxh_database', authMechanism='SCRAM-SHA-1')
db = client['wuxh_database']  # 数据库名
existing_collections = db.list_collection_names()
print(existing_collections)
# 指明数据的绝对路径和文件名
input_file_path = '/home/wuxh/SSIdb3/data/02.SnpEpistasis/all_cancertype_annovar_res_add_header_add_OR_true_false_add_example_tag.txt'
collection_name = 'NewSnpEpistasisRes'  # 在 MongoDB 中显示的表格名称

def convert_numpy_types(obj):
    """递归转换NumPy类型为Python原生类型"""
    if isinstance(obj, (np.int64, np.int32, np.int16, np.int8)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, np.float16)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return [convert_numpy_types(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(x) for x in obj]
    return obj

# 定义导入功能
def import_data(input_file_path):
    insert_count = 0  # 初始化计数器
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # 数据类型转换
            row['Cancertype'] = str(row['Cancertype'])
            row['SNPepi'] = str(row['SNP_epi'])
            row['SNP1'] = str(row['SNP1'])
            row['Chr1'] = str(row['Chr1'])
            row['pos1'] = int(row['pos1']) 
            row['alleles1'] = str(row['alleles1'])
            row['SNP2'] = str(row['SNP2'])
            row['Chr2'] = str(row['Chr2'])
            row['pos2'] = int(row['pos2']) 
            row['alleles2'] = str(row['alleles2'])

            # 使用 pandas.to_numeric 转换为 float，并处理 NaN
            row['OR_INT'] = pd.to_numeric(row['OR_INT_epistasis'], errors='coerce')
            row['OR_INT'] = round(row['OR_INT'], 4) if not pd.isna(row['OR_INT']) else None

            row['P_epistasis'] = pd.to_numeric(row['P_epistasis'], errors='coerce')
            row['P_saige'] = pd.to_numeric(row['saige_p_epistasis'], errors='coerce')
            row['P_joint'] = pd.to_numeric(row['P_joint'], errors='coerce')
            row['P_boost'] = pd.to_numeric(row['P_boost'], errors='coerce')

            # 将 NaN 替换为 None
            row['P_epistasis'] = None if pd.isna(row['P_epistasis']) else row['P_epistasis']
            row['P_joint'] = None if pd.isna(row['P_joint']) else row['P_joint']
            row['P_boost'] = None if pd.isna(row['P_boost']) else row['P_boost']
            
            row['Best_snp'] = str(row['Best_snp_epistasis'])
            row['IsSPA'] = str(row['IsSPA_boost']).lower() == 'true'
            row['Isepistasis'] = str(row['epistasis']).lower() == 'true'
            row['Isboost'] = str(row['boost']).lower() == 'true'
            row['Isjoint'] = str(row['joint']).lower() == 'true'
            row['ORstatus'] = str(row['X0_0OR']).lower() == 'true'
            row['Type'] = str(row['Type']).lower() == 'true'

            # 转换所有NumPy类型为Python原生类型
            row = convert_numpy_types(row)

            # 数据插入数据库
            db[collection_name].insert_one(row)
            insert_count += 1  # 每插入一条数据，计数器加1

    # 输出插入的数据条数
    print(f"共插入了 {insert_count} 条数据。")

# 创建索引
db[collection_name].create_index([('Cancertype', 1)])
db[collection_name].create_index([('SNP1', 1)])
db[collection_name].create_index([('SNP2', 1)])
db[collection_name].create_index([('P_epistasis', 1)])
db[collection_name].create_index([('ORstatus', 1)])
db[collection_name].create_index([('Type', 1)])

# 主程序入口
if __name__ == "__main__":
    import_data(input_file_path)