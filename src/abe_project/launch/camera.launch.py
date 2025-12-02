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
        get_package_share_directory('abe_project'), 'config', 'optris', 'optris_config.xml'
    )
    rviz_config_file = os.path.join(
        get_package_share_directory('abe_project'),
        'rviz',
        'rviz_config.rviz'
    )

    
    # Optional: allow a gantry prefix


    gantry_arg = DeclareLaunchArgument(
        'gantry',
        default_value='gantry',
        description='Prefix for gantry links'
    )

    urdf_file = PathJoinSubstitution([
        FindPackageShare('abe_project'),
        'urdf',
        'gantry.xacro'
    ])

    robot_description = {'robot_description': Command([
        FindExecutable(name='xacro'),
        ' ',
        urdf_file,
        ' gantry:=',
        LaunchConfiguration('gantry')
    ])}


    return LaunchDescription([


        gantry_arg,

        # Publish robot state
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            emulate_tty=True,
            parameters=[robot_description]
        ),

        # Joint sliders for RViz
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            output='screen',
            emulate_tty=True
        ),

        # Optional: RViz for immediate visualization
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            emulate_tty=True,
            arguments=['-d', rviz_config_file]  # optional, can remove if no config yet
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
        ),

        Node(
            package='thermal_processing',
            executable='image_processor',
            name='thermal_roi_detector',
            output='screen'
        ),

        Node(
            package='thermal_processing',
            executable='camera_control',
            name='camera_tracking',
            output='screen'
        ),

    

    ])
