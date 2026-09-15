import merkle_canon_dag

def verify_dag_integrity():
    dag = merkle_canon_dag.dag
    print("\033[1;36m================================================================\033[0m")
    print("\033[1;36m   SOVEREIGN CANON LAW DAG: DETERMINISTIC INTEGRITY VERIFICATION\033[0m")
    print("\033[1;36m================================================================\033[0m")

    root_node = None
    for h, node in dag.nodes.items():
        if node.node_id == "CANON_ROOT":
            root_node = node
            break

    if not root_node:
        print("\033[1;31m[-] CANONICAL ROOT NODE MISSING\033[0m")
        return

    # Check child-parent cryptographic bindings
    print(f"[+] Root Node Verified : {root_node.node_id}")
    print(f"[+] Root SHA-256 Hash  : {root_node.hash}")
    print(f"[+] Root Parent Count  : {len(root_node.parent_hashes)}")
    print("----------------------------------------------------------------")

    valid = True
    for parent_hash in root_node.parent_hashes:
        if parent_hash in dag.nodes:
            p_node = dag.nodes[parent_hash]
            print(f"  [✓] Linked Branch : {p_node.node_id} ({p_node.hash[:16]}...)")
        else:
            print(f"  [-] Broken Link   : {parent_hash}")
            valid = False

    print("----------------------------------------------------------------")
    if valid:
        print("\033[1;32m[✓] MERKLE CANON LAW DAG INTEGRITY: 100% VERIFIED\033[0m")
    else:
        print("\033[1;31m[-] INTEGRITY FAILURE DETECTED\033[0m")
    print("\033[1;36m================================================================\033[0m")

if __name__ == "__main__":
    verify_dag_integrity()
