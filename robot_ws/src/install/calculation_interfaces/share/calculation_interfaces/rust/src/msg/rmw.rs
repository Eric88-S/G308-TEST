#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "calculation_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__calculation_interfaces__msg__CalculationResult() -> *const std::ffi::c_void;
}

#[link(name = "calculation_interfaces__rosidl_generator_c")]
extern "C" {
    fn calculation_interfaces__msg__CalculationResult__init(msg: *mut CalculationResult) -> bool;
    fn calculation_interfaces__msg__CalculationResult__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<CalculationResult>, size: usize) -> bool;
    fn calculation_interfaces__msg__CalculationResult__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<CalculationResult>);
    fn calculation_interfaces__msg__CalculationResult__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<CalculationResult>, out_seq: *mut rosidl_runtime_rs::Sequence<CalculationResult>) -> bool;
}

// Corresponds to calculation_interfaces__msg__CalculationResult
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// 计算结果消息
/// result: 计算结果数值，如 4.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct CalculationResult {

    // This member is not documented.
    #[allow(missing_docs)]
    pub raw_expression: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: f64,

}



impl Default for CalculationResult {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !calculation_interfaces__msg__CalculationResult__init(&mut msg as *mut _) {
        panic!("Call to calculation_interfaces__msg__CalculationResult__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for CalculationResult {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { calculation_interfaces__msg__CalculationResult__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { calculation_interfaces__msg__CalculationResult__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { calculation_interfaces__msg__CalculationResult__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for CalculationResult {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for CalculationResult where Self: Sized {
  const TYPE_NAME: &'static str = "calculation_interfaces/msg/CalculationResult";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__calculation_interfaces__msg__CalculationResult() }
  }
}


