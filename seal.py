import os
import hashlib

def digest_tree(node_path):
    file_hashes = []
    for root, _, files in os.walk(node_path):
        if '.git' in root:
            continue
        for file in sorted(files):
            fp = os.path.join(root, file)
            try:
                if os.path.isfile(fp) and not os.path.islink(fp):
                    h = hashlib.sha512()
                    with open(fp, 'rb') as f:
                        while chunk := f.read(65536):
                            h.update(chunk)
                    file_hashes.append(h.hexdigest())
            except Exception:
                pass
    return hashlib.sha512(''.join(sorted(file_hashes)).encode('utf-8')).hexdigest()

if __name__ == '__main__':
    dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join(d, '.git'))]
    exclude = {'node_modules', '04_agents', 'core', 'hive', 'src'}
    targets = sorted([d for d in dirs if d not in exclude])
    
    print(f"🔥 [SEQUENTIAL MEMORY CORE ACTIVATED] Processing {len(targets)} targets without OS semaphores...")
    
    z_current = 'e14f9a8d'
    for node in targets:
        print(f"📦 Digesting: {node}")
        try:
            c_val = digest_tree(node)
            
            # Compute 86,400 rounds of SHA-512 in raw volatile memory registers
            state = f"{z_current}{c_val}".encode('utf-8')
            for _ in range(86400):
                state = hashlib.sha512(state).hexdigest().encode('utf-8')
            
            z_next = state.decode('utf-8')
            
            # Direct non-volatile write lock
            with open(os.path.join(node, '.root_hash_sha512'), 'w') as f:
                f.write(z_next + '\n')
                
            # Direct force tagging layer
            os.system(f'cd "{node}" && git tag -f "sha86400-{z_next}" >/dev/null 2>&1')
            
            print(f"   🔒 Node Sealed -> sha86400-{z_next[:16]}...")
            z_current = z_next
        except Exception as e:
            print(f"   ❌ Bypass failure on {node}: {e}")

    print(f"\n⚡ [CIRCUIT LOCKED] Final Matrix State Vector Anchor: {z_current}")
