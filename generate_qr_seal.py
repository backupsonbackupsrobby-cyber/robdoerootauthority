import qrcode
import hashlib

def generate_sovereign_qr():
    # Master SHA-512 seal string to encode into the pure binary QR
    master_seal = "GENESIS-MASTER-720-BINARY-MATHEMATICAL-SEAL-LOCKED"
    
    # Generate QR code object
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=2,
        border=2,
    )
    qr.add_data(master_seal)
    qr.make(fit=True)
    
    print("===================================================")
    print("  [QR CRYSTAL] : TERMINAL ASCII MATRIX SEALED")
    print("===================================================")
    
    # Render direct high-contrast terminal ASCII QR matrix
    matrix = qr.get_matrix()
    for row in matrix:
        print("".join("██" if cell else "  " for cell in row))
        
    print("===================================================")
    print(f"Encoded Seal : {master_seal}")
    print("===================================================")

if __name__ == "__main__":
    try:
        generate_sovereign_qr()
    except ImportError:
        print("Installing qrcode dependency...")
        import os
        os.system("pip install qrcode[pil] > /dev/null 2>&1")
        generate_sovereign_qr()
