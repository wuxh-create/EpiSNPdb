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
input_file_path = '/home/wuxh/SSIdb3/data/05.mutation/mutation_res'
collection_name = 'MutationRes'  # 在 MongoDB 中显示的表格名称
# 定义导入功能
def import_data(input_file_path, collection_name):
    insert_count = 0  # 初始化计数器
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # 只选择和转换感兴趣的列
            document = {
                'Cancertype': row['Cancer_Type'],  # 假设不需要转换
                'Mutation_X': row['Mutation_X'],            # 同上
                'Gene_X': row['Gene_X'],               # 同上
                'Mutation_Y': row['Mutation_Y'],
                'Gene_Y': row['Gene_Y'],
                'Cor_Type': row['Cor_Type'],
                'OR': float(row['Odds_Ratio']), # 转换为浮点数
                'Pvalue': float(row['Pvalue']),
                'Mutated_XY': int(row['Mutated_XY']),  
                'Mutated_X': int(row['Mutated_X']), 
                'Mutated_Y': int(row['Mutated_Y']), 
                'No_Mutated': int(row['No_Mutated']),              
            }
            # 数据插入数据库
            db[collection_name].insert_one(document)
            insert_count += 1  # 每插入一条数据，计数器加1
    # 输出插入的数据条数
    print(f"共插入了 {insert_count} 条数据。")

# 创建索引
db[collection_name].create_index([('Cancertype', 1)])
db[collection_name].create_index([('Mutation_X', 1)])
db[collection_name].create_index([('Mutation_Y', 1)])
db[collection_name].create_index([('Pvalue', 1)])

# 主程序入口
if __name__ == "__main__":
    # 确保传递两个参数给import_data函数
    import_data(input_file_path, collection_name)
