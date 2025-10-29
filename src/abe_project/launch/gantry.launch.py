from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
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
        DeclareLaunchArgument("roi_width_pi400", default_value="50", description="ROI width in pixels"), 
        DeclareLaunchArgument("roi_height_pi400", default_value="25", description="ROI height in pixels"),
        DeclareLaunchArgument("fixed_roi_enable_pi400", default_value="False"),
        DeclareLaunchArgument("fixed_roi_cx_pi400", default_value="191"),
        DeclareLaunchArgument("fixed_roi_cy_pi400", default_value="144"),
        DeclareLaunchArgument("fixed_roi_w_pi400",  default_value="150"),
        DeclareLaunchArgument("fixed_roi_h_pi400",  default_value="150"), 

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
            arguments=['-d', PathJoinSubstitution([
                FindPackageShare('abe_project'),
                'launch',
                'abe.rviz'

            ])]  # optional, can remove if no config yet
        ), 
        Node(
            package="draw_image_process",
            executable="optris_temp400LT",
            name="PI400LT_publisher",
            parameters=[{
                "roi_width": ParameterValue(LaunchConfiguration("roi_width_pi400"), value_type=int),
                "roi_height": ParameterValue(LaunchConfiguration("roi_height_pi400"), value_type=int),
                "fixed_roi_enable": LaunchConfiguration("fixed_roi_enable_pi400"),
                "fixed_roi_cx": LaunchConfiguration("fixed_roi_cx_pi400"),
                "fixed_roi_cy": LaunchConfiguration("fixed_roi_cy_pi400"),
                "fixed_roi_w":  LaunchConfiguration("fixed_roi_w_pi400"),
                "fixed_roi_h":  LaunchConfiguration("fixed_roi_h_pi400"),
            }],        
            output="screen",
    )
    

    ])
