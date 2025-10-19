#include <iostream>
#include <vector>
#include <random>
#include <iomanip>
#include <stdexcept>
#include "linalg.h"

using std::vector;

// Optional: small example main demonstrating usage
int main() {
    // Example usage (can be removed)
    LinAlg::Matrix A = {{1,2,3},{4,5,6}};
    LinAlg::Matrix B = {{7,8},{9,10},{11,12}};
    auto C = LinAlg::matmul(A,B);
    std::cout << "Result of matmul:\n";
    for (const auto& row : C) {
        for (double v : row) std::cout << v << ' ';
        std::cout << '\n';
    }

    vector<double> x = {1,2,3,4,5};
    vector<double> k = {1,0,-1};
    auto y = LinAlg::conv1d(x,k);
    std::cout << "Result of conv1d:\n";
    for (double v : y) std::cout << v << ' ';
    std::cout << '\n';

    return 0;
}