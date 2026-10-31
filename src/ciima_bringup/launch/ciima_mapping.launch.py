
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    bringup_dir = get_package_share_directory('bringup')
    slam_dir = get_package_share_directory('slam_toolbox')
    nav2_dir = get_package_share_directory('nav2_bringup')

    use_sim_time = LaunchConfiguration('use_sim_time')

    slam_params_file = os.path.join(
        bringup_dir,
        'configs',
        'slam_params.yaml'
    )

    nav2_params_file = os.path.join(
        bringup_dir,
        'configs',
        'nav2_params.yaml'
    )

    slam_launch_file = os.path.join(
        slam_dir,
        'launch',
        'online_async_launch.py'
    )

    nav2_launch_file = os.path.join(
        nav2_dir,
        'launch',
        'navigation_launch.py'
    )

    # Start SLAM Toolbox
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch_file),
        launch_arguments={
            'slam_params_file': slam_params_file,
            'use_sim_time': use_sim_time
        }.items()
    )

    # Start Nav2 navigation
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(nav2_launch_file),
        launch_arguments={
            'params_file': nav2_params_file,
            'use_sim_time': use_sim_time,
            'autostart': 'true',
            'use_composition': 'False',
            'use_respawn': 'False'
        }.items()
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use Gazebo simulation clock'
        ),

        slam,

        # Give SLAM a little time to initialize
        TimerAction(
            period=3.0,
            actions=[navigation]
        )
    ])
