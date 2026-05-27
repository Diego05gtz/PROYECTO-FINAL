# 🚀 Proyecto Final: Programación Paralela y Concurrente
> **Optimización de Fractales y Procesamiento de Imágenes con OpenMP**

Este proyecto implementa un sistema de alto rendimiento para la generación de fractales en **8K** y el procesamiento de imágenes mediante filtros de convolución, aplicando técnicas avanzadas de paralelismo y vectorización.

---

## 🛠️ Características Principales

- **❄️ Fractal Engine**: Generación del conjunto de Mandelbrot en resolución 8K (7680x4320).
- **👁️ Image Filtering**: Aplicación de desenfoque gaussiano optimizado con **SIMD (Single Instruction, Multiple Data)**.
- **📊 Histogram & Sync**: Análisis comparativo de sincronización entre `atomic` y `reduction` (evitando *False Sharing*).
- **📈 Benchmarking Suite**: Sistema automático para medir el impacto de diferentes *schedulers* (`static`, `dynamic`, `guided`) y tamaños de bloque (*chunks*).
- **🎨 Visual Analytics**: Generador de gráficas SVG (Speedup, Heatmaps, Histogramas) integrado.

---

## 📁 Estructura del Proyecto

```text
.
├── src/                # Código fuente C++ (.cpp, .hpp)
├── scripts/            # Scripts de automatización (Bash, Python)
├── Makefile            # Sistema de construcción optimizado
├── graphs.py           # Generador de visualizaciones profesionales
├── Proyecto_final.pdf  # Requerimientos originales
└── results.csv         # Datos crudos del benchmark
```

---

## 🚀 Guía de Inicio Rápido

### 1️⃣ Compilación
Construye el binario optimizado de forma silenciosa:
```bash
make clean && make
```

### 2️⃣ Ejecución del Proyecto
Corre una prueba rápida con 8 hilos:
```bash
./proyecto 8
```

### 3️⃣ Benchmark Completo
Ejecuta el análisis exhaustivo de todas las configuraciones:
```bash
chmod +x scripts/benchmark.sh
./scripts/benchmark.sh
```

### 4️⃣ Generación de Gráficas
Crea las visualizaciones para tu reporte final:
```bash
python3 graphs.py
```

---

## 💻 Especificaciones del Sistema
Puedes obtener los detalles técnicos de tu hardware ejecutando la utilidad incluida:
```bash
g++ -fopenmp src/specs.cpp -o specs && ./specs > specs.txt
```

---

## 📊 Análisis de Resultados
El proyecto genera un archivo `processed_results.csv` que incluye:
- **TotalTime**: Suma de tiempos de todas las tareas.
- **Speedup**: Cálculo de mejora de rendimiento respecto a 1 hilo.
- **Sync Metrics**: Comparativa de tiempos de sincronización.

---

## ✒️ Autor
**Proyecto Final de Computación de Alto Rendimiento**  
*Desarrollado para la demostración de optimización de carga y eficiencia paralela.*

---
<p align="center">
  Hecho con ❤️ para la eficiencia computacional
</p>
