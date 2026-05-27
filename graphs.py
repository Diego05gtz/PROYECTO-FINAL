import csv
import math

def generate_svg_line_chart_comparison(data, filename, title, x_label, y_label):
    threads = sorted(list(set(int(row['Threads']) for row in data)))
    schedules = sorted(list(set(row['Schedule'] for row in data)))
    
    width = 700
    height = 500
    padding = 70
    
    # Get max speedup for scaling
    max_speedup = max(float(row['Speedup']) for row in data)
    max_y = max(max_speedup, max(threads))
    
    scale_y = (height - 2 * padding) / max_y
    scale_x = (width - 2 * padding) / (max(threads) - min(threads)) if len(threads) > 1 else 1

    colors = {"static": "red", "dynamic": "green", "guided": "blue"}

    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append(f'<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">{title}</text>')
    
    # Axes
    svg.append(f'<line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>')
    svg.append(f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>')
    
    # Ideal Line
    points_ideal = []
    for t in threads:
        px = padding + (t - min(threads)) * scale_x
        py = (height - padding) - t * scale_y
        points_ideal.append(f"{px},{py}")
    svg.append(f'<polyline points="{" ".join(points_ideal)}" fill="none" stroke="#ccc" stroke-width="1" stroke-dasharray="5,5"/>')

    # Legend
    for i, s in enumerate(schedules):
        svg.append(f'<rect x="{width-120}" y="{padding + i*25}" width="15" height="15" fill="{colors.get(s, "black")}"/>')
        svg.append(f'<text x="{width-100}" y="{padding + i*25 + 12}" font-family="Arial" font-size="12">{s.capitalize()}</text>')

    # One line per scheduler (using best chunk per scheduler/thread)
    for s in schedules:
        points = []
        for t in threads:
            best_t_s = max([float(row['Speedup']) for row in data if int(row['Threads']) == t and row['Schedule'] == s] + [0])
            if best_t_s > 0:
                px = padding + (t - min(threads)) * scale_x
                py = (height - padding) - best_t_s * scale_y
                points.append(f"{px},{py}")
                svg.append(f'<circle cx="{px}" cy="{py}" r="3" fill="{colors[s]}"/>')
        
        if points:
            svg.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{colors[s]}" stroke-width="2"/>')
    
    # Labels
    svg.append(f'<text x="{width/2}" y="{height-15}" text-anchor="middle" font-family="Arial" font-size="14">{x_label}</text>')
    svg.append(f'<text x="25" y="{height/2}" text-anchor="middle" font-family="Arial" font-size="14" transform="rotate(-90 25,{height/2})">{y_label}</text>')
    
    for t in threads:
        px = padding + (t - min(threads)) * scale_x
        svg.append(f'<text x="{px}" y="{height-padding+20}" text-anchor="middle" font-family="Arial" font-size="12">{t}</text>')

    svg.append('</svg>')
    with open(filename, 'w') as f: f.write("\n".join(svg))
    print(f"Generated {filename}")

def generate_svg_heatmap(data, filename, target_threads):
    schedules = ["static", "dynamic", "guided"]
    chunks = sorted(list(set(int(row['ChunkSize']) for row in data)))
    
    # Filter data for target threads
    filtered = [r for r in data if int(r['Threads']) == target_threads]
    if not filtered: return

    width = 800
    height = 300
    padding_left = 100
    padding_top = 60
    padding_bottom = 60
    padding_right = 40
    
    cell_w = (width - padding_left - padding_right) / len(chunks)
    cell_h = (height - padding_top - padding_bottom) / len(schedules)

    times = [float(r['FractalTime']) for r in filtered]
    min_t, max_t = min(times), max(times)

    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Fractal Time Heatmap ({target_threads} Threads)</text>')

    for i, s in enumerate(schedules):
        # Y label
        svg.append(f'<text x="{padding_left-10}" y="{padding_top + i*cell_h + cell_h/2}" text-anchor="end" font-family="Arial" font-size="12">{s.capitalize()}</text>')
        for j, c in enumerate(chunks):
            # X label (only once)
            if i == 0:
                svg.append(f'<text x="{padding_left + j*cell_w + cell_w/2}" y="{height-padding_bottom+20}" text-anchor="middle" font-family="Arial" font-size="12">{c}</text>')
            
            # Find time
            match = [r for r in filtered if r['Schedule'] == s and int(r['ChunkSize']) == c]
            if match:
                t = float(match[0]['FractalTime'])
                # Interpolate color (Yellow to Red)
                # min_t (yellow) -> max_t (red)
                ratio = (t - min_t) / (max_t - min_t) if max_t > min_t else 0
                r = 255
                g = int(255 * (1 - ratio))
                b = 0
                svg.append(f'<rect x="{padding_left + j*cell_w}" y="{padding_top + i*cell_h}" width="{cell_w}" height="{cell_h}" fill="rgb({r},{g},{b})" stroke="white"/>')
                svg.append(f'<text x="{padding_left + j*cell_w + cell_w/2}" y="{padding_top + i*cell_h + cell_h/2 + 5}" text-anchor="middle" font-family="Arial" font-size="10" fill="{"black" if ratio < 0.5 else "white"}">{t:.2f}</text>')

    svg.append(f'<text x="{width/2}" y="{height-15}" text-anchor="middle" font-family="Arial" font-size="14">Chunk Size</text>')
    svg.append('</svg>')
    
    with open(filename, 'w') as f: f.write("\n".join(svg))
    print(f"Generated {filename}")

def generate_svg_line_chart(data, filename, title, x_label, y_label, x_key, y_key):
    threads = sorted(list(set(int(row['Threads']) for row in data)))
    best_values = []
    for t in threads:
        val = max(float(row[y_key]) for row in data if int(row['Threads']) == t)
        best_values.append(val)
    
    width = 600
    height = 400
    padding = 60
    max_y = max(best_values + threads)
    scale_y = (height - 2 * padding) / max_y
    scale_x = (width - 2 * padding) / (max(threads) - min(threads)) if len(threads) > 1 else 1

    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="20" font-weight="bold">{title}</text>')
    svg.append(f'<line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>')
    svg.append(f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>')
    
    points_ideal = []
    for t in threads:
        px = padding + (t - min(threads)) * scale_x
        py = (height - padding) - t * scale_y
        points_ideal.append(f"{px},{py}")
    svg.append(f'<polyline points="{" ".join(points_ideal)}" fill="none" stroke="gray" stroke-width="1" stroke-dasharray="5,5"/>')

    points_real = []
    for i, t in enumerate(threads):
        px = padding + (t - min(threads)) * scale_x
        py = (height - padding) - best_values[i] * scale_y
        points_real.append(f"{px},{py}")
        svg.append(f'<circle cx="{px}" cy="{py}" r="4" fill="blue"/>')
        svg.append(f'<text x="{px}" y="{py-10}" text-anchor="middle" font-family="Arial" font-size="12" fill="blue">{best_values[i]:.2f}</text>')
    
    svg.append(f'<polyline points="{" ".join(points_real)}" fill="none" stroke="blue" stroke-width="2"/>')
    svg.append(f'<text x="{width/2}" y="{height-10}" text-anchor="middle" font-family="Arial" font-size="14">{x_label}</text>')
    svg.append('</svg>')
    with open(filename, 'w') as f: f.write("\n".join(svg))
    print(f"Generated {filename}")

def generate_svg_hist_chart(data, filename):
    best_16_list = [r for r in data if int(r['Threads']) == 16 and r['Schedule'] == 'static' and int(r['ChunkSize']) == 8]
    if not best_16_list: return
    best_16 = best_16_list[0]
    atomic = float(best_16['HistAtomic'])
    reduction = float(best_16['HistReduction'])
    width, height, padding = 400, 400, 60
    max_val = max(atomic, reduction)
    scale_y = (height - 2 * padding) / max_val
    svg = [f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">']
    svg.append('<rect width="100%" height="100%" fill="white"/>')
    svg.append(f'<text x="{width/2}" y="30" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Atomic vs Reduction</text>')
    h1 = atomic * scale_y
    svg.append(f'<rect x="{padding + 40}" y="{height - padding - h1}" width="80" height="{h1}" fill="red"/>')
    svg.append(f'<text x="{padding + 80}" y="{height - padding - h1 - 10}" text-anchor="middle" font-family="Arial" font-size="12">{atomic:.4f}s</text>')
    h2 = reduction * scale_y
    svg.append(f'<rect x="{padding + 180}" y="{height - padding - h2}" width="80" height="{h2}" fill="green"/>')
    svg.append(f'<text x="{padding + 220}" y="{height - padding - h2 - 10}" text-anchor="middle" font-family="Arial" font-size="12">{reduction:.4f}s</text>')
    svg.append(f'<line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="black" stroke-width="2"/>')
    svg.append('</svg>')
    with open(filename, 'w') as f: f.write("\n".join(svg))
    print(f"Generated {filename}")

def main():
    data = []
    try:
        with open('/home/diego/Escritorio/PROYECTO FINAL/processed_results.csv', mode='r') as f:
            reader = csv.DictReader(f); data = [row for row in reader]
    except FileNotFoundError: return
    
    generate_svg_line_chart(data, 'speedup_best.svg', 'Best Speedup Overall', 'Threads', 'Speedup', 'Threads', 'Speedup')
    generate_svg_line_chart_comparison(data, 'speedup_comparison.svg', 'Speedup by Scheduler', 'Threads', 'Speedup')
    generate_svg_heatmap(data, 'heatmap_16_threads.svg', 16)
    generate_svg_hist_chart(data, 'sync_comparison.svg')
    print("\nAll SVG visualizations generated successfully.")

if __name__ == "__main__": main()
