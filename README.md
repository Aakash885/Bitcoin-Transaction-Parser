# **Bitcoin Transaction Parser** 🚀  
A Python tool to **fetch, decode, and analyze Bitcoin transactions in real time** using blockchain APIs.  

## **📌 Features**  
✔ Fetches Bitcoin transactions using **Blockstream API**  
✔ Extracts **inputs, outputs, sender & receiver addresses**  
✔ Supports **P2PKH, P2SH, and SegWit transactions**  
✔ Estimates **transaction fees** based on real-time **mempool data**  
✔ Handles **API failures & unsupported script types**  

## **⚙️ Installation**  
### **1️⃣ Clone the Repository**  
```bash  
git clone https://github.com/your-username/Bitcoin-Transaction-Parser.git  
cd Bitcoin-Transaction-Parser  
```

### **2️⃣ Install Dependencies**  
```bash  
pip install bitcoinlib requests  
```

## **🚀 Usage**  
Run the script with a **transaction ID**:  
```bash  
python basic.py <transaction_id>  
```
Example:  
```bash  
python basic.py b6f6991d628a5de2166244a381703b33265014c64cc19371c888b6a5e7dfd5f4  
```

## **🔧 How It Works**  
1. Fetches the raw transaction from the **Blockstream API**  
2. Parses the **transaction version, locktime, inputs, outputs, and fees**  
3. Identifies **script types** (P2PKH, P2SH, SegWit)  
4. Displays sender/receiver addresses and BTC amounts  

## **📜 Example Output**  
```
--- Bitcoin Transaction Details ---
Transaction ID: 5ca2f5d4accb886d2a949c089528bbfcf952b35ef8f3b3da26315e700476a269
Version: 2
Locktime: 0

Inputs (Senders):
  Address: bc1qtcza72rcvkxhwzwmxdr3su7088uw5f5lx7rz9n, Value: 0.0023 BTC

Outputs (Receivers):
  Address: 1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy, Value: 0.0021 BTC

Transaction Fee: 0.0002 BTC
```

## **📜 Dependencies**  
- **bitcoinlib** – for parsing transactions  
- **requests** – for fetching transaction data from blockchain APIs  

## **📜 License**  
This project is **MIT Licensed**. Feel free to use and modify it!  
