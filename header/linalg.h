#ifndef LINALG_H
#define LINALG_H

#include <iostream>
#include <vector>
#include <random>
#include <iomanip>
#include <stdexcept>

using std::vector;

class LinAlg {
public:
    using Matrix = vector<vector<double>>;

    // Naive matrix multiplication: C = A * B
    static Matrix matmul(const Matrix& A, const Matrix& B);

    // Naive 1D "valid" convolution: output length = input.size() - kernel.size() + 1
    static vector<double> conv1d(const vector<double>& input, const vector<double>& kernel);
};

#endif // LINALG_H