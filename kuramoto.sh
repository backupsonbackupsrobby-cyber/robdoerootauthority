#!/bin/zsh

N=4
K=1.5
dt=0.05
steps=10

typeset -a theta omega new_theta

for ((i=1; i<=N; i++)); do
    theta[$i]=$(jot -r 1 0 6.28 2>/dev/null || awk -v seed=$RANDOM 'BEGIN {srand(seed); print rand() * 6.28}')
    omega[$i]=$(jot -r 1 0.5 1.5 2>/dev/null || awk -v seed=$RANDOM 'BEGIN {srand(seed); print 0.5 + rand()}')
done

for ((step=1; step<=steps; step++)); do
    print "--- Step $step ---"
    for ((i=1; i<=N; i++)); do
        sum=0
        for ((j=1; j<=N; j++)); do
            diff=$(( theta[j] - theta[i] ))
            s_val=$(awk -v d="$diff" 'BEGIN {print sin(d)}')
            sum=$(awk -v s="$sum" -v sv="$s_val" 'BEGIN {print s + sv}')
        done
        
        coupling_term=$(awk -v k="$K" -v n="$N" -v sm="$sum" 'BEGIN {print (k / n) * sm}')
        dtheta=$(awk -v om="${omega[i]}" -v ct="$coupling_term" 'BEGIN {print om + ct}')
        new_theta[i]=$(awk -v th="${theta[i]}" -v dt="$dt" -v dth="$dtheta" 'BEGIN {print th + (dth * dt)}')
        print "theta[$i] = ${new_theta[i]}"
    done
    for ((i=1; i<=N; i++)); do
        theta[i]=${new_theta[i]}
    done
done
