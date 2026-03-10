# CS-216-Chain_Snatcher-Bitcoin-Transaction-simulation

## Team Information
* **Team Member 1:** Managari Saatvik - 240002035
* **Team Member 2:** Nagalla AbhiSri Karthik - 240002041
* **Team Member 3:** Nemani Sandeep - 240002044
* **Team Member 4:** Malladi Charan - 240008016

## Pre-Requisites:
* Bitcoin Core (bitcoind version > 27.0 & bitcoin-cli) 
* Python (version>3.8)
* Libraries: Bitcoinrpc
* Bitcoin Debugger: btcdeb

## Initialization

### Configuration

We first set up Bitcoin Core using the setup wizard and edited the configuration file to meet the project's requirements. 

```json
regtest=1
server=1
txindex=1

[regtest]
rpcuser=bitcoinrpc
rpcpassword=chainsnatcher1
rpcallowip=127.0.0.1
rpcport=18443

debug=validation

paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
```

Once this is done, we can start with the making of the required transaction

### Setup

* Run the bitcoind in regtest mode using ```bitcoind -regtest```
* Establish RPC connection with Python file
* Create a wallet and connect via the RPC
* Fund the Wallet by mining 101 Blocks (Standard) generating 50 BTC

## Part 1: Legacy Transaction

### Workflow: 

* Generate 3 Different Legacy Address naming them A, B and C
* Fund the address A through the wallet
* Create a transaction using a UTXO addressed to A, send some amount of BTC to Address B from A
* Decode the transaction and retrieve ScriptPubKey
* Sign the transaction with the sender's Public Key and broadcast it to the network
* The transaction is confirmed when a block is mined
* Repeat the same workflow to generate a transaction from B to C, from the previously generated UTXO at Address B
* Using the tx_id of the transaction, retrieve the hex of the transaction (transaction condensed into hexadecimal format)
* Decode this hex using ```deciderawtransaction``` which turns the hex into a readable JSON Script, from which we extract the ScriptSig

### Script Analysis

* Using the btcdeb, we verify the transaction's validity
* We are using ```./btcdeb <ScriptSig> <ScriptPubKey>```

**ScriptSig:** ```Signature[ALL] Pubkey```

**ScriptPubKey:** ```OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG```

#### Script Execution using btcdeb

The Entire Execution takes place using a stack-based execution process : 

* Initial stack -> []
* Push Signature -> [Sig]
* Push PubKey -> [Sig, PubKey]
* OP_DUP -> [Sig, PubKey, PubKey]
* OP_HASH160 -> [Sig, PubKey, HASH160(PubKey)]
* Push PubKeyHash -> [Sig, PubKey, HASH160(PubKey), PubKeyHash]
* OP_EQUALVERIFY -> [Sig, PubKey]
* OP_CHECKSIG -> [TRUE]


## Part 2: SegWit Transaction

### Workflow:

* Generate 3 Different SegWit Address naming them A, B and C
* Fund the address A through the wallet
* Create a transaction using a UTXO addressed to A, send some amount of BTC to Address B from A
* Decode the transaction and retrieve ScriptPubKey
* Sign the transaction with the sender's Public Key and broadcast it to the network
* The transaction is confirmed when a block is mined
* Repeat the same workflow to generate a transaction from B to C, from the previously generated UTXO at Address B
* Using the tx_id of the transaction, retrieve the hex of the transaction (transaction condensed into hexadecimal format)
* Decode this hex using decoderawtransaction which turns the hex into a readable JSON Script, from which we extract the ScriptSig, ScriptPubKey and Witness data

### Script Analysis

* Using the btcdeb, we verify the transaction's validity
* We are using ```./btcdeb <Witness> <RedeemScript / ScriptPubKey>``` 

**Witness:**  ```Signature[ALL] Pubkey```

**ScriptSig:**  ```0 <20-byte-pubkey-hash>```

**ScriptPubKey:**  ```OP_HASH160 <20-byte-script-hash> OP_EQUAL```

**RedeemScript:**  ```0 <20-byte-pubkey-hash>```

#### Script Execution using btcdeb

The Entire Execution takes place using a stack-based execution process :

* Initial stack -> []
* Push Signature -> [Sig]
* Push PubKey -> [Sig, PubKey]
* Push 0 (from RedeemScript) -> [Sig, PubKey, 0]
* Push PubKeyHash -> [Sig, PubKey, 0, PubKeyHash]
* OP_HASH160 -> [Sig, PubKey, HASH160(RedeemScript)]
* Push ScriptHash -> [Sig, PubKey, HASH160(RedeemScript), ScriptHash]
* OP_EQUAL -> [Sig, PubKey]
* OP_DUP -> [Sig, PubKey, PubKey]
* OP_HASH160 -> [Sig, PubKey, HASH160(PubKey)]
* Push PubKeyHash -> [Sig, PubKey, HASH160(PubKey), PubKeyHash]
* OP_EQUALVERIFY -> [Sig, PubKey]
* OP_CHECKSIG -> [TRUE]





