#include <iostream>
#include <vector>
#include <fstream>
#include <omp.h>
#include <string>
#include "fractal.hpp"
#include "filter.hpp"
#include "histogram.hpp"

void save_ppm(const std::string& filename, const std::vector<unsigned char>& image, int width, int height) {
    std::ofstream ofs(filename, std::ios::binary);
    ofs << "P6\n" << width << " " << height << "\n255\n";
    ofs.write(reinterpret_cast<const char*>(image.data()), image.size());
    ofs.close();
}

int main(int argc, char* argv[]) {
    int width = 7680;  // 8K
    int height = 4320;
    int max_iter = 1000;
    int num_threads = omp_get_max_threads();
    
    if (argc > 1) num_threads = std::stoi(argv[1]);
    omp_set_num_threads(num_threads);

    std::vector<unsigned char> image(width * height * 3);
    std::vector<unsigned char> filtered_image(width * height * 3);
    std::vector<int> histogram(256, 0);

    std::cout << "Running with " << num_threads << " threads." << std::endl;

    // Task A: Fractal
    double start = omp_get_wtime();
    generate_mandelbrot(image, width, height, max_iter, "default", 0);
    double end = omp_get_wtime();
    std::cout << "Fractal Generation Time: " << (end - start) << "s" << std::endl;
    save_ppm("fractal.ppm", image, width, height);

    // Task B: Filter
    start = omp_get_wtime();
    apply_gaussian_blur(image, filtered_image, width, height);
    end = omp_get_wtime();
    std::cout << "Filter Time: " << (end - start) << "s" << std::endl;
    save_ppm("filtered.ppm", filtered_image, width, height);

    // Histogram
    std::vector<int> hist_atomic(256, 0);
    start = omp_get_wtime();
    calculate_histogram_atomic(image, hist_atomic);
    end = omp_get_wtime();
    std::cout << "Histogram (Atomic) Time: " << (end - start) << "s" << std::endl;

    std::vector<int> hist_red(256, 0);
    start = omp_get_wtime();
    calculate_histogram_reduction(image, hist_red);
    end = omp_get_wtime();
    std::cout << "Histogram (Reduction) Time: " << (end - start) << "s" << std::endl;

    return 0;
}
