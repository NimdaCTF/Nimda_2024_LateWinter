cmake_minimum_required (VERSION 3.13)
project (libdeflate)

file(GLOB_RECURSE SOURCE
	"common/**/*.c"
	"common/**/*.h"
	"lib/*.c"
	"lib/*.h"
)

add_library(libdeflate libdeflate.h ${SOURCE})
target_include_directories(libdeflate PUBLIC "${CMAKE_PROJECT_DIR}")
