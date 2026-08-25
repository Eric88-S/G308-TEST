cmake_minimum_required(VERSION 3.8)
project(odom_visualization)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(quadrotor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(pose_utils REQUIRED)
find_package(Armadillo REQUIRED)

add_executable(odom_visualization src/odom_visualization.cpp)

ament_target_dependencies(odom_visualization
  rclcpp
  sensor_msgs
  nav_msgs
  visualization_msgs
  quadrotor_msgs
  geometry_msgs
  std_msgs
  tf2_ros
  pose_utils
)

target_link_libraries(odom_visualization
  ${ARMADILLO_LIBRARIES}
)

install(
  TARGETS odom_visualization
  EXPORT ${PROJECT_NAME}_export
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

ament_package()
