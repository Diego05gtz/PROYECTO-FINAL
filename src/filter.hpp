#ifndef FILTER_HPP
#define FILTER_HPP

#include <vector>

void apply_gaussian_blur(const std::vector<unsigned char>& input, std::vector<unsigned char>& output, int width, int height);

#endif
