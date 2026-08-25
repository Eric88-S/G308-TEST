cmake_minimum_required(VERSION 3.8)
project(waypoint_generator)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall -g")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(Eigen3 REQUIRED)

include_directories(include ${EIGEN3_INCLUDE_DIRS})

add_executable(waypoint_generator src/waypoint_generator.cpp)

ament_target_dependencies(waypoint_generator
  rclcpp
  nav_msgs
  geometry_msgs
  std_msgs
)

target_link_libraries(waypoint_generator
  ${EIGEN3_LIBRARIES}
)

install(
  TARGETS waypoint_generator
  EXPORT ${PROJECT_NAME}_export
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

ament_export_targets(${PROJECT_NAME}_export HAS_LIBRARY_TARGET)
ament_export_dependencies(
  rclcpp
)

ament_package()
