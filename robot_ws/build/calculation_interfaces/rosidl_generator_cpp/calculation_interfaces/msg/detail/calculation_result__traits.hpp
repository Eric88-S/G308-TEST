// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from calculation_interfaces:msg/CalculationResult.idl
// generated code does not contain a copyright notice

#ifndef CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__TRAITS_HPP_
#define CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "calculation_interfaces/msg/detail/calculation_result__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace calculation_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CalculationResult & msg,
  std::ostream & out)
{
  out << "{";
  // member: raw_expression
  {
    out << "raw_expression: ";
    rosidl_generator_traits::value_to_yaml(msg.raw_expression, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CalculationResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: raw_expression
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "raw_expression: ";
    rosidl_generator_traits::value_to_yaml(msg.raw_expression, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result: ";
    rosidl_generator_traits::value_to_yaml(msg.result, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CalculationResult & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace calculation_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use calculation_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const calculation_interfaces::msg::CalculationResult & msg,
  std::ostream & out, size_t indentation = 0)
{
  calculation_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use calculation_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const calculation_interfaces::msg::CalculationResult & msg)
{
  return calculation_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<calculation_interfaces::msg::CalculationResult>()
{
  return "calculation_interfaces::msg::CalculationResult";
}

template<>
inline const char * name<calculation_interfaces::msg::CalculationResult>()
{
  return "calculation_interfaces/msg/CalculationResult";
}

template<>
struct has_fixed_size<calculation_interfaces::msg::CalculationResult>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<calculation_interfaces::msg::CalculationResult>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<calculation_interfaces::msg::CalculationResult>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__TRAITS_HPP_
