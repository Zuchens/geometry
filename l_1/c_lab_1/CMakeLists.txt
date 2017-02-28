cmake_minimum_required(VERSION 3.6)
project(c_lab_1)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    100_points.csv
    10_14_points.csv
    circle.csv
    lab_1.c
    line.csv
    predicates.c)

add_executable(c_lab_1 ${SOURCE_FILES})