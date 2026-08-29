// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from status_interfaces:msg/StudentInfo.idl
// generated code does not contain a copyright notice

#ifndef STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__TRAITS_HPP_
#define STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "status_interfaces/msg/detail/student_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace status_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const StudentInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: student_id
  {
    out << "student_id: ";
    rosidl_generator_traits::value_to_yaml(msg.student_id, out);
    out << ", ";
  }

  // member: student_name
  {
    out << "student_name: ";
    rosidl_generator_traits::value_to_yaml(msg.student_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const StudentInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: student_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "student_id: ";
    rosidl_generator_traits::value_to_yaml(msg.student_id, out);
    out << "\n";
  }

  // member: student_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "student_name: ";
    rosidl_generator_traits::value_to_yaml(msg.student_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const StudentInfo & msg, bool use_flow_style = false)
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

}  // namespace status_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use status_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const status_interfaces::msg::StudentInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  status_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use status_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const status_interfaces::msg::StudentInfo & msg)
{
  return status_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<status_interfaces::msg::StudentInfo>()
{
  return "status_interfaces::msg::StudentInfo";
}

template<>
inline const char * name<status_interfaces::msg::StudentInfo>()
{
  return "status_interfaces/msg/StudentInfo";
}

template<>
struct has_fixed_size<status_interfaces::msg::StudentInfo>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<status_interfaces::msg::StudentInfo>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<status_interfaces::msg::StudentInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__TRAITS_HPP_
