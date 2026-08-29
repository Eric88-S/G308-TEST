// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from calculation_interfaces:msg/CalculationResult.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "calculation_interfaces/msg/detail/calculation_result__rosidl_typesupport_introspection_c.h"
#include "calculation_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "calculation_interfaces/msg/detail/calculation_result__functions.h"
#include "calculation_interfaces/msg/detail/calculation_result__struct.h"


// Include directives for member types
// Member `raw_expression`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  calculation_interfaces__msg__CalculationResult__init(message_memory);
}

void calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_fini_function(void * message_memory)
{
  calculation_interfaces__msg__CalculationResult__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_member_array[2] = {
  {
    "raw_expression",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(calculation_interfaces__msg__CalculationResult, raw_expression),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "result",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(calculation_interfaces__msg__CalculationResult, result),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_members = {
  "calculation_interfaces__msg",  // message namespace
  "CalculationResult",  // message name
  2,  // number of fields
  sizeof(calculation_interfaces__msg__CalculationResult),
  calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_member_array,  // message members
  calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_init_function,  // function to initialize message memory (memory has to be allocated)
  calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_type_support_handle = {
  0,
  &calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_calculation_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, calculation_interfaces, msg, CalculationResult)() {
  if (!calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_type_support_handle.typesupport_identifier) {
    calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &calculation_interfaces__msg__CalculationResult__rosidl_typesupport_introspection_c__CalculationResult_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
