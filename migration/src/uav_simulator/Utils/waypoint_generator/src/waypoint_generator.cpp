#include <iostream>
#include <rclcpp/rclcpp.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/pose_array.hpp>
#include <geometry_msgs/msg/vector3.hpp>
#include <nav_msgs/msg/path.hpp>
#include "sample_waypoints.h"
#include <string>
#include <vector>
#include <deque>
#include <sstream>
#include <boost/format.hpp>
#include <Eigen/Dense>

using namespace std;
using bfmt = boost::format;

rclcpp::Node::SharedPtr g_node;
rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr pub1;
rclcpp::Publisher<geometry_msgs::msg::PoseArray>::SharedPtr pub2;
string waypoint_type = string("manual");
bool is_odom_ready = false;
nav_msgs::msg::Odometry odom;
nav_msgs::msg::Path waypoints;

// series waypoint needed
std::deque<nav_msgs::msg::Path> waypointSegments;
rclcpp::Time trigged_time = rclcpp::Time(0, 0, RCL_ROS_TIME);

void load_seg(int segid, const rclcpp::Time& time_base) {
    std::string seg_str = "seg" + std::to_string(segid) + ".";
    double yaw;
    double time_of_start = 0.0;
    RCLCPP_INFO(g_node->get_logger(), "Getting segment %d", segid);
    if (!g_node->get_parameter(seg_str + "yaw", yaw)) {
        RCLCPP_ERROR(g_node->get_logger(), "Missing parameter '%syaw'", seg_str.c_str());
        return;
    }
    if (!((yaw > -3.1499999) && (yaw < 3.14999999))) {
        RCLCPP_ERROR(g_node->get_logger(), "yaw=%.3f out of range", yaw);
        return;
    }
    if (!g_node->get_parameter(seg_str + "time_of_start", time_of_start)) {
        RCLCPP_ERROR(g_node->get_logger(), "Missing parameter '%stime_of_start'", seg_str.c_str());
        return;
    }
    if (time_of_start < 0.0) {
        RCLCPP_ERROR(g_node->get_logger(), "time_of_start < 0");
        return;
    }

    std::vector<double> ptx;
    std::vector<double> pty;
    std::vector<double> ptz;

    if (!g_node->get_parameter(seg_str + "x", ptx) ||
        !g_node->get_parameter(seg_str + "y", pty) ||
        !g_node->get_parameter(seg_str + "z", ptz)) {
        RCLCPP_ERROR(g_node->get_logger(), "Missing x/y/z parameter for segment %d", segid);
        return;
    }

    if (!ptx.size()) {
        RCLCPP_ERROR(g_node->get_logger(), "Empty x for segment %d", segid);
        return;
    }
    if (!(ptx.size() == pty.size() && ptx.size() == ptz.size())) {
        RCLCPP_ERROR(g_node->get_logger(), "x/y/z size mismatch for segment %d", segid);
        return;
    }

    nav_msgs::msg::Path path_msg;

    path_msg.header.stamp = time_base + rclcpp::Duration::from_seconds(time_of_start);

    double baseyaw = getYaw(odom.pose.pose.orientation);

    for (size_t k = 0; k < ptx.size(); ++k) {
        geometry_msgs::msg::PoseStamped pt;
        pt.pose.orientation = quaternionFromYaw(baseyaw + yaw);
        Eigen::Vector2d dp(ptx.at(k), pty.at(k));
        Eigen::Vector2d rdp;
        rdp.x() = std::cos(-baseyaw-yaw)*dp.x() + std::sin(-baseyaw-yaw)*dp.y();
        rdp.y() =-std::sin(-baseyaw-yaw)*dp.x() + std::cos(-baseyaw-yaw)*dp.y();
        pt.pose.position.x = rdp.x() + odom.pose.pose.position.x;
        pt.pose.position.y = rdp.y() + odom.pose.pose.position.y;
        pt.pose.position.z = ptz.at(k) + odom.pose.pose.position.z;
        path_msg.poses.push_back(pt);
    }

    waypointSegments.push_back(path_msg);
}

