// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from calculation_interfaces:msg/CalculationResult.idl
// generated code does not contain a copyright notice

#ifndef CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__STRUCT_HPP_
#define CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__calculation_interfaces__msg__CalculationResult __attribute__((deprecated))
#else
# define DEPRECATED__calculation_interfaces__msg__CalculationResult __declspec(deprecated)
#endif

namespace calculation_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CalculationResult_
{
  using Type = CalculationResult_<ContainerAllocator>;

  explicit CalculationResult_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->raw_expression = "";
      this->result = 0.0;
    }
  }

  explicit CalculationResult_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : raw_expression(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->raw_expression = "";
      this->result = 0.0;
    }
  }

  // field types and members
  using _raw_expression_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _raw_expression_type raw_expression;
  using _result_type =
    double;
  _result_type result;

  // setters for named parameter idiom
  Type & set__raw_expression(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->raw_expression = _arg;
    return *this;
  }
  Type & set__result(
    const double & _arg)
  {
    this->result = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    calculation_interfaces::msg::CalculationResult_<ContainerAllocator> *;
  using ConstRawPtr =
    const calculation_interfaces::msg::CalculationResult_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      calculation_interfaces::msg::CalculationResult_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      calculation_interfaces::msg::CalculationResult_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__calculation_interfaces__msg__CalculationResult
    std::shared_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__calculation_interfaces__msg__CalculationResult
    std::shared_ptr<calculation_interfaces::msg::CalculationResult_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CalculationResult_ & other) const
  {
    if (this->raw_expression != other.raw_expression) {
      return false;
    }
    if (this->result != other.result) {
      return false;
    }
    return true;
  }
  bool operator!=(const CalculationResult_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CalculationResult_

// alias to use template instance with default allocator
using CalculationResult =
  calculation_interfaces::msg::CalculationResult_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace calculation_interfaces

#endif  // CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__STRUCT_HPP_
