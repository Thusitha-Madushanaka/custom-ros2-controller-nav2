import os
import re

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    gazebo_ros_share = get_package_share_directory("gazebo_ros")

    urdf_file = os.path.expanduser(
        "~/nav2_ws/ciima_nav2_control_test.urdf"
    )

    world_file = os.path.expanduser(
        "~/nav2_ws/worlds/ciima_warehouse.world"
    )

    with open(urdf_file, "r") as file:
        robot_description = file.read()

    robot_description = re.sub(
        r"<!--.*?-->",
        "",
        robot_description,
        flags=re.DOTALL
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_ros_share,
                "launch",
                "gazebo.launch.py",
            )
        ),
        launch_arguments={
            "world": world_file,
            "verbose": "true",
        }.items(),
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[
            {"robot_description": robot_description},
            {"use_sim_time": True},
        ],
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-entity", "ciima_mesh_test",
            "-file", urdf_file,
            "-x", "0",
            "-y", "0",
            "-z", "0",
        ],
        output="screen",
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "60",
        ],
        output="screen",
    )

    custom_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "custom_controller",
            "--controller-manager", "/controller_manager",
            "--controller-manager-timeout", "60",
        ],
        output="screen",
    )

    start_broadcaster_after_spawn = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_robot,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )

    start_controller_after_broadcaster = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[custom_controller_spawner],
        )
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot,
        start_broadcaster_after_spawn,
        start_controller_after_broadcaster,
    ])