void load_waypoints(const rclcpp::Time& time_base) {
    int seg_cnt = 0;
    waypointSegments.clear();
    if (!g_node->get_parameter("segment_cnt", seg_cnt)) {
        RCLCPP_ERROR(g_node->get_logger(), "Missing parameter segment_cnt");
        return;
    }
    for (int i = 0; i < seg_cnt; ++i) {
        load_seg(i, time_base);
        if (i > 0) {
            if (!(rclcpp::Time(waypointSegments[i - 1].header.stamp) <
                  rclcpp::Time(waypointSegments[i].header.stamp))) {
                RCLCPP_ERROR(g_node->get_logger(), "Segments not in time order");
                return;
            }
        }
    }
    RCLCPP_INFO(g_node->get_logger(), "Overall load %zu segments", waypointSegments.size());
}

void publish_waypoints() {
    waypoints.header.frame_id = std::string("world");
    waypoints.header.stamp = g_node->get_clock()->now();
    pub1->publish(waypoints);
    geometry_msgs::msg::PoseStamped init_pose;
    init_pose.header = odom.header;
    init_pose.pose = odom.pose.pose;
    waypoints.poses.insert(waypoints.poses.begin(), init_pose);
    // pub2->publish(waypoints);
    waypoints.poses.clear();
}

void publish_waypoints_vis() {
    nav_msgs::msg::Path wp_vis = waypoints;
    geometry_msgs::msg::PoseArray poseArray;
    poseArray.header.frame_id = std::string("world");
    poseArray.header.stamp = g_node->get_clock()->now();

    {
        geometry_msgs::msg::Pose init_pose;
        init_pose = odom.pose.pose;
        poseArray.poses.push_back(init_pose);
    }

    for (auto it = waypoints.poses.begin(); it != waypoints.poses.end(); ++it) {
        geometry_msgs::msg::Pose p;
        p = it->pose;
        poseArray.poses.push_back(p);
    }
    pub2->publish(poseArray);
}

void odom_callback(const nav_msgs::msg::Odometry::ConstSharedPtr& msg) {
    is_odom_ready = true;
    odom = *msg;

    if (waypointSegments.size()) {
        rclcpp::Time expected_time(waypointSegments.front().header.stamp);
        if (rclcpp::Time(odom.header.stamp) >= expected_time) {
            waypoints = waypointSegments.front();

            std::stringstream ss;
            ss << bfmt("Series send %.3f from start:\n") % trigged_time.seconds();
            for (auto& pose_stamped : waypoints.poses) {
                ss << bfmt("P[%.2f, %.2f, %.2f] q(%.2f,%.2f,%.2f,%.2f)") %
                          pose_stamped.pose.position.x % pose_stamped.pose.position.y %
                          pose_stamped.pose.position.z % pose_stamped.pose.orientation.w %
                          pose_stamped.pose.orientation.x % pose_stamped.pose.orientation.y %
                          pose_stamped.pose.orientation.z << std::endl;
            }
            RCLCPP_INFO_STREAM(g_node->get_logger(), ss.str());

            publish_waypoints_vis();
            publish_waypoints();

            waypointSegments.pop_front();
        }
    }
}

