from main import BitcoinRegtest 
from bitcoinrpc.authproxy import AuthServiceProxy

btc = BitcoinRegtest()

#Part 1:
#Setup and Fund Wallet by Mining s

btc.create_wallet('btcwallet')
btc.fund_wallet()

# print(btc.wallet_rpc.listwallets())
# print(btc.wallet_rpc.getbalance())
# print(btc.wallet_rpc.getbalances())
# print(btc.wallet_rpc.getblockcount())

#create legacy addresses
A, B , C = btc.create_legacy_addresses()

#Sending 50 BTC fromw wallet to A 
tx0 = btc.send_to_address(A, 40)
print("Transaction ID for funding A:", tx0)

#Crosschecking where the transaction is successful by checking the balance of A
A_Bal = btc.get_address_balance(A)
if A_Bal != 40:
    print("Error: A balance is incorrect")
else:  
    print("A balance is correct , Transaction successful")
B_Bal = btc.get_address_balance(B)
C_Bal = btc.get_address_balance(C)
print("Balance of A:", A_Bal)
print("Balance of B:", B_Bal)
print("Balance of C:", C_Bal)

print("-------------------------------------------------------------------------------")

#Part 2: Creating and Broadcasting a Raw Transaction
#sending half of the total BTC from A to B
raw_tx_hex = btc.create_raw_transaction(A, B, A_Bal/2, 0.0001) 

#decoding the transaction above to get ScriptPubKey of the output
decoded_tx = btc.wallet_rpc.decoderawtransaction(raw_tx_hex)

#signing the transaction
signed_tx = btc.wallet_rpc.signrawtransactionwithwallet(raw_tx_hex)

#broadcasting the transaction
txid = btc.wallet_rpc.sendrawtransaction(signed_tx["hex"])
btc.wallet_rpc.generatetoaddress(1, A)

#checking the balance of B to confirm the transaction is successful
B_bal = btc.get_address_balance(B) 
if B_bal != A_Bal/2:
    print("Error: B balance is incorrect , Trsansaction failed")
else:  
    print("Transaction successful")

A_bal = btc.get_address_balance(A)
C_bal = btc.get_address_balance(C)
print("Balance of A:", A_bal)
print("Balance of B:", B_bal)
print("Balance of C:", C_bal)

print("--------------------------------------------------------------------------------")

#Part 3: Spending the UTXO received by B to C
#checking the UTXO sent by A to B
utxos_B = btc.list_utxos(B)
if len(utxos_B) != 1:
    print("Error: UTXO count for B is incorrect")
else:    
    print("UTXO count for B is correct")

raw_tx_hex_2 = btc.create_raw_transaction(B, C, B_bal/2, 0.0001)

#decoding the transaction above to get ScriptPubKey of the output
decoded_tx_2 = btc.wallet_rpc.decoderawtransaction(raw_tx_hex_2)

#signing the transaction
signed_tx_2 = btc.wallet_rpc.signrawtransactionwithwallet(raw_tx_hex_2)

#broadcasting the transaction
txid_2 = btc.wallet_rpc.sendrawtransaction(signed_tx_2["hex"])
btc.wallet_rpc.generatetoaddress(1,B)

print("----------------------------------------------------------------------------------")

# Get the wallet transaction of B spending the UTXO
wallet_tx = btc.rpc.gettransaction(txid_2)

# Decode it to get vin/vout
decoded_spending_tx = btc.rpc.decoderawtransaction(wallet_tx["hex"])

# ScriptSig of input (from B)
scriptSig_response = decoded_spending_tx["vin"][0]["scriptSig"]["asm"]

# Previous transaction (A->B) info from wallet
prev_tx_wallet = btc.rpc.gettransaction(decoded_spending_tx["vin"][0]["txid"])
prev_tx = btc.rpc.decoderawtransaction(prev_tx_wallet["hex"])

# ScriptPubKey (challenge script from A->B)
prev_vout = decoded_spending_tx["vin"][0]["vout"]
challenge_script = prev_tx["vout"][prev_vout]["scriptPubKey"]["asm"]

print("----------------------------- Decoded Scripts ---------------------------------------")
print("Transaction from A -> B : " , prev_tx)
print("Transaction from B -> C : " , decoded_spending_tx)

print("------------------------------ Transaction IDs ----------------------------------------")

print("Transaction TD from A -> B : " , txid)
print("Transaction ID from B -> C : " , decoded_spending_tx["txid"])

print("----------------------------- Required Details -------------------------------------")

print("Transaction ID for B -> C:", txid_2)
print("ScriptSig (response provided by B):", scriptSig_response)
print("Challenge Script (ScriptPubKey from A->B tx):", challenge_script)

print("-----------------------------Transaction Sizes----------------------------------")

print(" A->B Transaction" )
print("Transaction Size :" , decoded_spending_tx["size"]  )
print("Transaction Virtual size:", decoded_spending_tx["vsize"] )
print("Transaction Weight:",decoded_spending_tx["weight"] )
print("Transaction Size (in bytes):" , len(prev_tx_wallet["hex"])/2  ) 

print(" B->C Transaction" )
print("Transaction Size :" , decoded_spending_tx["size"]  )
print("Transaction Virtual size:", decoded_spending_tx["vsize"] )
print("Transaction Weight:",decoded_spending_tx["weight"] )
print("Transaction Size (in bytes):" , len(wallet_tx["hex"])/2  ) 

print("----------------------------- Final Balances ---------------------------------------")

a_bal = btc.get_address_balance(A)
b_bal = btc.get_address_balance(B)
c_bal = btc.get_address_balance(C)
print("Balance of A:", a_bal)
print("Balance of B:", b_bal) 
print("Balance of C:", c_bal)

btc.rpc.unloadwallet("btcwallet")
print("btcwallet unloaded")