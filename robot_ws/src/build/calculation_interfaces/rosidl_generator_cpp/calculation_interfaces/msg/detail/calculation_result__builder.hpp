// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from calculation_interfaces:msg/CalculationResult.idl
// generated code does not contain a copyright notice

#ifndef CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__BUILDER_HPP_
#define CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "calculation_interfaces/msg/detail/calculation_result__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace calculation_interfaces
{

namespace msg
{

namespace builder
{

class Init_CalculationResult_result
{
public:
  explicit Init_CalculationResult_result(::calculation_interfaces::msg::CalculationResult & msg)
  : msg_(msg)
  {}
  ::calculation_interfaces::msg::CalculationResult result(::calculation_interfaces::msg::CalculationResult::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::calculation_interfaces::msg::CalculationResult msg_;
};

class Init_CalculationResult_raw_expression
{
public:
  Init_CalculationResult_raw_expression()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CalculationResult_result raw_expression(::calculation_interfaces::msg::CalculationResult::_raw_expression_type arg)
  {
    msg_.raw_expression = std::move(arg);
    return Init_CalculationResult_result(msg_);
  }

private:
  ::calculation_interfaces::msg::CalculationResult msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::calculation_interfaces::msg::CalculationResult>()
{
  return calculation_interfaces::msg::builder::Init_CalculationResult_raw_expression();
}

}  // namespace calculation_interfaces

#endif  // CALCULATION_INTERFACES__MSG__DETAIL__CALCULATION_RESULT__BUILDER_HPP_
