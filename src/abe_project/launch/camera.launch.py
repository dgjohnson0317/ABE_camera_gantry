from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    config_file = os.path.join(
        get_package_share_directory('abe_project'), 'config', 'optris', 'xi400_2.xml'
    )




    return LaunchDescription([



        # Optional: RViz for immediate visualization
        Node(
            package='rqt_gui',
            executable='rqt_gui',
            name='rqt_gui',
            output='screen',
            emulate_tty=True  # optional, can remove if no config yet
        ), 
        Node(
            package='optris_drivers2',
            executable='optris_imager_node',
            name='optris_camera',
            output='screen',
            arguments=[config_file], # adjust path
        ),

        Node(
            package='optris_drivers2',
            executable='optris_colorconvert_node',
            name='optris_camera_colored',
            output='screen',  # adjust path
        )

    

    ])
