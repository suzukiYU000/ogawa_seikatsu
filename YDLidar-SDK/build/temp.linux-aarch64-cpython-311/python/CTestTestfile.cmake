# CMake generated Testfile for 
# Source directory: /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/python
# Build directory: /home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/home/ogawa/ogawa_ws/ogawa_seikatsu/.venv/bin/python3" "/home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=:/home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/build/temp.linux-aarch64-cpython-311/python" _BACKTRACE_TRIPLES "/home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/python/CMakeLists.txt;42;add_test;/home/ogawa/ogawa_ws/ogawa_seikatsu/YDLidar-SDK/python/CMakeLists.txt;0;")
subdirs("examples")
