cmake_minimum_required(VERSION 3.8)
project(cmake_utils)

find_package(ament_cmake REQUIRED)

# Install cmake modules so other packages can find them
set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
file(GLOB CMAKE_UTILS_FILES cmake/*.cmake)

install(
  FILES ${CMAKE_UTILS_FILES}
  DESTINATION share/${PROJECT_NAME}/cmake
)

# Also install custom Find*.cmake modules
file(GLOB CMAKE_MODULES_FILES cmake_modules/*.cmake)
install(
  FILES ${CMAKE_MODULES_FILES}
  DESTINATION share/${PROJECT_NAME}/cmake_modules
)

ament_package()
