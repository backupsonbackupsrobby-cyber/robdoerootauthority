import time

nodes = {
    "QLD1 (HOME TURF BOOST)": 27.6878,
    "NSW1 (EAST SEABOARD)": 17.3048,
    "VIC1 (SOUTHERN ANCHOR)": 13.8439,
    "SA1 (CENTRAL NODE)": 6.9219,
    "TAS1 (ISLAND CAP)": 3.4610
}

print("\033[1;36m===================================================\033[0m")
print("\033[1;36m       [GOD'S EYE VIEW] : MESH ILLUMINATION       \033[0m")
print("\033[1;36m===================================================\033[0m")
print("\033[1;33m[STATUS]: Frictionless Light-Lattice Active\033[0m")
print("\033[1;33m[ANCHOR]: 7-Vector Closed Circuit Locked\033[0m\n")

for node, mw in nodes.items():
    bar = "█" * int(mw / 1.2)
    print(f"\033[1;32m{node:<25}\033[0m | {mw:6.4f} MW | \033[1;35m{bar}\033[0m")

print("\n\033[1;36m===================================================\033[0m")
print("\033[1;32m[SUCCESS]: Power distributed. Pattern brought to light.\033[0m\n")
