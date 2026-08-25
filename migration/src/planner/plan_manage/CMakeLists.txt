cmake_minimum_required(VERSION 3.8)
project(ego_planner)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)
find_package(quadrotor_msgs REQUIRED)
find_package(plan_env REQUIRED)
find_package(path_searching REQUIRED)
find_package(bspline_opt REQUIRED)
find_package(traj_utils REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(PCL REQUIRED COMPONENTS common)

# Custom messages
set(msg_files
  msg/Bspline.msg
  msg/DataDisp.msg
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES std_msgs geometry_msgs builtin_interfaces
)

include_directories(
  include
  ${EIGEN3_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
)

# Main planner node
add_executable(ego_planner_node
  src/ego_planner_node.cpp
  src/ego_replan_fsm.cpp
  src/planner_manager.cpp
)

target_include_directories(ego_planner_node
  PRIVATE
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
)

ament_target_dependencies(ego_planner_node
  rclcpp
  std_msgs
  builtin_interfaces
  geometry_msgs
  nav_msgs
  sensor_msgs
  visualization_msgs
  quadrotor_msgs
  plan_env
  path_searching
  bspline_opt
  traj_utils
  cv_bridge
  Eigen3
)

target_link_libraries(ego_planner_node
  ${PCL_LIBRARIES}
)

rosidl_target_interfaces(ego_planner_node
  ${PROJECT_NAME} "rosidl_typesupport_cpp"
)

# Traj server node
add_executable(traj_server
  src/traj_server.cpp
)

ament_target_dependencies(traj_server
  rclcpp
  std_msgs
  builtin_interfaces
  geometry_msgs
  nav_msgs
  visualization_msgs
  quadrotor_msgs
  bspline_opt
  Eigen3
)

target_link_libraries(traj_server
  ${PCL_LIBRARIES}
  ${EIGEN3_LIBRARIES}
)

rosidl_target_interfaces(traj_server
  ${PROJECT_NAME} "rosidl_typesupport_cpp"
)

# Install
install(
  DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

install(
  TARGETS ego_planner_node traj_server
  EXPORT ${PROJECT_NAME}_export
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

ament_export_targets(${PROJECT_NAME}_export HAS_LIBRARY_TARGET)
ament_export_include_directories(include)
ament_export_dependencies(
  rclcpp
  std_msgs
  plan_env
  path_searching
  bspline_opt
  traj_utils
  rosidl_default_runtime
)

ament_package()
