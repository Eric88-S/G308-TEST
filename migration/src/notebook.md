# ROS2 迁移错题本

> 记录我（学习者）在迁移练习中写错的地方。

---

### 1. `make_shared` 拼写 + 命名空间写法

-  原本：`std::make_shred<rclcpp.node>()`
-  应该：`std::make_shared<rclcpp::Node>("waypoint_generator", options)`

---

### 2. 发布者：函数名 + 尖括号里装什么

-  原本：`g_node->create_subscribtion<rclcpp.node>()`
-  应该：`g_node->create_publisher<nav_msgs::msg::Path>("waypoints", 50)`
-  记：发布用 `create_publisher`，尖括号 `<>` 里装「消息类型」，不是节点类型。

---

### 3. 发布者声明：大小写 + 消息类型 + `::SharedPtr`

-  原本：`rclcpp::publisher<sensor_msgs::msg::PoseArray> pub1;`
-  应该：`rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub1;`
-  记：`Publisher` 大写 P；结尾必须 `::SharedPtr`；消息类型要对。

---

### 4. 订阅者：函数名 + 尖括号不能空

-  原本：`g_node->create_subscriber<>("goal", 10, goal_callback);`
-  应该：`auto sub2 = g_node->create_subscription<geometry_msgs::msg::PoseStamped>("goal", 10, goal_callback);`
-  记：订阅用 `create_subscription`（不是 subscriber）；尖括号里要写消息类型；推荐用 `auto`。

---

### 5. 参数声明：字符串加引号 + 记得两步

-  原本：`g_node->declare_parameter<std::string>("waypoint_type",manual)`
-  应该：
  ```cpp
  g_node->declare_parameter<std::string>("waypoint_type", "manual");
  waypoint_type = g_node->get_parameter("waypoint_type").as_string();
  ```
-  记：字符串字面量要 `"..."`；声明后还要 `get_parameter` 读出来。

---

### 6. 参数读取：单数 + 拼接用 `+`

-  原本：`ok=g_node->get_parameters(seg_str="yaw",yaw)`
-  应该：`bool ok = g_node->get_parameter(seg_str + "yaw", yaw);`
-  记：`get_parameter`（不加 s）；字符串拼接用 `+`，不是 `=`。

---

### 7. include 头文件：加 `/msg/` + 拼写

-  原本：`#include <sensor_msgs/point_clud2.hpp>`
-  应该：`#include <sensor_msgs/msg/point_cloud2.hpp>`
-  记：路径里加 `msg/`；`cloud`（云）不是 `clud`。

---

### 8. 类型名保持驼峰（重点！）

-  原本：`quadrotor_msgs::msg::position_command`
-  应该：`quadrotor_msgs::msg::PositionCommand`
-  记：**`#include` 文件名用蛇形（`position_command.hpp`），代码里类型名用驼峰（`PositionCommand`）。**

---

### 9. Duration 别忘参数

-  原本：`rclcpp::Duration::from_seconds()`
-  应该：`rclcpp::Duration::from_seconds(time_of_start)`
-  记：`from_seconds` 括号里要传时长（秒数）。

---

### 10. 拼写：visualization_msgs

-  原本：`visualizatin_msgs::msg::Marker`
-  应该：`visualization_msgs::msg::Marker`
-  记：`visualization` = vi-su-a-li-**za-tion**（中间有 o）。

---

### 11. 尖括号里装「消息类型」，不是 subscriber/node

-  原本：`g_node->create_subscription<rclcpp::subscriber>("cmd", 100, cmd_callback)`
-  应该：`g_node->create_subscription<quadrotor_msgs::msg::PositionCommand>("cmd", 100, cmd_callback)`
-  记：`create_publisher` / `create_subscription` 的 `< >` 里永远是「消息类型」。

---

### 12. 回调必须收 `ConstSharedPtr`，不是 `const&`

-  原本：`void cmd_callback(const quadrotor_msgs::msg::PositionCommand& cmd)`
-  应该：`void cmd_callback(const quadrotor_msgs::msg::PositionCommand::ConstSharedPtr cmd)`
-  记：ROS2 回调一律收智能指针 `ConstSharedPtr`，不能收普通引用 `const&`。

---

### 13. 参数：`get_param` → `get_parameter`，斜杠 → 点

-  原本：`g_node->get_param("map/x_size", _x_size)`
-  应该：`g_node->get_parameter("map.x_size", _x_size)`
-  记：函数名是 `get_parameter`（不是 get_param）；参数名用 `.` 不用 `/`。

---

### 14. 时间：`Time` 大写 + `seconds()` + 零时刻三参数

-  原本：`rclcpp::time` / `t.second()` / `rclcpp::Time(0)`
-  应该：`rclcpp::Time` / `t.seconds()` / `rclcpp::Time(0, 0, RCL_ROS_TIME)`
-  记：`Time` 大写 T；`seconds()` 有 s；`Time(0, 0, RCL_ROS_TIME)` 三个参数。

---

### 15. 发布用箭头 `->`，时间用 `get_clock()->now()`

-  原本：`pub2.publish(arr);` 和 `ros::Time::now()`
-  应该：`pub2->publish(arr);` 和 `g_node->get_clock()->now()`
-  记：`pub2` 是指针，用 `->`；`ros::Time::now()` 全改成 `g_node->get_clock()->now()`。

---

## 常见病根总结（下次先自查这几条）

1. **拼写/大小写**：`make_shared`、`Publisher`（大写）、`cloud`、`visualization`、`rclcpp::Time`（大写 T）。
2. **尖括号 `<>` 忘装消息类型**（或装错成 `rclcpp::subscriber` / 节点类型）。
3. **函数名记混**：`create_subscription`（不是 subscriber）、`get_parameter`（不是 get_param）。
4. **字符串**：忘加引号 `"..."`；拼接用 `+` 不是 `=`。
5. **`::SharedPtr` 老是漏**：发布者/订阅者声明结尾必须有它。
6. **回调收 `ConstSharedPtr`**：不是 `const&`（ROS2 回调必须收智能指针）。
7. **指针用箭头 `->`**：`pub->publish(...)`，不是 `pub.publish(...)`。
8. **文件名 vs 类型名**：`#include` 蛇形，`::msg::` 驼峰。
9. **参数名**：`/` 换成 `.`。
