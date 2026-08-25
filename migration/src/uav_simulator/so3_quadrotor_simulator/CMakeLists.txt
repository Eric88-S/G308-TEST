cmake_minimum_required(VERSION 3.8)
project(so3_quadrotor_simulator)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(quadrotor_msgs REQUIRED)
find_package(uav_utils REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(cmake_utils REQUIRED)
find_package(Eigen3 REQUIRED)

include_directories(include)
include_directories(${EIGEN3_INCLUDE_DIRS})

# Quadrotor dynamics library (no ROS deps)
add_library(quadrotor_dynamics src/dynamics/Quadrotor.cpp)
target_include_directories(quadrotor_dynamics
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)
ament_target_dependencies(quadrotor_dynamics
  Eigen3
)

# Main simulator node
add_executable(quadrotor_simulator_so3
  src/quadrotor_simulator_so3.cpp)

ament_target_dependencies(quadrotor_simulator_so3
  rclcpp
  quadrotor_msgs
  uav_utils
  nav_msgs
  sensor_msgs
  geometry_msgs
  Eigen3
)

target_link_libraries(quadrotor_simulator_so3
  quadrotor_dynamics
)

install(
  TARGETS quadrotor_dynamics quadrotor_simulator_so3
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
