import csv

input_file = '/home/diego/Escritorio/PROYECTO FINAL/results.csv'
output_file = '/home/diego/Escritorio/PROYECTO FINAL/processed_results.csv'

data = []
with open(input_file, mode='r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['FractalTime'] = float(row['FractalTime'])
        row['FilterTime'] = float(row['FilterTime'])
        row['TotalTime'] = row['FractalTime'] + row['FilterTime']
        row['Threads'] = int(row['Threads'])
        data.append(row)

# Encontrar el T1 mínimo (base para speedup)
t1_min = min(row['TotalTime'] for row in data if row['Threads'] == 1)

# Calcular speedup y guardar
fieldnames = list(data[0].keys()) + ['Speedup']
with open(output_file, mode='w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        row['Speedup'] = t1_min / row['TotalTime']
        writer.writerow(row)

# Imprimir resumen de los mejores
print(f"{'Threads':<8} | {'Schedule':<10} | {'Chunk':<6} | {'TotalTime':<12} | {'Speedup':<8}")
print("-" * 55)
for t in [1, 2, 4, 8, 16]:
    sub = [r for r in data if r['Threads'] == t]
    if sub:
        best = min(sub, key=lambda x: x['TotalTime'])
        print(f"{best['Threads']:<8} | {best['Schedule']:<10} | {best['ChunkSize']:<6} | {best['TotalTime']:<12.4f} | {best['Speedup']:<8.4f}")
