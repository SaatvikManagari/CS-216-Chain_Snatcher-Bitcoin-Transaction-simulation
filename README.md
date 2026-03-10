# CS-216-Chain_Snatchers-Bitcoin-Transaction-simulation

## Introduction

This project demonstrates the creation, signing, broadcasting, and verification of Bitcoin transactions using Bitcoin Core in regtest mode. The objective of this simulation is to understand how Bitcoin transactions work internally by manually constructing and analyzing both Legacy (P2PKH) and SegWit (P2SH-P2WPKH) transactions.
Using RPC commands, Python scripts, and the btcdeb Bitcoin Script debugger, we simulate the complete transaction workflow including wallet funding, raw transaction creation, script validation, and UTXO spending. The project also compares Legacy and SegWit transactions in terms of script structure, transaction size, weight, and fees, providing a clear understanding of how SegWit improves efficiency and solves issues such as transaction malleability.
This simulation helps in gaining practical knowledge of Bitcoin’s scripting system, transaction format, and validation mechanism at a low level.

## Team Information

### Team Name: Chain Snatchers

* **Team Member 1:** Managari Saatvik - 240002035
* **Team Member 2:** Nagalla AbhiSri Karthik - 240002041
* **Team Member 3:** Nemani Sandeep - 240002044
* **Team Member 4:** Malladi Charan - 240008016

## Requirements:
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
rpcuser=charan
rpcpassword=123charan
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
* Fund the Wallet by mining 101 Blocks (Standard), generating 50 BTC

Download all the Python files locally and keep the bitcoin.conf file in the Bitcoin running directory. Run the Legacy_work.py for legacy transactions and segwit_work.py for segwit transactions

**Note:** The wallet is unloaded after every execution of the file to avoid conflict between the wallets of both files. But if the same file were to be run more than once, the entire regtest is required to be manually reset by deleting the wallets and regtest folders. 

