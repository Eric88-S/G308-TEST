cmake_minimum_required(VERSION 3.8)
project(local_sensing_node)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(quadrotor_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(PCL REQUIRED)
find_package(Eigen3 REQUIRED)

add_executable(pcl_render_node src/pointcloud_render_node.cpp)

ament_target_dependencies(pcl_render_node
  rclcpp
  sensor_msgs
  nav_msgs
  geometry_msgs
  quadrotor_msgs
  pcl_conversions
)

target_include_directories(pcl_render_node SYSTEM PRIVATE
  ${PCL_INCLUDE_DIRS}
  ${EIGEN3_INCLUDE_DIRS}
)

target_link_libraries(pcl_render_node
  ${PCL_LIBRARIES}
)

install(
  TARGETS pcl_render_node
  EXPORT ${PROJECT_NAME}_export
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

ament_package()
