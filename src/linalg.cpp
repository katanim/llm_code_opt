#include "linalg.h"
#include <stdexcept>
#include <vector>

LinAlg::Matrix LinAlg::matmul(const LinAlg::Matrix& A, const LinAlg::Matrix& B) {
    if (A.empty() || B.empty()) throw std::runtime_error("Empty matrix");
    std::size_t m = A.size();
    std::size_t k = A[0].size();
    for (const auto& row : A) if (row.size() != k) throw std::runtime_error("Inconsistent A row size");
    std::size_t k2 = B.size();
    std::size_t n = B[0].size();
    for (const auto& row : B) if (row.size() != n) throw std::runtime_error("Inconsistent B row size");
    if (k != k2) throw std::runtime_error("Inner dimensions do not match for multiplication");

    LinAlg::Matrix C(m, std::vector<double>(n, 0.0));
    for (std::size_t i = 0; i < m; ++i) {
        for (std::size_t j = 0; j < n; ++j) {
            double sum = 0.0;
            for (std::size_t t = 0; t < k; ++t) {
                sum += A[i][t] * B[t][j];
            }
            C[i][j] = sum;
        }
    }
    return C;
}

std::vector<double> LinAlg::conv1d(const std::vector<double>& input, const std::vector<double>& kernel) {
    if (input.empty() || kernel.empty()) throw std::runtime_error("Empty input or kernel");
    std::size_t n = input.size();
    std::size_t k = kernel.size();
    if (k > n) return {}; // no valid outputs
    std::size_t out_len = n - k + 1;
    std::vector<double> out(out_len, 0.0);
    for (std::size_t i = 0; i < out_len; ++i) {
        double sum = 0.0;
        for (std::size_t j = 0; j < k; ++j) {
            sum += input[i + j] * kernel[j];
        }
        out[i] = sum;
    }
    return out;
}