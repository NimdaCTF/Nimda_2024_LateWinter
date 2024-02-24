cmake_minimum_required (VERSION 3.13)
project (lua)

# Lua needs to be linked dynamically on Windows and statically on *nix, so that LuaRocks work:
if (WIN32)
	add_library(lualib SHARED)

	target_compile_definitions(lualib PUBLIC LUA_BUILD_AS_DLL)

	set(LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR}/Server)

	# Output the DLL into the Server subfolder, so that Cuberite can find it:
	SET_TARGET_PROPERTIES(lualib PROPERTIES
		ARCHIVE_OUTPUT_DIRECTORY                ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_DEBUG          ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE        ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_DEBUGPROFILE   ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_RELEASEPROFILE ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY                ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_DEBUG          ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_RELEASE        ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_DEBUGPROFILE   ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_RELEASEPROFILE ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY                ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_DEBUG          ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_RELEASE        ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_DEBUGPROFILE   ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_RELEASEPROFILE ${CMAKE_BINARY_DIR}/Server
	)

	set(EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR}/Server)

	set_target_properties(lualib PROPERTIES OUTPUT_NAME "lua51" PREFIX "")

	# NOTE: The DLL for each configuration is stored at the same place, thus overwriting each other.
	# This is known, however such behavior is needed for LuaRocks - they always load "lua5.1.dll" or "lua51.dll"
	# We make it work by compiling to "lua51.dll" and providing a proxy-DLL "lua5.1.dll"
	# See http://lua-users.org/wiki/LuaProxyDllFour for details
else()
	add_library(lualib STATIC)
endif()

# All .c files were renamed to .cpp so the compiler uses C++ when compiling the library,
# so that Lua uses C++ exceptions instead of setjmp / longjmp (GH #3678). Don't use set_source_files_properties
# with LANGUAGE option because clang emits a deprecation warning.

target_sources(
	lualib PRIVATE

	src/lapi.cpp
	src/lauxlib.cpp
	src/lbaselib.cpp
	src/lcode.cpp
	src/ldblib.cpp
	src/ldebug.cpp
	src/ldo.cpp
	src/ldump.cpp
	src/lfunc.cpp
	src/lgc.cpp
	src/linit.cpp
	src/liolib.cpp
	src/llex.cpp
	src/lmathlib.cpp
	src/lmem.cpp
	src/loadlib.cpp
	src/lobject.cpp
	src/lopcodes.cpp
	src/loslib.cpp
	src/lparser.cpp
	src/lstate.cpp
	src/lstring.cpp
	src/lstrlib.cpp
	src/ltable.cpp
	src/ltablib.cpp
	src/ltm.cpp
	src/lundump.cpp
	src/lvm.cpp
	src/lzio.cpp
	src/print.cpp

	src/lapi.h
	src/lcode.h
	src/ldebug.h
	src/ldo.h
	src/lfunc.h
	src/lgc.h
	src/llex.h
	src/llimits.h
	src/lmem.h
	src/lobject.h
	src/lopcodes.h
	src/lparser.h
	src/lstate.h
	src/lstring.h
	src/ltable.h
	src/ltm.h
	src/luaconf.h
	src/lundump.h
	src/lvm.h
	src/lzio.h
)

target_sources(
	lualib PUBLIC

	src/lauxlib.h
	src/lua.h
	src/lualib.h
)

# Tell Lua what dynamic loader to use (for LuaRocks):
if (UNIX)
	add_definitions(-DLUA_USE_DLOPEN)
	target_link_libraries(lualib m ${CMAKE_DL_LIBS})
endif()

# Let Lua use additional checks on its C API. This is only compiled into Debug builds:
target_compile_definitions(lualib PRIVATE LUA_USE_APICHECK)

# Lua files themselves don't need this include, but Cuberite does, so INTERFACE:
target_include_directories(lualib INTERFACE "${CMAKE_CURRENT_LIST_DIR}/src")

# If not crosscompiling, build a local Lua:
if (NOT CMAKE_CROSSCOMPILING)
	add_executable(lua src/lua.cpp)
	target_link_libraries(lua lualib)

	# Output the EXE into the Server subfolder, so that it can find lua51.dll:
	SET_TARGET_PROPERTIES(lua PROPERTIES
		ARCHIVE_OUTPUT_DIRECTORY                ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_DEBUG          ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_RELEASE        ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_DEBUGPROFILE   ${CMAKE_BINARY_DIR}/Server
		ARCHIVE_OUTPUT_DIRECTORY_RELEASEPROFILE ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY                ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_DEBUG          ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_RELEASE        ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_DEBUGPROFILE   ${CMAKE_BINARY_DIR}/Server
		LIBRARY_OUTPUT_DIRECTORY_RELEASEPROFILE ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY                ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_DEBUG          ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_RELEASE        ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_DEBUGPROFILE   ${CMAKE_BINARY_DIR}/Server
		RUNTIME_OUTPUT_DIRECTORY_RELEASEPROFILE ${CMAKE_BINARY_DIR}/Server
	)

	if (MSVC)
		set_target_properties(
			lua
			PROPERTIES FOLDER Support
		)
	endif()
endif()
