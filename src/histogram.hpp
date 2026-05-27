#ifndef HISTOGRAM_HPP
#define HISTOGRAM_HPP

#include <vector>

void calculate_histogram_atomic(const std::vector<unsigned char>& image, std::vector<int>& histogram);
void calculate_histogram_reduction(const std::vector<unsigned char>& image, std::vector<int>& histogram);

#endif
