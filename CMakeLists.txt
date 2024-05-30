cmake_minimum_required(VERSION 3.20)

project(NFA2DFA LANGUAGES CXX)

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
target_include_directories(NFA2DFA PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(NFA2DFA Automaton)