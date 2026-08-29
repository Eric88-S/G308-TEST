// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from calculation_interfaces:msg/CalculationResult.idl
// generated code does not contain a copyright notice
#include "calculation_interfaces/msg/detail/calculation_result__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `raw_expression`
#include "rosidl_runtime_c/string_functions.h"

bool
calculation_interfaces__msg__CalculationResult__init(calculation_interfaces__msg__CalculationResult * msg)
{
  if (!msg) {
    return false;
  }
  // raw_expression
  if (!rosidl_runtime_c__String__init(&msg->raw_expression)) {
    calculation_interfaces__msg__CalculationResult__fini(msg);
    return false;
  }
  // result
  return true;
}

void
calculation_interfaces__msg__CalculationResult__fini(calculation_interfaces__msg__CalculationResult * msg)
{
  if (!msg) {
    return;
  }
  // raw_expression
  rosidl_runtime_c__String__fini(&msg->raw_expression);
  // result
}

bool
calculation_interfaces__msg__CalculationResult__are_equal(const calculation_interfaces__msg__CalculationResult * lhs, const calculation_interfaces__msg__CalculationResult * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // raw_expression
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->raw_expression), &(rhs->raw_expression)))
  {
    return false;
  }
  // result
  if (lhs->result != rhs->result) {
    return false;
  }
  return true;
}

bool
calculation_interfaces__msg__CalculationResult__copy(
  const calculation_interfaces__msg__CalculationResult * input,
  calculation_interfaces__msg__CalculationResult * output)
{
  if (!input || !output) {
    return false;
  }
  // raw_expression
  if (!rosidl_runtime_c__String__copy(
      &(input->raw_expression), &(output->raw_expression)))
  {
    return false;
  }
  // result
  output->result = input->result;
  return true;
}

calculation_interfaces__msg__CalculationResult *
calculation_interfaces__msg__CalculationResult__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  calculation_interfaces__msg__CalculationResult * msg = (calculation_interfaces__msg__CalculationResult *)allocator.allocate(sizeof(calculation_interfaces__msg__CalculationResult), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(calculation_interfaces__msg__CalculationResult));
  bool success = calculation_interfaces__msg__CalculationResult__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
calculation_interfaces__msg__CalculationResult__destroy(calculation_interfaces__msg__CalculationResult * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    calculation_interfaces__msg__CalculationResult__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
calculation_interfaces__msg__CalculationResult__Sequence__init(calculation_interfaces__msg__CalculationResult__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  calculation_interfaces__msg__CalculationResult * data = NULL;

  if (size) {
    data = (calculation_interfaces__msg__CalculationResult *)allocator.zero_allocate(size, sizeof(calculation_interfaces__msg__CalculationResult), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = calculation_interfaces__msg__CalculationResult__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        calculation_interfaces__msg__CalculationResult__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
calculation_interfaces__msg__CalculationResult__Sequence__fini(calculation_interfaces__msg__CalculationResult__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      calculation_interfaces__msg__CalculationResult__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

calculation_interfaces__msg__CalculationResult__Sequence *
calculation_interfaces__msg__CalculationResult__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  calculation_interfaces__msg__CalculationResult__Sequence * array = (calculation_interfaces__msg__CalculationResult__Sequence *)allocator.allocate(sizeof(calculation_interfaces__msg__CalculationResult__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = calculation_interfaces__msg__CalculationResult__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
calculation_interfaces__msg__CalculationResult__Sequence__destroy(calculation_interfaces__msg__CalculationResult__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    calculation_interfaces__msg__CalculationResult__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
calculation_interfaces__msg__CalculationResult__Sequence__are_equal(const calculation_interfaces__msg__CalculationResult__Sequence * lhs, const calculation_interfaces__msg__CalculationResult__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!calculation_interfaces__msg__CalculationResult__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
calculation_interfaces__msg__CalculationResult__Sequence__copy(
  const calculation_interfaces__msg__CalculationResult__Sequence * input,
  calculation_interfaces__msg__CalculationResult__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(calculation_interfaces__msg__CalculationResult);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    calculation_interfaces__msg__CalculationResult * data =
      (calculation_interfaces__msg__CalculationResult *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!calculation_interfaces__msg__CalculationResult__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          calculation_interfaces__msg__CalculationResult__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!calculation_interfaces__msg__CalculationResult__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
