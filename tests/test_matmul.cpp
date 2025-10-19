#include <iostream>
#include <vector>
#include <cassert>

using std::vector;

// Function prototype for matmul
vector<vector<double>> matmul(const vector<vector<double>>& A, const vector<vector<double>>& B);

// Unit tests for matmul function
void test_matmul() {
    // Test case 1: Simple 2x2 multiplication
    vector<vector<double>> A = {{1, 2}, {3, 4}};
    vector<vector<double>> B = {{5, 6}, {7, 8}};
    vector<vector<double>> expected = {{19, 22}, {43, 50}};
    auto result = matmul(A, B);
    assert(result == expected);

    // Test case 2: Identity matrix
    vector<vector<double>> I = {{1, 0}, {0, 1}};
    result = matmul(A, I);
    assert(result == A);

    // Test case 3: Multiplying by zero matrix
    vector<vector<double>> Z = {{0, 0}, {0, 0}};
    expected = {{0, 0}, {0, 0}};
    result = matmul(A, Z);
    assert(result == expected);

    // Test case 4: Incompatible dimensions
    vector<vector<double>> C = {{1, 2, 3}};
    try {
        matmul(A, C);
        assert(false); // Should not reach here
    } catch (const std::runtime_error& e) {
        assert(true); // Expected exception
    }

    std::cout << "All tests passed!" << std::endl;
}

int main() {
    test_matmul();
    return 0;
}