import json
import os
from cdp import Wallet

# 定义存储钱包种子和ID的文件路径
file_path = "wallet_seed.json"

if os.path.exists(file_path):
    # 如果文件存在，加载已保存的钱包数据
    with open(file_path, 'r') as f:
        wallet_dict = json.load(f)
    
    wallet_id = wallet_dict.get('wallet_id')
    if wallet_id:
        # 根据钱包ID获取钱包
        agent_wallet = Wallet.fetch(wallet_id)
        # 从文件中加载种子
        agent_wallet.load_seed(file_path)
        print(f"已加载现有钱包，钱包ID为: {agent_wallet.id}")
    else:
        print("在保存的数据中未找到钱包ID。")
else:
    # 如果文件不存在，创建一个新钱包
    agent_wallet = Wallet.create()
    # 导出钱包数据（包含种子和钱包ID）
    wallet_data = agent_wallet.export_data()
    wallet_dict = wallet_data.to_dict()
    # 将钱包数据保存到文件
    with open(file_path, 'w') as f:
        json.dump(wallet_dict, f)
    print(f"已创建新钱包，钱包ID为: {agent_wallet.id}，并已保存到 {file_path}")
