#include <iostream>
#include <fstream>
#include <string>
#include <omp.h>
#include <unistd.h>

void print_cpu_info() {
    std::ifstream cpuinfo("/proc/cpuinfo");
    std::string line;
    std::string model_name = "Unknown";
    int physical_cores = 0;
    int siblings = 0;

    if (cpuinfo.is_open()) {
        while (std::getline(cpuinfo, line)) {
            if (line.substr(0, 10) == "model name") {
                model_name = line.substr(line.find(":") + 2);
            }
            if (line.substr(0, 9) == "cpu cores") {
                physical_cores = std::stoi(line.substr(line.find(":") + 2));
            }
            if (line.substr(0, 8) == "siblings") {
                siblings = std::stoi(line.substr(line.find(":") + 2));
            }
        }
        cpuinfo.close();
    }

    std::cout << "========================================" << std::endl;
    std::cout << "        HARDWARE SPECIFICATIONS         " << std::endl;
    std::cout << "========================================" << std::endl;
    std::cout << "CPU Model:      " << model_name << std::endl;
    std::cout << "Physical Cores: " << physical_cores << std::endl;
    std::cout << "Logical Cores:  " << siblings << " (Threads)" << std::endl;
    std::cout << "OpenMP Max Thr: " << omp_get_max_threads() << std::endl;
    
    // Cache info
    for (int i = 0; i < 4; ++i) {
        std::string path = "/sys/devices/system/cpu/cpu0/cache/index" + std::to_string(i) + "/";
        std::ifstream level_file(path + "level");
        std::ifstream size_file(path + "size");
        std::ifstream type_file(path + "type");
        if (level_file.is_open() && size_file.is_open()) {
            std::string level, size, type;
            std::getline(level_file, level);
            std::getline(size_file, size);
            std::getline(type_file, type);
            std::cout << "Cache L" << level << " (" << type << "): " << size << std::endl;
        }
    }

    // Memoria
    std::ifstream meminfo("/proc/meminfo");
    if (meminfo.is_open()) {
        while (std::getline(meminfo, line)) {
            if (line.substr(0, 8) == "MemTotal") {
                std::cout << "RAM Total:     " << line.substr(line.find(":") + 2) << std::endl;
                break;
            }
        }
        meminfo.close();
    }
    
    char hostname[1024];
    gethostname(hostname, 1024);
    std::cout << "Hostname:       " << hostname << std::endl;
    std::cout << "========================================" << std::endl;
}

int main() {
    print_cpu_info();
    return 0;
}
