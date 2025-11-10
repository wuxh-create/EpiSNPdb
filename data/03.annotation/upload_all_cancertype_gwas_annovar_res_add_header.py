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
input_file_path = '/home/wuxh/SSIdb3/data/03.annotation/all_cancertype_gwas_annovar_res_add_header_order'
collection_name = 'SnpGwasAnnovar'  # 在 MongoDB 中显示的表格名称
# 定义导入功能
def import_data(input_file_path):
    insert_count = 0  # 初始化计数器
    with open(input_file_path, 'r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            # 数据类型转换
            row['Cancertype'] = str(row['Cancertype'])
            row['SNP'] = str(row['SNP'])
            row['Pos'] = str(row['Pos'])
            row['POS'] = int(row['POS'])
            row['alleles'] = str(row['alleles'])
            row['P'] = float(row['P'])
            row['BETA'] = float(row['BETA'])
            row['FuncrefGene'] = str(row['Func.refGene'])
            row['GenerefGene'] = str(row['Gene.refGene'])
            row['ExonicFuncrefGene'] = str(row['ExonicFunc.refGene'])
            row['AAChangerefGene'] = str(row['AAChange.refGen'])
            
            row['Type'] = str(row['Type']).lower() == 'true'

            # 数据插入数据库
            db[collection_name].insert_one(row)
            insert_count += 1  # 每插入一条数据，计数器加1
    # 输出插入的数据条数
    print(f"共插入了 {insert_count} 条数据。")
# 创建索引
db[collection_name].create_index([('Cancertype', 1)])
db[collection_name].create_index([('SNP', 1)])
db[collection_name].create_index([('P', 1)])
db[collection_name].create_index([('Type', 1)])


# 主程序入口
if __name__ == "__main__":
    import_data(input_file_path)
