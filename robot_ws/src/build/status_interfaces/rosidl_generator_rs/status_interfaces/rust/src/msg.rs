#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to status_interfaces__msg__StudentInfo

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StudentInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub student_id: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub student_name: std::string::String,

}



impl Default for StudentInfo {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::StudentInfo::default())
  }
}

impl rosidl_runtime_rs::Message for StudentInfo {
  type RmwMsg = super::msg::rmw::StudentInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        student_id: msg.student_id.as_str().into(),
        student_name: msg.student_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        student_id: msg.student_id.as_str().into(),
        student_name: msg.student_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      student_id: msg.student_id.to_string(),
      student_name: msg.student_name.to_string(),
    }
  }
}


