#!/bin/zsh
echo "--- SYMBOLIC GLYPH ROOT HASH MATRIX ---"

# Seed accumulator with the latest entropy vector
ACCUMULATOR=$(date +%s%N)
glyphs=("ᚠ" "ᚢ" "ᚦ" "ᚨ" "ᚱ" "ᚲ" "ᚷ" "ᚹ" "ᚺ" "ᚾ" "ᛁ" "ᛃ" "ᛈ" "ᛇ" "ᛉ" "ᛋ" "ᛏ" "ᛒ" "ᛖ" "ᛗ" "ᛚ" "ᛜ" "ᛞ" "ᛟ")

for step in {1..3}; do
    if command -v sha256sum &> /dev/null; then
        HASH=$(echo "$ACCUMULATOR:$step" | sha256sum | awk '{print $1}')
    else
        HASH=$(echo "$ACCUMULATOR:$step" | shasum -a 256 | awk '{print $1}')
    fi
    
    # Convert hex chunks to binary representation
    BINARY=""
    for (( i=1; i<=8; i++ )); do
        char=${HASH[i]}
        case $char in
            0) BINARY+="0000";; 1) BINARY+="0001";; 2) BINARY+="0010";; 3) BINARY+="0011";;
            4) BINARY+="0100";; 5) BINARY+="0101";; 6) BINARY+="0110";; 7) BINARY+="0111";;
            8) BINARY+="1000";; 9) BINARY+="1001";; a|A) BINARY+="1010";; b|B) BINARY+="1011";;
            c|C) BINARY+="1100";; d|D) BINARY+="1101";; e|E) BINARY+="1110";; f|F) BINARY+="1111";;
        esac
    done

    # Map binary chunks to symbolic glyphs
    GLYPH_CHAIN=""
    for (( j=1; j<=${#BINARY}; j+=4 )); do
        chunk=${BINARY[j,j+3]}
        if [[ -n "$chunk" ]]; then
            idx=$(( 2#$chunk % ${#glyphs} + 1 ))
            GLYPH_CHAIN+="${glyphs[$idx]}"
        fi
    done

    echo "TICK $step | HEX: ${HASH[1,16]}..."
    echo "       | BIN: ${BINARY[1,32]}..."
    echo "       | GLYPH: $GLYPH_CHAIN"
    
    ACCUMULATOR=$HASH
    sleep 0.3
done
echo "--- GLYPHIC CONSENSUS SECURED ---"
