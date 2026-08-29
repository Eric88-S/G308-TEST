// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from status_interfaces:msg/StudentInfo.idl
// generated code does not contain a copyright notice

#ifndef STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__BUILDER_HPP_
#define STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "status_interfaces/msg/detail/student_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace status_interfaces
{

namespace msg
{

namespace builder
{

class Init_StudentInfo_student_name
{
public:
  explicit Init_StudentInfo_student_name(::status_interfaces::msg::StudentInfo & msg)
  : msg_(msg)
  {}
  ::status_interfaces::msg::StudentInfo student_name(::status_interfaces::msg::StudentInfo::_student_name_type arg)
  {
    msg_.student_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::status_interfaces::msg::StudentInfo msg_;
};

class Init_StudentInfo_student_id
{
public:
  Init_StudentInfo_student_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_StudentInfo_student_name student_id(::status_interfaces::msg::StudentInfo::_student_id_type arg)
  {
    msg_.student_id = std::move(arg);
    return Init_StudentInfo_student_name(msg_);
  }

private:
  ::status_interfaces::msg::StudentInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::status_interfaces::msg::StudentInfo>()
{
  return status_interfaces::msg::builder::Init_StudentInfo_student_id();
}

}  // namespace status_interfaces

#endif  // STATUS_INTERFACES__MSG__DETAIL__STUDENT_INFO__BUILDER_HPP_
