#!/usr/bin/env python3

from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch.launch_context import LaunchContext
from launch_ros.actions import Node


def _launch_node(context: LaunchContext):

    # Convert launch-arguments -> python types
    respawn_bool  = LaunchConfiguration("respawn").perform(context).lower() == "true"
    delay_float   = float(LaunchConfiguration("respawn_delay").perform(context))

    params_path = Path(
        get_package_share_directory("xsens_mti_ros2_driver"),
        "param",
        "xsens_mti_node.yaml",
    )

    return [
        Node(
            package="xsens_mti_ros2_driver",
            executable="xsens_mti_node",
            name="xsens_mti_node",
            output="screen",
            parameters=[params_path],
            respawn=respawn_bool,
            respawn_delay=delay_float,
            # Optional CPU affinity / niceness:
            # prefix=['taskset','-c','2','nice','-n','-5'],
        )
    ]


def generate_launch_description():

    ld = LaunchDescription()

    # Environment tweaks for consistent logging
    ld.add_action(SetEnvironmentVariable("RCUTILS_LOGGING_USE_STDOUT", "1"))
    ld.add_action(SetEnvironmentVariable("RCUTILS_LOGGING_BUFFERED_STREAM", "1"))

    # New launch arguments
    ld.add_action(DeclareLaunchArgument(
        "respawn",
        default_value="true",
        description="Restart xsens_mti_node automatically if it exits"))
    ld.add_action(DeclareLaunchArgument(
        "respawn_delay",
        default_value="2.0",
        description="Seconds to wait before respawning the node"))

    # Build the driver node after substitutions are known
    ld.add_action(OpaqueFunction(function=_launch_node))

    return ld
