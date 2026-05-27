#!/bin/bash

# Compilar silenciosamente
make clean
make

# CSV Headers
echo "Threads,Schedule,ChunkSize,FractalTime,FilterTime,HistAtomic,HistReduction" > results.csv

THREADS_LIST="1 2 4 8 16"
SCHEDULES="static dynamic guided"
CHUNKS="1 2 4 8 16 32 64 128"

echo "Starting Benchmark..."

for t in $THREADS_LIST; do
    for sched in $SCHEDULES; do
        for chunk in $CHUNKS; do
            # Mostrar solo la configuración actual en una sola línea
            printf "Running: [Threads: %2d | Sched: %-7s | Chunk: %3d] ... " "$t" "$sched" "$chunk"
            
            export OMP_SCHEDULE="$sched,$chunk"
            
            # Ejecutar y capturar salida, redirigiendo errores a /dev/null
            OUTPUT=$(./proyecto $t 2>/dev/null)
            
            # Extraer datos de la salida capturada
            FRACTAL=$(echo "$OUTPUT" | grep "Fractal Generation Time" | awk '{print $4}' | sed 's/s//')
            FILTER=$(echo "$OUTPUT" | grep "Filter Time" | awk '{print $3}' | sed 's/s//')
            ATOMIC=$(echo "$OUTPUT" | grep "Histogram (Atomic) Time" | awk '{print $4}' | sed 's/s//')
            REDUCTION=$(echo "$OUTPUT" | grep "Histogram (Reduction) Time" | awk '{print $4}' | sed 's/s//')
            
            echo "$t,$sched,$chunk,$FRACTAL,$FILTER,$ATOMIC,$REDUCTION" >> results.csv
            
            printf "Done\n"
        done
    done
done

echo "----------------------------------------------------"
echo "Benchmark finished successfully."
echo "Results saved in: results.csv"
echo "----------------------------------------------------"
