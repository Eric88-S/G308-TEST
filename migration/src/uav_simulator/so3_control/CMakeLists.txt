cmake_minimum_required(VERSION 3.8)
project(so3_control)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(quadrotor_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(cmake_utils REQUIRED)
find_package(Eigen3 REQUIRED)

include_directories(include)
include_directories(${EIGEN3_INCLUDE_DIRS})

# SO3Control library (no ROS deps)
add_library(SO3Control src/SO3Control.cpp)
target_include_directories(SO3Control
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
ament_target_dependencies(SO3Control
  Eigen3
)

# so3_control node (converted from nodelet)
add_executable(so3_control_node src/so3_control_nodelet.cpp)
target_include_directories(so3_control_node
  PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
ament_target_dependencies(so3_control_node
  rclcpp
  nav_msgs
  quadrotor_msgs
  tf2
  tf2_geometry_msgs
  sensor_msgs
  std_msgs
  Eigen3
)
target_link_libraries(so3_control_node
  SO3Control
)

# Control example
add_executable(control_example src/control_example.cpp)
ament_target_dependencies(control_example
  rclcpp
  quadrotor_msgs
)

install(
  TARGETS SO3Control so3_control_node control_example
  EXPORT ${PROJECT_NAME}_export
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

ament_export_targets(${PROJECT_NAME}_export HAS_LIBRARY_TARGET)
ament_export_include_directories(include)
ament_export_dependencies(
  rclcpp
  Eigen3
)

ament_package()