void goal_callback(const geometry_msgs::msg::PoseStamped::ConstSharedPtr& msg) {
/*    if (!is_odom_ready) {
        RCLCPP_ERROR(g_node->get_logger(), "[waypoint_generator] No odom!");
        return;
    }*/

    trigged_time = g_node->get_clock()->now(); //odom.header.stamp;
    //RCLCPP_ASSERT(trigged_time > rclcpp::Time(0));

    g_node->get_parameter("waypoint_type", waypoint_type);

    if (waypoint_type == string("circle")) {
        waypoints = circle();
        publish_waypoints_vis();
        publish_waypoints();
    } else if (waypoint_type == string("eight")) {
        waypoints = eight();
        publish_waypoints_vis();
        publish_waypoints();
    } else if (waypoint_type == string("points")) {
        waypoints = point();
        publish_waypoints_vis();
        publish_waypoints();
    } else if (waypoint_type == string("series")) {
        load_waypoints(trigged_time);
    } else if (waypoint_type == string("manual-lonely-waypoint")) {
        if (msg->pose.position.z > -0.1) {
            // if height > 0, it's a valid goal;
            geometry_msgs::msg::PoseStamped pt = *msg;
            waypoints.poses.clear();
            waypoints.poses.push_back(pt);
            publish_waypoints_vis();
            publish_waypoints();
        } else {
            RCLCPP_WARN(g_node->get_logger(), "[waypoint_generator] invalid goal in manual-lonely-waypoint mode.");
        }
    } else {
        if (msg->pose.position.z > 0) {
            // if height > 0, it's a normal goal;
            geometry_msgs::msg::PoseStamped pt = *msg;
            if (waypoint_type == string("noyaw")) {
                double yaw = getYaw(odom.pose.pose.orientation);
                pt.pose.orientation = quaternionFromYaw(yaw);
            }
            waypoints.poses.push_back(pt);
            publish_waypoints_vis();
        } else if (msg->pose.position.z > -1.0) {
            // if 0 > height > -1.0, remove last goal;
            if (waypoints.poses.size() >= 1) {
                waypoints.poses.erase(std::prev(waypoints.poses.end()));
            }
            publish_waypoints_vis();
        } else {
            // if -1.0 > height, end of input
            if (waypoints.poses.size() >= 1) {
                publish_waypoints_vis();
                publish_waypoints();
            }
        }
    }
}

void traj_start_trigger_callback(const geometry_msgs::msg::PoseStamped::ConstSharedPtr& msg) {
    (void)msg;
    if (!is_odom_ready) {
        RCLCPP_ERROR(g_node->get_logger(), "[waypoint_generator] No odom!");
        return;
    }

    RCLCPP_WARN(g_node->get_logger(), "[waypoint_generator] Trigger!");
    trigged_time = rclcpp::Time(odom.header.stamp);
    if (!(trigged_time > rclcpp::Time(0, 0, RCL_ROS_TIME))) {
        RCLCPP_ERROR(g_node->get_logger(), "[waypoint_generator] invalid trigged_time");
        return;
    }

    g_node->get_parameter("waypoint_type", waypoint_type);

    RCLCPP_ERROR_STREAM(g_node->get_logger(), "Pattern " << waypoint_type << " generated!");
    if (waypoint_type == string("free")) {
        waypoints = point();
        publish_waypoints_vis();
        publish_waypoints();
    } else if (waypoint_type == string("circle")) {
        waypoints = circle();
        publish_waypoints_vis();
        publish_waypoints();
    } else if (waypoint_type == string("eight")) {
        waypoints = eight();
        publish_waypoints_vis();
        publish_waypoints();
   } else if (waypoint_type == string("point")) {
        waypoints = point();
        publish_waypoints_vis();
        publish_waypoints();
    } else if (waypoint_type == string("series")) {
        load_waypoints(trigged_time);
    }
}

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);

    rclcpp::NodeOptions options;
    options.allow_undeclared_parameters(true);
    g_node = std::make_shared<rclcpp::Node>("waypoint_generator", options);

    g_node->declare_parameter<std::string>("waypoint_type", "manual");
    waypoint_type = g_node->get_parameter("waypoint_type").as_string();

    auto sub1 = g_node->create_subscription<nav_msgs::msg::Odometry>(
        "odom", 10, odom_callback);
    auto sub2 = g_node->create_subscription<geometry_msgs::msg::PoseStamped>(
        "goal", 10, goal_callback);
    auto sub3 = g_node->create_subscription<geometry_msgs::msg::PoseStamped>(
        "traj_start_trigger", 10, traj_start_trigger_callback);
    pub1 = g_node->create_publisher<nav_msgs::msg::Path>("waypoints", 50);
    pub2 = g_node->create_publisher<geometry_msgs::msg::PoseArray>("waypoints_vis", 10);

    trigged_time = rclcpp::Time(0, 0, RCL_ROS_TIME);

    rclcpp::spin(g_node);
    rclcpp::shutdown();
    return 0;
}
