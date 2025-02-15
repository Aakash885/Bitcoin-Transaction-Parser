import sys
import requests
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Address

BLOCKSTREAM_API = "https://blockstream.info/api/tx/"
MEMPOOL_FEE_API = "https://mempool.space/api/v1/fees/recommended"

def fetch_live_transaction(txid):
    """Fetches the raw transaction hex from Blockstream API."""
    try:
        url = f"{BLOCKSTREAM_API}{txid}/hex"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: Unable to fetch transaction. Status Code: {response.status_code}")
            return None

        return response.text.strip()
    
    except Exception as e:
        print(f"Error fetching transaction: {e}")
        return None

def fetch_fee_rates():
    """Fetches recommended transaction fees from Mempool.space API."""
    try:
        response = requests.get(MEMPOOL_FEE_API)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch fee rates")
            return None
    except Exception as e:
        print(f"Error fetching fee rates: {e}")
        return None

def detect_script_type(script_hex):
    """Identifies Bitcoin script type (P2PKH, P2SH, SegWit)."""
    if script_hex.startswith("76a914"):  
        return "P2PKH (Legacy)"
    elif script_hex.startswith("a914"):  
        return "P2SH (Multi-Sig)"
    elif script_hex.startswith("0014") or script_hex.startswith("0020"):  
        return "P2WPKH (SegWit)"
    else:
        return "Unknown"

def decode_transaction(hex_string):
    """Decodes Bitcoin transaction, extracting inputs, outputs, fees, and addresses."""
    try:
        tx = Transaction.parse(hex_string)

        total_input = sum(inp.value for inp in tx.inputs)
        total_output = sum(out.value for out in tx.outputs)
        fee = total_input - total_output
        tx_size = len(hex_string) // 2
        fee_per_byte = fee / tx_size if tx_size > 0 else 0

        print("\n--- Bitcoin Transaction Details ---")
        print(f"Transaction ID: {tx.txid}")
        print(f"Version: {tx.version}")
        print(f"Locktime: {tx.locktime}")

        print("\nInputs (Senders):")
        for i, inp in enumerate(tx.inputs):
            address = Address(inp.address) if inp.address else "Unknown"
            print(f"  Input {i+1}: {address}, Value: {inp.value / 1e8:.8f} BTC")

        print("\nOutputs (Receivers):")
        for i, out in enumerate(tx.outputs):
            address = Address(out.address) if out.address else "Unknown"
            script_hex = out.script.hex() if hasattr(out.script, "hex") else "Unknown"
            script_type = detect_script_type(script_hex)
            
            print(f"  Output {i+1}: {address}, Value: {out.value / 1e8:.8f} BTC, Type: {script_type}")

        print(f"\nTransaction Fee: {fee / 1e8:.8f} BTC")
        print(f"Transaction Size: {tx_size} bytes")
        print(f"Fee Rate: {fee_per_byte:.2f} sat/byte")

        # Fetch mempool fee rates
        fee_rates = fetch_fee_rates()
        if fee_rates:
            low_fee = fee_rates["economyFee"]
            medium_fee = fee_rates["halfHourFee"]
            high_fee = fee_rates["fastestFee"]

            print("\nCurrent Mempool Fee Rates:")
            print(f"Low Priority: {low_fee} sat/b")
            print(f"Medium Priority: {medium_fee} sat/b")
            print(f"High Priority: {high_fee} sat/b")

            if fee_per_byte < low_fee:
                print("\n⚠️ Warning: The fee is very low, and the transaction might take a long time.")
            elif fee_per_byte < medium_fee:
                print("\n🟡 Medium: Your fee is okay but not optimal for fast confirmation.")
            else:
                print("\n✅ High Fee: Your transaction should confirm quickly!")

    except Exception as e:
        print(f"Error decoding transaction: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parser.py <raw_transaction_hex_or_txid>")
    else:
        user_input = sys.argv[1]

        if len(user_input) == 64:  # TXID
            raw_tx = fetch_live_transaction(user_input)
            if raw_tx:
                decode_transaction(raw_tx)
        else:  # Raw hex input
            decode_transaction(user_input)
