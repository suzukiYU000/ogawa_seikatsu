# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.25

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311

# Include any dependencies generated for this target.
include examples/CMakeFiles/tri_and_gs_test.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/CMakeFiles/tri_and_gs_test.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/tri_and_gs_test.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/tri_and_gs_test.dir/flags.make

examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o: examples/CMakeFiles/tri_and_gs_test.dir/flags.make
examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o: /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/examples/tri_and_gs_test.cpp
examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o: examples/CMakeFiles/tri_and_gs_test.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o"
	cd /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o -MF CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o.d -o CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o -c /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/examples/tri_and_gs_test.cpp

examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.i"
	cd /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/examples/tri_and_gs_test.cpp > CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.i

examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.s"
	cd /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/examples/tri_and_gs_test.cpp -o CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.s

# Object files for target tri_and_gs_test
tri_and_gs_test_OBJECTS = \
"CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o"

# External object files for target tri_and_gs_test
tri_and_gs_test_EXTERNAL_OBJECTS =

tri_and_gs_test: examples/CMakeFiles/tri_and_gs_test.dir/tri_and_gs_test.cpp.o
tri_and_gs_test: examples/CMakeFiles/tri_and_gs_test.dir/build.make
tri_and_gs_test: libydlidar_sdk.a
tri_and_gs_test: examples/CMakeFiles/tri_and_gs_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../tri_and_gs_test"
	cd /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tri_and_gs_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/tri_and_gs_test.dir/build: tri_and_gs_test
.PHONY : examples/CMakeFiles/tri_and_gs_test.dir/build

examples/CMakeFiles/tri_and_gs_test.dir/clean:
	cd /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples && $(CMAKE_COMMAND) -P CMakeFiles/tri_and_gs_test.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/tri_and_gs_test.dir/clean

examples/CMakeFiles/tri_and_gs_test.dir/depend:
	cd /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311 && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/examples /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311 /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/examples/CMakeFiles/tri_and_gs_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/tri_and_gs_test.dir/depend

