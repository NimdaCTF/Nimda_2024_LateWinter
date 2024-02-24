cmake_minimum_required (VERSION 3.13)
project (lsqlite C)

add_library(lsqlite lsqlite3.cpp)
target_link_libraries(lsqlite PUBLIC sqlite3 lualib)
