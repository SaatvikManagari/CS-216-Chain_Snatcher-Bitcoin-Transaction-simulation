from rpc_con import rpc , rpc_user , rpc_password , rpc_port 
from bitcoinrpc.authproxy import AuthServiceProxy

class BitcoinRegtest:

    def __init__(self):
        self.rpc = rpc
        self.wallet_rpc = None


    def create_wallet(self, wallet_name):
        try:
            result = self.rpc.createwallet(wallet_name)
            print("Wallet created:", result)

        except Exception as e:
            print("Wallet may already exist:", e)

        # connect to wallet RPC endpoint
        self.wallet_rpc = AuthServiceProxy(
            f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
        )


    # fund wallet by mining
    def fund_wallet(self):
        miner_addr = self.wallet_rpc.getnewaddress("", "legacy")
        print("Mining to:", miner_addr)

        self.rpc.generatetoaddress(101, miner_addr)
        print("Wallet Balance:", self.wallet_rpc.getbalance())


    # create legacy addresses
    def create_legacy_addresses(self):

        A = self.wallet_rpc.getnewaddress("A", "legacy")
        B = self.wallet_rpc.getnewaddress("B", "legacy")
        C = self.wallet_rpc.getnewaddress("C", "legacy")

        print("A:", A)
        print("B:", B)
        print("C:", C)

        return A, B, C


    # send coins from wallet
    def send_to_address(self, address, amount):

        txid = self.wallet_rpc.sendtoaddress(address, amount)
        print("Transaction sent:", txid)

        return txid


    # get wallet balance
    def get_balance(self):
        balance = self.wallet_rpc.getbalance()
        print("Wallet Balance:", balance)

        return balance


    # list utxos of address
    def list_utxos(self, address):
        utxos = self.wallet_rpc.listunspent(1, 9999999, [address])
        print("UTXOs:")

        for u in utxos:
            print(u)

        return utxos
    
    utxos = list_utxos("A")
    utxo = utxos[0]
    txid = utxo["txid"]
    vout = utxo["vout"]
    amount = utxo["amount"]

    
    def create_raw_transaction(self, txid, vout, sender_addr, receiver_addr, utxo_amount, send_amount, fee):

        # input UTXO
        inputs = [{
            "txid": txid,
            "vout": vout
        }]

        # calculate change
        change = utxo_amount - send_amount - fee

        outputs = {
            receiver_addr: send_amount,
            sender_addr: change
        }

        raw_tx = self.rpc.createrawtransaction(inputs, outputs)

        print("Raw Transaction:", raw_tx)

        return raw_tx


    # decode raw transaction
    def decode_transaction(self, raw_tx):

        decoded = self.rpc.decoderawtransaction(raw_tx)

        print("\nDecoded Transaction")

        for vout in decoded["vout"]:
            print("Value:", vout["value"])
            print("ScriptPubKey:", vout["scriptPubKey"])

        return decoded


    # sign transaction
    def sign_transaction(self, raw_tx):
        signed = self.wallet_rpc.signrawtransactionwithwallet(raw_tx)
        print("Signed TX:", signed["hex"])

        return signed["hex"]


    # broadcast transaction
    def broadcast_transaction(self, signed_tx):
        txid = self.rpc.sendrawtransaction(signed_tx)
        print("Broadcasted TXID:", txid)

        return txid