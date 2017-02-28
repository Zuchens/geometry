cmake_minimum_required(VERSION 3.6)
project(Geo)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    lab_1.c
    predicates.c)

add_executable(Geo ${SOURCE_FILES})