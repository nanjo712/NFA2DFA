cmake_minimum_required(VERSION 3.20)

project(NFA2DFA LANGUAGES CXX)

find_package(Python 3.10 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG)

# set output directories to build/bin
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(
    Automaton
    STATIC
    src/Automaton.cpp
)
target_include_directories(Automaton PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(
    NFA2DFA
    src/main.cpp
)
target_link_libraries(NFA2DFA PRIVATE Automaton)

if (CMAKE_BUILD_TYPE STREQUAL "Release")
    pybind11_add_module(Automaton_bindings src/Automaton_bindings.cpp)
    target_link_libraries(Automaton_bindings PRIVATE Automaton)
    target_include_directories(Automaton_bindings PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/include)

    install(TARGETS Automaton_bindings
            LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/python_package)
endif()