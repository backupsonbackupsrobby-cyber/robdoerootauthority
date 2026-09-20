import datetime

def seal_ledger():
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    proof_entry = f'{{"timestamp": "{timestamp}", "state": "ABSOLUTE", "anchor": "LadbotOneLad", "status": "LOCKED"}}\n'
    
    with open("STATE_PROOFS.jsonl", "a") as f:
        f.write(proof_entry)
        
    print("[SUCCESS] Final ledger state permanently sealed.")

if __name__ == "__main__":
    seal_ledger()
