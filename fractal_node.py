# Law of Shaped Force: Optimized Fractal Matrix Engine
import time
import socket
import sys

HOST = '127.0.0.1'
PORT = 8888

class ERC721TokenState:
    def __init__(self):
        self.registry = {}
        self.next_token_id = 1

    def mint(self, owner_addr: str, metadata: dict) -> dict:
        token_id = self.next_token_id
        self.registry[token_id] = {
            "owner": owner_addr,
            "metadata": metadata,
            "minted_at": time.time()
        }
        self.next_token_id += 1
        return {"status": "SUCCESS", "token_id": token_id, "owner": owner_addr}

def evaluate_fractal_gate(cr: float, ci: float, max_iter: int = 100) -> bool:
    zr, zi = 0.0, 0.0
    iteration = 0
    while iteration < max_iter:
        if (zr * zr + zi * zi) > 4.0:
            # Clears instantly upon escaping the complex boundary
            print(f"[GATE-PASS] Force escaped bounds at loop iteration: {iteration}")
            return True
        temp_zr = zr * zr - zi * zi + cr
        zi = 2.0 * zr * zi + ci
        zr = temp_zr
        iteration += 1
    return False # Trapped in the stable set body

def process_shaped_force_packet(token_engine: ERC721TokenState, raw_payload: str, addr: tuple) -> str:
    try:
        if not raw_payload.startswith("MINT_REQUEST:"):
            return "ERR: INVALID_PROTOCOL_PREFIX\n"
        coords_str = raw_payload.replace("MINT_REQUEST:", "").strip()
        cr_str, ci_str = coords_str.split(",")
        cr, ci = float(cr_str), float(ci_str)
        print(f"[GATE-CHECK] Evaluating complex space coordinate c = ({cr} + {ci}i)")
        
        if evaluate_fractal_gate(cr, ci):
            metadata = {"type": "Shaped Force Waveform", "cr": cr, "ci": ci}
            tx_receipt = token_engine.mint(owner_addr=f"termux://{addr[0]}:{addr[1]}", metadata=metadata)
            print(f"[MINT-CONFIRMED] ERC-721 Token #{tx_receipt['token_id']} successfully bound.")
            return f"ACK: MINTED_ERC721_TOKEN_{tx_receipt['token_id']}\n"
        else:
            print("[REJECTED] Coordinate stable / trapped inside boundary body.")
            return "ERR: SHAPED_FORCE_COLLAPSE\n"
    except Exception as e:
        return f"ERR: MATRIX_PERTURBATION ({str(e)})\n"

def init_sovereign_node():
    print("[INIT] Booting local ERC-721 execution loop via Termux...")
    token_engine = ERC721TokenState()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"[LOCKED] Local interface bound to {HOST}:{PORT}")
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"\n[CONN] Channel open with {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        decoded_msg = data.decode('utf-8', errors='ignore')
                        response = process_shaped_force_packet(token_engine, decoded_msg, addr)
                        conn.sendall(response.encode('utf-8'))
            except KeyboardInterrupt:
                print("\n[SHUTDOWN] Sovereign node halted.")
                sys.exit(0)
            except Exception as e:
                print(f"[ERR] Runtime loop error: {e}")

if __name__ == "__main__":
    init_sovereign_node()
