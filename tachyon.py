# TACHYON-PHASE JULIA ENGINE [v72.0-TURBO]
import math
import sys

def render_tachyon_grid(step, width=64, height=32):
    palette = " .·:=+*#%@█"
    c_real, c_imag = -0.7, 0.27015
    
    tachyon_shift = math.sin(step * 0.2) * 0.15
    
    xmin, xmax = -1.0 + tachyon_shift, 1.0 + tachyon_shift
    ymin, ymax = -0.6, 0.6
    
    output = [f"--- TACHYON FLUX MATRIX [T-STEP: {step:03d}] ---"]
    for h in range(height):
        row = []
        zy = ymin + (h / (height - 1)) * (ymax - ymin)
        for w in range(width):
            zx = xmin + (w / (width - 1)) * (xmax - xmin)
            
            i = 80
            while zx*zx + zy*zy < 4.0 and i > 0:
                xtemp = (zx*zx - zy*zy) + c_real + (tachyon_shift * 0.5)
                zy = (2.0 * zx * zy) + c_imag - (tachyon_shift * 0.3)
                zx = xtemp
                i -= 1
                
            char_idx = int((i / 80) * (len(palette) - 1))
            row.append(palette[char_idx])
        output.append("".join(row))
    return "\n".join(output)

if __name__ == "__main__":
    for s in range(5):
        print(render_tachyon_grid(s))
        print("\n" + "="*64 + "\n")
