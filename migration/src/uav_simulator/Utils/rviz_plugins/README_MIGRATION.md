# rviz_plugins — excluded from the ROS2 build

This package is intentionally excluded from the `colcon build` via the
`COLCON_IGNORE` marker file, for two reasons:

1. **Missing message type** — `src/gamelikeinput.cpp` publishes
   `quadrotor_msgs::SwarmCommand`, but no `SwarmCommand.msg` exists in the
   `quadrotor_msgs` package in this workspace (only `PositionCommand`,
   `Odometry`, `SO3Command`, etc. are present). The file would not compile
   until that message is added.

2. **Large Qt / rviz_common port** — the package is a set of rviz display and
   tool plugins (`goal_tool`, `pose_tool`, `probmap_display`,
   `aerialmap_display`, `multi_probmap_display`). Migrating it requires porting
   from ROS1 `rviz` (`rviz::Display`, `rviz::Tool`, `rviz::FrameManager`) to
   ROS2 `rviz_common`/`rviz_default_plugins` plus the Qt5 signal/slot plugin
   loader and `pluginlib` export machinery. It is optional visualization
   tooling, not part of the ego-planner autonomy stack, so it is left as a
   follow-up.

Remove the `COLCON_IGNORE` file to re-enable this package once a
`SwarmCommand` message is defined and the rviz API is migrated.
