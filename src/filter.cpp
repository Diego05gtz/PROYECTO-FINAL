#include "filter.hpp"
#include <omp.h>

void apply_gaussian_blur(const std::vector<unsigned char>& input, std::vector<unsigned char>& output, int width, int height) {
    float kernel[5][5] = {
        {1/273.f, 4/273.f, 7/273.f, 4/273.f, 1/273.f},
        {4/273.f, 16/273.f, 26/273.f, 16/273.f, 4/273.f},
        {7/273.f, 26/273.f, 41/273.f, 26/273.f, 7/273.f},
        {4/273.f, 16/273.f, 26/273.f, 16/273.f, 4/273.f},
        {1/273.f, 4/273.f, 7/273.f, 4/273.f, 1/273.f}
    };

    #pragma omp parallel for collapse(2)
    for (int y = 2; y < height - 2; ++y) {
        for (int x = 2; x < width - 2; ++x) {
            float r = 0, g = 0, b = 0;
            
            // Inner loops for convolution - candidate for SIMD
            for (int ky = -2; ky <= 2; ++ky) {
                #pragma omp simd reduction(+:r,g,b)
                for (int kx = -2; kx <= 2; ++kx) {
                    int pixel_idx = ((y + ky) * width + (x + kx)) * 3;
                    float k_val = kernel[ky + 2][kx + 2];
                    r += input[pixel_idx] * k_val;
                    g += input[pixel_idx + 1] * k_val;
                    b += input[pixel_idx + 2] * k_val;
                }
            }
            
            int out_idx = (y * width + x) * 3;
            output[out_idx] = (unsigned char)r;
            output[out_idx + 1] = (unsigned char)g;
            output[out_idx + 2] = (unsigned char)b;
        }
    }
}
