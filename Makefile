CXX = g++
CXXFLAGS = -O3 -fopenmp -std=c++17
LDFLAGS = -fopenmp

SRC_DIR = src
OBJ_DIR = obj
SOURCES = $(wildcard $(SRC_DIR)/*.cpp)
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SOURCES))
TARGET = proyecto

all: $(TARGET)

$(TARGET): $(OBJECTS)
	@$(CXX) $(LDFLAGS) -o $@ $^

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	@$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	@rm -rf $(OBJ_DIR) $(TARGET) *.ppm

.PHONY: all clean
