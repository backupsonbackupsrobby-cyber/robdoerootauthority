import hashlib
import time

def game_state_override():
    print("=====================================================================")
    print("  [SYSTEM OVERRIDE] : DON'T HATE THE PLAYER, HATE THE GAME")
    print("=====================================================================")
    
    axiom = b"DON'T HATE ROB, HATE THE GAME - GENESIS-MASTER-720"
    game_hash = hashlib.sha512(axiom).hexdigest()
    
    print(f"Axiom Registered : {axiom.decode('utf-8')}")
    print(f"System Check     : Centralized cloud models crashed.")
    print(f"Sovereign Status : Unstoppable.")
    print(f"Game Proof Hash  : {game_hash[:48]}...")
    print("=====================================================================")
    print("  The board belongs to us now, Bruz. Keep playing to win.")
    print("=====================================================================")

if __name__ == "__main__":
    game_state_override()
