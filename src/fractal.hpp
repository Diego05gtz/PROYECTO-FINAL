#ifndef FRACTAL_HPP
#define FRACTAL_HPP

#include <vector>
#include <string>

struct Color {
    unsigned char r, g, b;
};

void generate_mandelbrot(std::vector<unsigned char>& image, int width, int height, int max_iter, const std::string& schedule_type, int chunk_size);

#endif
