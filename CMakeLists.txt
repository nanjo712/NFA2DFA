cmake_minimum_required(VERSION 3.20)

project(NFA2DFA LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(
    Automaton
    STATIC
    src/Automaton.cpp
)
target_include_directories(Automaton PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)