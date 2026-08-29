# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target calculation_interfaces::calculation_interfaces
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${calculation_interfaces_TARGETS}.
if(calculation_interfaces_TARGETS AND NOT TARGET calculation_interfaces::calculation_interfaces)
  add_library(calculation_interfaces::calculation_interfaces INTERFACE IMPORTED)
  set_target_properties(calculation_interfaces::calculation_interfaces PROPERTIES
    INTERFACE_LINK_LIBRARIES "${calculation_interfaces_TARGETS}")
endif()
