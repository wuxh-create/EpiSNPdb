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
print(existing_collections)
# # 删除所有已有的集合
# for collection_name in existing_collections:
#     db[collection_name].drop()
#     print(f"已删除集合：{collection_name}")
# 指明数据的绝对路径和文件名
input_file_path = '/home/wuxh/SSIdb3/data/04.suivival/two_recessive_res_add_header_filter_p_0.05_remove_na'
collection_name = 'TwoRecessiveSurvival'  # 在 MongoDB 中显示的表格名称
# 定义导入功能
def import_data(input_file_path, collection_name):
    insert_count = 0  # 初始化计数器
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # 只选择和转换感兴趣的列
            document = {
                'Cancertype': row['Cancertype'],  # 假设不需要转换
                'Model': row['Model'],            # 同上
                'SNP_epi': row['SNP'],
                'SNP1': row['SNP1'],
                'SNP2': row['SNP2'],               
                'P_Value': float(row['P_Value']), # 转换为浮点数
                'N': int(row['N']),              # 转换为整数
                # 只添加感兴趣的中位生存期数据，并转换为浮点数
                'OS_Median_aabb': float(row['Median_OS_2_2']),
                'OS_Median_aaBB_and_aaBb': float(row['Median_OS_2_01']),
                'OS_Median_AAbb_and_Aabb': float(row['Median_OS_01_2']),
                'OS_Median_AABB_AABb_AaBB_and_AaBb': float(row['Median_OS_01_01']),
            }

            # 数据插入数据库
            db[collection_name].insert_one(document)
            insert_count += 1  # 每插入一条数据，计数器加1

    print(f"共插入了 {insert_count} 条数据。")
    
if collection_name not in existing_collections:
    db.create_collection(collection_name)
db[collection_name].create_index([('Cancertype', 1)])
db[collection_name].create_index([('SNP', 1)])
db[collection_name].create_index([('P_Value', 1)])  # 确保使用正确的字段名


# 主程序入口
if __name__ == "__main__":
    # 确保传递两个参数给import_data函数
    import_data(input_file_path, collection_name)
