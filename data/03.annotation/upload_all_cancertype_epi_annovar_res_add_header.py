from pymongo import MongoClient
from urllib.parse import quote_plus
import csv
import pandas as pd
import numpy as np  # 导入 numpy 以检查类型

# 替换为自己的用户名和密码
username = quote_plus('wuxh')
password = quote_plus('wuxh')
# 创建MongoClient实例并提供认证信息
client = MongoClient(f'mongodb://{username}:{password}@127.0.0.1:30000/wuxh_database', 
    authSource='wuxh_database', authMechanism='SCRAM-SHA-1')
db = client['wuxh_database']  # 数据库名
# 检查 MongoDB 中已有的集合名称，防止重名
existing_collections = db.list_collection_names()
print(existing_collections)

# 指明数据的绝对路径和文件名
input_file_path = '/home/wuxh/EpiSNPdb/data/03.annotation/New_all_combine_score_epi.txt'
collection_name = 'SnpEpistasisAnnovar'  # 在 MongoDB 中显示的表格名称

# 定义一个函数来安全地转换 NumPy 类型
def convert_value(value):
    if isinstance(value, (np.float64, np.float32)):
        return float(value)
    elif isinstance(value, (np.int64, np.int32)):
        return int(value)
    else:
        return value

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
            row['SNP2'] = str(row['SNP2'])

            # 转换数值类型并处理 NaN
            row['OR_INT'] = pd.to_numeric(row['OR_INT_epistasis'], errors='coerce')
            row['OR_INT'] = round(float(row['OR_INT']), 4) if not pd.isna(row['OR_INT']) else None
            
            # 使用 convert_value 函数处理其他数值字段
            row['P_epistasis'] = convert_value(pd.to_numeric(row['P_epistasis'], errors='coerce'))
            row['P_saige'] = convert_value(pd.to_numeric(row['P_saige'], errors='coerce'))
            row['P_joint'] = convert_value(pd.to_numeric(row['P_joint'], errors='coerce'))
            row['P_boost'] = convert_value(pd.to_numeric(row['P_boost'], errors='coerce'))
            
            # 将 NaN 替换为 None
            row['P_epistasis'] = None if pd.isna(row['P_epistasis']) else float(row['P_epistasis'])
            row['P_joint'] = None if pd.isna(row['P_joint']) else float(row['P_joint'])
            row['P_boost'] = None if pd.isna(row['P_boost']) else float(row['P_boost'])
            row['P_saige'] = None if pd.isna(row['P_saige']) else float(row['P_saige'])

            row['FuncrefGene1'] = str(row['Func.refGene1'])
            row['GenerefGene1'] = str(row['Gene.refGene1'])
            row['ExonicFuncrefGene1'] = str(row['ExonicFunc.refGene1'])
            row['AAChangerefGene1'] = str(row['AAChange.refGen1'])

            row['FuncrefGene2'] = str(row['Func.refGene2'])
            row['GenerefGene2'] = str(row['Gene.refGene2'])
            row['ExonicFuncrefGene2'] = str(row['ExonicFunc.refGene2'])
            row['AAChangerefGene2'] = str(row['AAChange.refGen2'])

            row['coexpression'] = str(row['coexpression'])
            row['textmining_transferred'] = str(row['textmining_transferred'])
            row['combined_score'] = str(row['combined_score'])

            # 确保所有值都是 MongoDB 可序列化的类型
            processed_row = {k: convert_value(v) for k, v in row.items()}
            
            # 数据插入数据库
            db[collection_name].insert_one(processed_row)
            insert_count += 1  # 每插入一条数据，计数器加1
    # 输出插入的数据条数
    print(f"共插入了 {insert_count} 条数据。")

# 创建索引
db[collection_name].create_index([('Cancertype', 1)])
db[collection_name].create_index([('SNP1', 1)])
db[collection_name].create_index([('SNP2', 1)])
db[collection_name].create_index([('P_epistasis', 1)])
db[collection_name].create_index([('SNPepi', 1)])

# 主程序入口
if __name__ == "__main__":
    import_data(input_file_path)