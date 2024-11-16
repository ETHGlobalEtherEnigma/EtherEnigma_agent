from cdp import *
import os

# Get configuration from environment variables
API_KEY_NAME = os.environ.get("CDP_API_KEY_NAME")
PRIVATE_KEY = os.environ.get("CDP_PRIVATE_KEY", "").replace('\\n', '\n')

# Configure CDP with environment variables
Cdp.configure(API_KEY_NAME, PRIVATE_KEY)

agent_wallet = Wallet.create()
wallet_data = agent_wallet.export_data()
wallet_dict = wallet_data.to_dict()
file_path = "wallet_seed.json"
agent_wallet.save_seed(file_path, encrypt=True)
print(agent_wallet.id)

fetched_wallet = Wallet.fetch(agent_wallet.id)
fetched_wallet.load_seed("wallet_seed.json")
fetched_wallet.faucet()