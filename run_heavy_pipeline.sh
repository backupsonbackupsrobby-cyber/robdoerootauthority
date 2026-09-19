# --------------------------------------------------------------------------
# 💀 INTEGRATED MANDELBROT / JULIA SET CHAOS LOOP
# --------------------------------------------------------------------------
render_chaos_matrix() {
    clear
    # Extract real-time telemetry vectors to define the complex seed (c = cx + i*cy)
    local batt=$(cat /sys/class/power_supply/battery/capacity 2>/dev/null || echo "50")
    local mem=$(free -m | awk '/Mem:/ {print $4}' || echo "1024")
    
    # Map battery percentage and memory size into bounded complex plane scales
    local cx=$(echo "scale=4; -0.7 + ($batt / 500.0)" | bc -l)
    local cy=$(echo "scale=4; 0.27015 + ($mem / 10000.0)" | bc -l)
    
    local width=70
    local height=35
    local max_iter=24
    local chars=(" " "." ":" "-" "=" "+" "*" "#" "%" "@" "💀" "⚡" "█")

    echo "=========================================================="
    echo "❄️ FRACTAL MATRIX ACTIVED // SEED: ($cx + $cy i)"
    echo "=========================================================="
    
    # Iterate across the 2D terminal plane grid
    for ((y=0; y<height; y++)); do
        local line=""
        for ((x=0; x<width; x++)); do
            # Map grid coordinates to complex plane boundaries (-1.5 to 1.5)
            local zx=$(echo "scale=4; ($x - $width/2) * 3.0 / $width" | bc -l)
            local zy=$(echo "scale=4; ($y - $height/2) * 2.0 / $height" | bc -l)
            local iter=0
            
            # Compute Julia feedback sequence z = z^2 + c
            while [ $iter -lt $max_iter ]; do
                # Precision float calculations via native bc backend
                local x2=$(echo "scale=4; $zx * $zx" | bc -l)
                local y2=$(echo "scale=4; $zy * $zy" | bc -l)
                local dist=$(echo "scale=4; $x2 + $y2" | bc -l)
                
                # Check for boundary escape threshold (escape velocity > 4)
                if (( $(echo "$dist > 4.0" | bc -l) )); then
                    break
                fi
                
                # Compute next state coordinates
                local new_zy=$(echo "scale=4; 2.0 * $zx * $zy + $cy" | bc -l)
                zx=$(echo "scale=4; $x2 - $y2 + $cx" | bc -l)
                zy=$new_zy
                iter=$((iter + 1))
            done
            
            # Map structural depth to the character matrix string
            local char_index=$(( iter % ${#chars[@]} ))
            line+="${chars[$char_index]}"
        done
        echo -e "$line"
    done
    echo "=========================================================="
    echo "⚡ Controlled Chaos Complete. Terminal session locked."
}

# Replace standard exit vector with our integrated fractal loop
trap "kill -9 $MESH_PID $OFFLOAD_PID 2>/dev/null; render_chaos_matrix" EXIT
