cmake_minimum_required(VERSION 3.8)
project(uav_utils)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(cmake_utils REQUIRED)
find_package(Eigen3 REQUIRED)

# Header-only library — install headers
install(
  DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)

# Build and run tests if testing enabled
if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(${PROJECT_NAME}_test
    src/uav_utils_test.cpp
  )
  target_include_directories(${PROJECT_NAME}_test PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    ${EIGEN3_INCLUDE_DIRS}
  )
  ament_target_dependencies(${PROJECT_NAME}_test
    nav_msgs
    geometry_msgs
  )
  target_link_libraries(${PROJECT_NAME}_test
    ${EIGEN3_LIBRARIES}
  )
endif()

ament_package()
