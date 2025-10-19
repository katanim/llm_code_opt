cmake_minimum_required(VERSION 3.10)

project(llm_code_opt VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Header include directory
set(HEADER_DIR "${PROJECT_SOURCE_DIR}/header")

# Build linalg as a library from src/linalg.cpp
add_library(linalg STATIC
    src/linalg.cpp
)

target_include_directories(linalg
    PUBLIC
        ${HEADER_DIR}
)

# Executable
add_executable(llm_code_opt
    src/main.cpp
)

target_link_libraries(llm_code_opt
    PRIVATE
        linalg
)

#only add if tests/CMakeLists.txt exists
if(EXISTS "${CMAKE_SOURCE_DIR}/tests/CMakeLists.txt")
    enable_testing()
    add_subdirectory(tests)
endif()