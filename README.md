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

* The wallet first sends 40 BTC to address A to fund it.
* A raw transaction is then created to send half of A's balance to address B.
* This transaction is signed and broadcast to the network, producing the transaction ID (txid) for the A → B transaction.
* The output of this transaction becomes a UTXO belonging to address B.
* The program retrieves this UTXO using listunspent.
* The retrieved UTXO contains the txid and output index (vout) of the A → B transaction.
* This UTXO is then used as the input for the next raw transaction, where B sends funds to address C.
* When the B → C transaction is decoded, the previous transaction ID is obtained using: ```decoded_spending_tx["vin"][0]["txid"]```
* This value corresponds to the A → B transaction ID, demonstrating that the B → C transaction spends the output created in the previous transaction.

### Script Analysis

* Using the btcdeb, we verify the transaction's validity
* We are using ```./btcdeb <ScriptSig> <ScriptPubKey>```

1. Locking Script Creation (ScriptPubKey)
   
When A sends BTC to B, the output contains a ScriptPubKey.

Structure:

```OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG```
```<PubKeyHash>```-> is the hash of B’s public key.

This acts as the challenge script defining the conditions to spend the output.

2. Unlocking Script Creation (ScriptSig)
   
When B spends the output (B → C), the input contains a ScriptSig.

Structure:

```<signature> <public_key>```
The signature proves ownership of the private key corresponding to the public key.

3. Transaction Linking
   
The B → C transaction input references the previous transaction using:
```txid```-> ID of the A → B transaction
```vout```-> index of the output being spent

#### Script Execution using btcdeb

The entire execution takes place using a stack-based execution process : 

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

* The wallet first sends 40 BTC to address A to fund it.
* A raw transaction is then created to send half of A's balance to address B.
* This transaction is signed and broadcast to the network, producing the transaction ID (txid) for the A → B transaction.
* The output of this transaction becomes a UTXO belonging to address B.
* The program retrieves this UTXO using listunspent.
* The retrieved UTXO contains the txid and output index (vout) of the A → B transaction.
* This UTXO is then used as the input for the next raw transaction, where B sends funds to address C.
* When the B → C transaction is decoded, the previous transaction ID is obtained using:  ```decoded_spending_tx["vin"][0]["txid"]```
* This value corresponds to the A → B transaction ID, demonstrating that the B → C transaction spends the output created in the previous transaction.

### Script Analysis

* Using the btcdeb, we verify the transaction's validity
* We are using ```./btcdeb <Witness> <RedeemScript / ScriptPubKey>``` 

1. Locking Script Creation (ScriptPubKey)

When A sends BTC to B using a SegWit address, the output contains a P2SH ScriptPubKey.

Structure:

```OP_HASH160 <RedeemScriptHash> OP_EQUAL```
```<RedeemScriptHash>```-> is the HASH160 of the redeem script.

The redeem script corresponds to the SegWit witness program.

2. Redeem Script(Witness Program)

The redeem script embedded inside P2SH is:

```0 <PubKeyHash>```

0-> SegWit version number.

```<PubKeyHash>```-> HASH160 of B's public key.

This script tells Bitcoin that the actual unlocking data will be stored in the witness field.

3. Unlocking Script (ScriptSig)

For P2SH-P2WPKH, the ScriptSig contains only the redeem script:

```<redeem_script>```

Example:

```0 <PubKeyHash>```

So ScriptSig is much smaller than legacy ScriptSig.

4. Witness Data(txinwitness)

The actual unlocking data is placed in the witness field instead of ScriptSig.

Witness structure:

```<signature>```
```<public_key>```

This is similar to the legacy ScriptSig, but moved into the witness.

5. Transaction Linking

The B->C transaction input references the previous output using:

```txid``` → transaction ID of A → B

```vout``` → output index

This output becomes the input for the next transaction.

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

  ## Part 3: Analysis and Explanation

 ### Comparison of P2PKH (Legacy) and P2SH-P2WPKH (SegWit) Transactions
 
##### 1. Size comparison of P2PKH and P2SH-P2WPKH transactions

The transaction size was obtained using:
```bitcoin-cli -regtest getrawtransaction <txid> true```

The important fields observed were size, vsize and weight.

 | Metric | P2PKH (Legacy) | P2SH-P2WPKH (SegWit) |
|--------|---------------|----------------------|
| Size (bytes) | 225 | 247 |
| Virtual Size (vbytes) | 225 | 166 |
| Weight | 900 | 661 |
| Fee | Higher | Lower |

The SegWit transaction has smaller virtual size and weight compared to the Legacy transaction.

#### 2. Script structure comparison (challenge-response script)
   
| Feature | P2PKH (Legacy) | P2SH-P2WPKH (SegWit) |
|---------|---------------|----------------------|
| ScriptPubKey | `OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG` | `OP_HASH160 <ScriptHash> OP_EQUAL` |
| scriptSig | `Signature PubKey` | `0 <PubKeyHash>` |
| RedeemScript | Not used | `0 <PubKeyHash>` |
| Witness | Not present | `Signature PubKey` |
| Validation | `scriptSig + scriptPubKey` | `scriptSig + scriptPubKey + redeemScript + witness` |
| Script result | TRUE | TRUE |

* In P2PKH, the signature and public key are stored in scriptSig.
* In P2SH-P2WPKH, the signature and public key are stored in the witness, and scriptSig only contains the redeemScript.

#### 3. Why SegWit transactions are smaller?

* SegWit transactions are smaller because the signature data is separated from the main transaction and stored in the witness field.
* In Legacy transactions, the signature and public key are stored in scriptSig, and the entire scriptSig is counted fully in the transaction size.
* In SegWit transactions,the Signature data is moved from scriptSig to witness, reducing the base transaction size
* Witness data is discounted in weight calculation, so it contributes less to vsize
* scriptSig becomes smaller because it only contains the redeemScript instead of signature + public key
* ScriptPubKey in P2SH-P2WPKH is shorter than the full P2PKH locking script
* The transaction ID does not include witness data, so less data is counted in the base transaction
* Reduced base size lowers the weight, which directly reduces the virtual size
* Smaller virtual size results in lower fee because fees are calculated per vbyte

weight = base_size × 4 + witness_size
vsize = weight / 4

Because the witness part is multiplied by 1 instead of 4, the total weight and virtual size of the SegWit transaction becomes smaller.

#### 4. Benefits of SegWit transactions

* Lower transaction fees due to smaller virtual size
* More transactions can fit in one block
* Fixes transaction malleability problem
* Improves scalability of the Bitcoin network
* Enables advanced features like Lightning Network





