from decimal import Decimal
from rpc_con import rpc , rpc_user , rpc_password  
from bitcoinrpc.authproxy import AuthServiceProxy

class BitcoinRegtest:

    def __init__(self):
        self.rpc = rpc
        self.wallet_rpc = None
        self.utxos = None
        self.script_pub_key = None


    def create_wallet(self, wallet_name):
        try:
            result = self.rpc.createwallet(wallet_name)
            print("Wallet created:", result)

        except Exception as e:
            print("Wallet may already exist:", e)


        # connect to wallet RPC endpoint
        self.wallet_rpc = AuthServiceProxy(
            f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/{wallet_name}"
        )


    # fund wallet by mining
    def fund_wallet(self):
        miner_addr = self.wallet_rpc.getnewaddress("", "legacy")

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
    
    def create_segwit_addresses(self):

        A = self.wallet_rpc.getnewaddress("A", "p2sh-segwit")
        B = self.wallet_rpc.getnewaddress("B", "p2sh-segwit")
        C = self.wallet_rpc.getnewaddress("C", "p2sh-segwit")

        print("A:", A)
        print("B:", B)
        print("C:", C)

        return A, B, C


    # send coins from wallet
    def send_to_address(self, address, amount):

        txid = self.wallet_rpc.sendtoaddress(address, amount)

        # confirm transaction
        self.rpc.generatetoaddress(1, self.wallet_rpc.getnewaddress())

        return txid


    # get wallet balance
    def get_balance(self):
        balance = self.wallet_rpc.getbalance()
        print("Wallet Balance:", balance)

        return balance

    # list utxos of address
    def list_utxos(self, address):
        self.utxos = self.wallet_rpc.listunspent(1, 9999999, [address])

        return self.utxos
    
    #get address balance
    def get_address_balance(self, address):
        self.utxos = self.list_utxos(address)
        balance = sum([u["amount"] for u in self.utxos])
        print(f"Balance of {address}: {balance}")

        return balance
    

    def create_raw_transaction(self,sender_addr, receiver_addr, send_amount, fee):
        fee = Decimal(str(fee))
        self.utxos = self.list_utxos(sender_addr)
        utxo = self.utxos[0]
        txid = utxo["txid"]
        vout = utxo["vout"]
        utxo_amount = utxo["amount"]
        # input UTXO
        inputs = [{
            "txid": txid,
            "vout": vout
        }]

        # calculate change
        if(utxo_amount < send_amount + fee):
            raise Exception("Insufficient funds")
        else:
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