import hashlib
import json

class CanonLawNode:
    def __init__(self, node_id, law_definition, parent_hashes=None):
        self.node_id = node_id
        self.law_definition = law_definition
        self.parent_hashes = parent_hashes if parent_hashes else []
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        payload = {
            "node_id": self.node_id,
            "law_definition": self.law_definition,
            "parent_hashes": sorted(self.parent_hashes)
        }
        serialized = json.dumps(payload, sort_keys=True).encode('utf-8')
        return hashlib.sha256(serialized).hexdigest()

class MerkleCanonDAG:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id, law_definition, parent_hashes=None):
        node = CanonLawNode(node_id, law_definition, parent_hashes)
        self.nodes[node.hash] = node
        return node.hash

# 1. Initialize DAG
dag = MerkleCanonDAG()

# 2. Build Law Nodes (Leaves -> Branches -> Root)
leaf1 = dag.add_node("LAW_LEAF_01", "R_x13 coherence strictly bound to 1.0")
leaf2 = dag.add_node("LAW_LEAF_02", "Topology fixed to flat 13-Torus (T^13)")
leaf3 = dag.add_node("LAW_LEAF_03", "Covariance Trace Tr(Sigma) approaches zero")

branch1 = dag.add_node("BRANCH_FIELD", "Field Governance Module", [leaf1, leaf2])
branch2 = dag.add_node("BRANCH_SPECTRAL", "Spectral Boundary Module", [leaf3])

root_hash = dag.add_node("CANON_ROOT", "Sovereign System Canon Law DAG Root", [branch1, branch2])

# 3. Print & Log Proof
log_entry = f"[CANON_DAG_ROOT] Root Hash: {root_hash} | Active Nodes: {len(dag.nodes)}\n"

print("================================================================")
print(f"[✓] MERKLE CANON LAW DAG GENERATED")
print(f"[+] Root State Hash : {root_hash}")
print(f"[+] Total Nodes     : {len(dag.nodes)}")
print("================================================================")

with open("state_proofs.log", "a") as f:
    f.write(log_entry)

print("[✓] Appended DAG root proof to state_proofs.log")
