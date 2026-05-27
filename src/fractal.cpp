#include "fractal.hpp"
#include <omp.h>
#include <complex>

void generate_mandelbrot(std::vector<unsigned char>& image, int width, int height, int max_iter, const std::string& schedule_type, int chunk_size) {
    // Definir los límites del plano complejo
    double min_re = -2.0, max_re = 1.0;
    double min_im = -1.2, max_im = 1.2;
    double re_factor = (max_re - min_re) / (width - 1);
    double im_factor = (max_im - min_im) / (height - 1);

    // Configurar dinámicamente el scheduler si fuera necesario, 
    // pero para este proyecto usaremos pragmas específicos o controlados por el sistema.
    // La especificación pide analizar static, dynamic, guided.

    #pragma omp parallel for collapse(2) schedule(runtime)
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            double c_re = min_re + x * re_factor;
            double c_im = max_im - y * im_factor;
            double z_re = c_re, z_im = c_im;
            int iter = 0;
            for (iter = 0; iter < max_iter; ++iter) {
                double z_re2 = z_re * z_re, z_im2 = z_im * z_im;
                if (z_re2 + z_im2 > 4.0) break;
                z_im = 2.0 * z_re * z_im + c_im;
                z_re = z_re2 - z_im2 + c_re;
            }

            int idx = (y * width + x) * 3;
            // Mapeo simple de color
            if (iter == max_iter) {
                image[idx] = 0;
                image[idx + 1] = 0;
                image[idx + 2] = 0;
            } else {
                image[idx] = (iter % 8) * 32;
                image[idx + 1] = (iter % 16) * 16;
                image[idx + 2] = (iter % 32) * 8;
            }
        }
    }
}
