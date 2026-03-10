# CS-216-Chain_Snatcher-Bitcoin-Transaction-simulation

## Team Information
* **Team Member 1:** Managari Saatvik - 240002035
* **Team Member 2:** [Nagalla AbhiSri Karthik] - [240002041]
*(Note: Ensure this is the same team from the 1st programming assignment as required)*

## Instructions on How to Run the Program
*(Provide clear, step-by-step instructions here so the grader can run your code)*
1. **Prerequisites:** Ensure `bitcoind`, `bitcoin-cli`, and `btcdeb` are installed.
2. **Environment Setup:** * Start bitcoind in Regtest mode.
   * Ensure `bitcoin.conf` has the correct fee settings (paytxfee=0.0001, etc.).
3. **Execution:**
   * Run the Part 1 script: `python part1_legacy.py` (or your specific command).
   * Run the Part 2 script: `python part2_segwit.py`.

---

## Part 1: Legacy Address Transactions (P2PKH)

### 1.1 Transaction Workflow
* **Transaction A -> B:**
  * **TXID:** `[Insert TXID here]`
* **Transaction B -> C:**
  * **TXID:** `[Insert TXID here]`
  * **Workflow Explanation:** The transaction from A to B created a UTXO for address B. This UTXO (referenced by its txid and vout) was then used as the input to fund the subsequent transaction from B to C.

### 1.2 Decoded Scripts
* **Transaction A -> B (Locking Script for B):**
  ```json
  [Insert JSON snippet of the ScriptPubKey here]
