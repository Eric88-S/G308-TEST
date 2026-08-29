#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to calculation_interfaces__msg__CalculationResult
/// 计算结果消息
/// raw_expression: OCR识别到的原始数学表达式，如 "12×4-132÷3"
/// result: 计算结果数值，如 4.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CalculationResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub raw_expression: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: f64,

}



impl Default for CalculationResult {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::CalculationResult::default())
  }
}

impl rosidl_runtime_rs::Message for CalculationResult {
  type RmwMsg = super::msg::rmw::CalculationResult;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        raw_expression: msg.raw_expression.as_str().into(),
        result: msg.result,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        raw_expression: msg.raw_expression.as_str().into(),
      result: msg.result,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      raw_expression: msg.raw_expression.to_string(),
      result: msg.result,
    }
  }
}


