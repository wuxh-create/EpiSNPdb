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

input_file_path = '/home/wuxh/SSIdb3/data/04.suivival/all_cancertype_single_recessive_res_add_header_filter_p_0.05_remove_na'
collection_name = 'SingleRecessiveSurvival'  # 在 MongoDB 中显示的表格名称
# 定义导入功能
def import_data(input_file_path):
    insert_count = 0  # 初始化计数器
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # 数据类型转换
            row['Cancertype'] = str(row['Cancertype'])
            row['Model'] = str(row['Model'])
            row['SNP'] = str(row['SNP'])
            row['P_Value'] = float(row['P_Value'])
            row['Sample_Size'] = str(row['Sample_Size'])
            row['OS_Median_AA_Aa'] = float(row['OS_Median_AA_Aa'])
            row['OS_Median_aa'] = float(row['OS_Median_aa'])
            # 数据插入数据库
            db[collection_name].insert_one(row)
            insert_count += 1  # 每插入一条数据，计数器加1
    # 输出插入的数据条数
    print(f"共插入了 {insert_count} 条数据。")
# 创建索引
db[collection_name].create_index([('Cancertype', 1)])
db[collection_name].create_index([('SNP', 1)])
db[collection_name].create_index([('P_Value', 1)])

# 主程序入口
if __name__ == "__main__":
    import_data(input_file_path)
