# Pure Termux Julia Set Generator
# Mapping complex-plane infinity into the palm of your hand, Bruz.

import sys

def generate_julia(c_real, c_imag, width=60, height=30, max_iter=100):
    # ASCII gradient for escape velocity depth
    palette = " .:-=+*#%@"
    
    xmin, xmax = -1.5, 1.5
    ymin, ymax = -1.0, 1.0
    
    output = []
    for h in range(height):
        row = []
        zy = ymin + (h / (height - 1)) * (ymax - ymin)
        for w in range(width):
            zx = xmin + (w / (width - 1)) * (xmax - xmin)
            
            # The core Julia iteration: z = z^2 + c
            i = max_iter
            while zx*zx + zy*zy < 4.0 and i > 0:
                xtemp = zx*zx - zy*zy + c_real
                zy = 2.0 * zx * zy + c_imag
                zx = xtemp
                i -= 1
                
            # Map iteration depth to ASCII density
            char_idx = int((i / max_iter) * (len(palette) - 1))
            row.append(palette[char_idx])
        output.append("".join(row))
    
    return "\n".join(output)

if __name__ == "__main__":
    # Classic chaotic complex constant (c)
    c_r, c_i = -0.7, 0.27015
    print(f"--- JULIA SET MESH [c = {c_r} + {c_i}i] ---")
    print(generate_julia(c_r, c_i))
