import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    bringup_dir = get_package_share_directory('nav2_bringup')
    ciima_bringup_dir = get_package_share_directory('bringup')

    params_file = os.path.join(
        ciima_bringup_dir,
        'configs',
        'nav2_params.yaml'
    )

    

    default_map = os.path.expanduser(
        '~/nav2_ws/maps/slam/ciima_warehouse_slam.yaml'
    )

    localization_launch_file = os.path.join(
        bringup_dir,
        'launch',
        'localization_launch.py'
    )

    navigation_launch_file = os.path.join(
        bringup_dir,
        'launch',
        'navigation_launch.py'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_file = LaunchConfiguration('map')

    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(localization_launch_file),
        launch_arguments={
            'map': map_file,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
            'autostart': 'true',
            'use_composition': 'False',
            'use_respawn': 'False'
        }.items()
    )

    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(navigation_launch_file),
        launch_arguments={
            'params_file': params_file,
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

        DeclareLaunchArgument(
            'map',
            default_value=default_map,
            description='Path to CIIMA warehouse map'
        ),

        localization,
        navigation
    ])
