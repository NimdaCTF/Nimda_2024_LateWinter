cmake_minimum_required (VERSION 3.13)
project (expat)

file(GLOB SOURCE
    "*.c"
    "*.h"
)

# Set files to go to a "Sources" folder in MSVC project files:
if (MSVC)
	source_group("Sources" FILES ${SOURCE})
endif()

add_library(expat ${SOURCE})

# The Expat library is linked in statically, make the source files aware of that.
# PUBLIC to propagate the define to everyone including our header, as well as our own sources:
target_compile_definitions(expat PUBLIC XML_STATIC)
