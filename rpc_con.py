from bitcoinrpc.authproxy import AuthServiceProxy
from pprint import pprint
import logging

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)


rpc_user = "charan"
rpc_password = "123charan"

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443" , timeout=120)
