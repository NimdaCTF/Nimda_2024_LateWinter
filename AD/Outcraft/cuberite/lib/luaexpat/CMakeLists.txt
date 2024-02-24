cmake_minimum_required (VERSION 3.13)
project (luaexpat)

include_directories ("${PROJECT_SOURCE_DIR}/../expat")
include_directories ("${PROJECT_SOURCE_DIR}/../lua/src")

add_library(luaexpat lxplib.cpp lxplib.h)
target_link_libraries(luaexpat expat)
