#include <iostream>
#include <vector>
#include <cstring>
#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
#include <sensor_msgs/msg/point_field.hpp>
#include <pose_utils.h>
#include <multi_map_server/msg/multi_occupancy_grid.hpp>
#include <multi_map_server/msg/multi_sparse_map3_d.hpp>
#include <multi_map_server/Map2D.h>
#include <multi_map_server/Map3D.h>

using namespace std;

rclcpp::Node::SharedPtr g_node;
rclcpp::Publisher<multi_map_server::msg::MultiOccupancyGrid>::SharedPtr pub1;
rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pub2;

vector<Map2D> maps2d;
vector<geometry_msgs::msg::Pose> origins2d;
vector<Map3D> maps3d;
vector<geometry_msgs::msg::Pose> origins3d;

void maps2d_callback(const multi_map_server::msg::MultiOccupancyGrid::ConstSharedPtr msg)
{
  // Merge map
  maps2d.resize(msg->maps.size(), Map2D(4));
  for (unsigned int k = 0; k < msg->maps.size(); k++)
    maps2d[k].Replace(msg->maps[k]);
  origins2d = msg->origins;
  // Assemble and publish map
  multi_map_server::msg::MultiOccupancyGrid m;
  m.maps.resize(maps2d.size());
  m.origins.resize(maps2d.size());
  for (unsigned int k = 0; k < maps2d.size(); k++)
  {
    m.maps[k]    = maps2d[k].GetMap();
    m.origins[k] = origins2d[k];
  }
  pub1->publish(m);
}

void maps3d_callback(const multi_map_server::msg::MultiSparseMap3D::ConstSharedPtr msg)
{
  // Update incremental map
  maps3d.resize(msg->maps.size());
  for (unsigned int k = 0; k < msg->maps.size(); k++)
    maps3d[k].UnpackMsg(msg->maps[k]);
  origins3d = msg->origins;

  // Assemble 3D point cloud
  vector<float> data;
  for (unsigned int k = 0; k < msg->maps.size(); k++)
  {
    colvec po(6);
    po(0) = origins3d[k].position.x;
    po(1) = origins3d[k].position.y;
    po(2) = origins3d[k].position.z;
    colvec poq(4);
    poq(0) = origins3d[k].orientation.w;
    poq(1) = origins3d[k].orientation.x;
    poq(2) = origins3d[k].orientation.y;
    poq(3) = origins3d[k].orientation.z;
    po.rows(3,5) = R_to_ypr(quaternion_to_R(poq));
    colvec tpo = po.rows(0,2);
    mat    Rpo = ypr_to_R(po.rows(3,5));
    vector<colvec> pts = maps3d[k].GetOccupancyWorldFrame(OCCUPIED);
    for (unsigned int i = 0; i < pts.size(); i++)
    {
      colvec pt = Rpo * pts[i] + tpo;
      data.push_back(pt(0));
      data.push_back(pt(1));
      data.push_back(pt(2));
    }
  }

  sensor_msgs::msg::PointCloud2 m;
  m.header.stamp    = g_node->get_clock()->now();
  m.header.frame_id = string("/map");
  m.height          = 1;
  m.width           = data.size() / 3;
  m.is_dense        = true;
  m.is_bigendian    = false;
  m.point_step      = 3 * sizeof(float);
  m.row_step        = m.point_step * m.width;

  sensor_msgs::msg::PointField f1, f2, f3;
  f1.name     = "x";
  f1.offset   = 0;
  f1.datatype = sensor_msgs::msg::PointField::FLOAT32;
  f1.count    = 1;
  f2.name     = "y";
  f2.offset   = 4;
  f2.datatype = sensor_msgs::msg::PointField::FLOAT32;
  f2.count    = 1;
  f3.name     = "z";
  f3.offset   = 8;
  f3.datatype = sensor_msgs::msg::PointField::FLOAT32;
  f3.count    = 1;
  m.fields.push_back(f1);
  m.fields.push_back(f2);
  m.fields.push_back(f3);

  m.data.resize(data.size() * sizeof(float));
  memcpy(m.data.data(), data.data(), data.size() * sizeof(float));

  pub2->publish(m);
}

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  g_node = std::make_shared<rclcpp::Node>("multi_map_visualization");

  auto sub1 = g_node->create_subscription<multi_map_server::msg::MultiOccupancyGrid>(
    "dmaps2d", 1, maps2d_callback);
  auto sub2 = g_node->create_subscription<multi_map_server::msg::MultiSparseMap3D>(
    "dmaps3d", 1, maps3d_callback);
  pub1 = g_node->create_publisher<multi_map_server::msg::MultiOccupancyGrid>("maps2d", 1);
  pub2 = g_node->create_publisher<sensor_msgs::msg::PointCloud2>("map3d", 1);

  rclcpp::spin(g_node);
  rclcpp::shutdown();
  return 0;
}
