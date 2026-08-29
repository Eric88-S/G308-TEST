// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from status_interfaces:msg/StudentInfo.idl
// generated code does not contain a copyright notice

#ifndef STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__STRUCT_H_
#define STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'student_id'
// Member 'student_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/StudentInfo in the package status_interfaces.
typedef struct status_interfaces__msg__StudentInfo
{
  rosidl_runtime_c__String student_id;
  rosidl_runtime_c__String student_name;
} status_interfaces__msg__StudentInfo;

// Struct for a sequence of status_interfaces__msg__StudentInfo.
typedef struct status_interfaces__msg__StudentInfo__Sequence
{
  status_interfaces__msg__StudentInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} status_interfaces__msg__StudentInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__STRUCT_H_
