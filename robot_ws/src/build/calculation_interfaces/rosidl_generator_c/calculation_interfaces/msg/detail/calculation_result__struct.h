// NOLINT: This file starts with a BOM since it contain non-ASCII characters
// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from calculation_interfaces:msg/CalculationResult.idl
// generated code does not contain a copyright notice

#ifndef CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__STRUCT_H_
#define CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'raw_expression'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/CalculationResult in the package calculation_interfaces.
/**
  * 计算结果消息
  * result: 计算结果数值，如 4.0
 */
typedef struct calculation_interfaces__msg__CalculationResult
{
  rosidl_runtime_c__String raw_expression;
  double result;
} calculation_interfaces__msg__CalculationResult;

// Struct for a sequence of calculation_interfaces__msg__CalculationResult.
typedef struct calculation_interfaces__msg__CalculationResult__Sequence
{
  calculation_interfaces__msg__CalculationResult * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} calculation_interfaces__msg__CalculationResult__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__STRUCT_H_
