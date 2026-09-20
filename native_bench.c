#include <stdio.h>
#include <time.h>
#include <math.h>

int main() {
    long long iterations = 50000000; // 10x more passes to give the hardware a real challenge
    double res = 93312000.0;
    double step = 2.0 * M_PI / res;
    double accumulator = 0.0;
    
    printf("🚀 Launching native machine-code engine (%lld vector passes)...\n", iterations);
    
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // Pure, unthrottled native hardware calculation loop
    for (long long i = 0; i < iterations; i++) {
        double angle = (double)i * step;
        accumulator += sin(angle) * cos(angle);
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    double duration = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    
    // 6 FLOPs per iteration
    double total_flops = (double)iterations * 6.0;
    double gflops = (total_flops / duration) / 1e9;
    
    printf("\n=== ⚡ NATIVE HARDWARE BENCHMARK RESOLVED ===\n");
    printf(" Real Duration    : %.4f seconds\n", duration);
    printf(" Checksum Vector  : %.6f\n", accumulator);
    printf(" Real CPU Velocity: %.2f GFLOPS\n", gflops);
    printf("=============================================\n");
    
    return 0;
}
