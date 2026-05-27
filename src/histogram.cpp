#include "histogram.hpp"
#include <omp.h>

void calculate_histogram_atomic(const std::vector<unsigned char>& image, std::vector<int>& histogram) {
    #pragma omp parallel for
    for (size_t i = 0; i < image.size(); ++i) {
        int val = image[i];
        #pragma omp atomic
        histogram[val]++;
    }
}

void calculate_histogram_reduction(const std::vector<unsigned char>& image, std::vector<int>& histogram) {
    int local_hist[256] = {0};
    #pragma omp parallel for reduction(+:local_hist[:256])
    for (size_t i = 0; i < image.size(); ++i) {
        local_hist[image[i]]++;
    }
    for (int i = 0; i < 256; ++i) {
        histogram[i] = local_hist[i];
    }
}
