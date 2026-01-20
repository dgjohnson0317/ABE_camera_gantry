from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    # Path to your bag
    bag_path = 'rosbag2_2025_11_17-16_22_30'

    # Replay the bag file
    rosbag_play = ExecuteProcess(
        cmd=['ros2', 'bag', 'play', bag_path, '--loop'],
        output='screen'
    )

    # Example nodes to launch
    image_processor = Node(
        package='thermal_processing',
        executable='camera_control',
        name='camera_control',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    arduino_link = Node(
        package='thermal_processing',
        executable='arduino_link',
        name='arduino_link',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    rviz = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    arguments=['-d', 'src/abe_project/rviz/rviz_config.rviz'],
    parameters=[{'use_sim_time': True}],
)

    # Combine everything
    return LaunchDescription([
        rosbag_play,
        image_processor,
        arduino_link,
        rviz
    ])
