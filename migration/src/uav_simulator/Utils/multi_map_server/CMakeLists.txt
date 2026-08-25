cmake_minimum_required(VERSION 3.8)
project(multi_map_server)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(pose_utils REQUIRED)
find_package(Armadillo REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/MultiOccupancyGrid.msg"
  "msg/MultiSparseMap3D.msg"
  "msg/SparseMap3D.msg"
  "msg/VerticalOccupancyGridList.msg"
  DEPENDENCIES nav_msgs geometry_msgs std_msgs
)

include_directories(include)

add_executable(multi_map_visualization src/multi_map_visualization.cc)

rosidl_get_typesupport_target(cpp_typesupport_target ${PROJECT_NAME} "rosidl_typesupport_cpp")
target_link_libraries(multi_map_visualization "${cpp_typesupport_target}")

ament_target_dependencies(multi_map_visualization
  rclcpp
  nav_msgs
  geometry_msgs
  std_msgs
  sensor_msgs
  pose_utils
)

target_link_libraries(multi_map_visualization
  ${ARMADILLO_LIBRARIES}
)

install(
  TARGETS multi_map_visualization
  EXPORT ${PROJECT_NAME}_export
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

# Install headers
install(
  DIRECTORY include/
  DESTINATION include
)

ament_export_include_directories(include)
ament_export_dependencies(
  rclcpp
  nav_msgs
  geometry_msgs
  std_msgs
)

ament_package()
