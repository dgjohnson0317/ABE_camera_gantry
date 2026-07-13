#This launch file will bring up the robot w/CMT and both Optris IR cameras
 
import os

import yaml
 
from ament_index_python import get_package_share_directory
 
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.actions import TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_xml.launch_description_sources import XMLLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

import ament_index_python.packages
 
def load_parameters() -> str:
    share_dir = ament_index_python.packages.get_package_share_directory('ueye_cam')
    # There are two different ways to pass parameters to a non-composed node;
    # either by specifying the path to the file containing the parameters, or by
    # passing a dictionary containing the key -> value pairs of the parameters.
    # When starting a *composed* node on the other hand, only the dictionary
    # style is supported.  To keep the code between the non-composed and
    # composed launch file similar, we use that style here as well.
    parameters_file = os.path.join(share_dir, 'config', 'example_ros_configuration.yaml')
    with open(parameters_file, 'r') as f:
        parameters = yaml.safe_load(f)['ueye_cam']['ros__parameters']
    return parameters

def generate_launch_description():
    
    robot_namespace = DeclareLaunchArgument(
        'robot_namespace',
        default_value='am_400',
        description='Namespace for the robot'
    )
 
    # Set the ROS namespace for all subsequent ROS actions within this group
    push_namespace = PushRosNamespace(LaunchConfiguration('robot_namespace'))
    
 
   
 
    rqt_irimages = Node(
        package='rqt_gui',
        executable='rqt_gui',
        name='rqt_gui_with_perspective',
       # arguments=[
       #     '--perspective-file',
       #     ( os.path.dirname(os.path.realpath(__file__)).split('AM-400-ROS2/')[0] + 'AM-400-ROS2' +'/rqt/ir_data_pi640v3.perspective')],
        output='screen'
    )
    
 
    return LaunchDescription([
        robot_namespace,
        GroupAction([
        push_namespace,
 
    TimerAction(
    period=5.0,
    actions=[
 
    #Node(package = 'optris_drivers2',
    #                executable = 'optris_imager_node',
    #                name = 'pi640',
    #                remappings=[
    #                ("/thermal_image", "/thermal_image_pi640")],
    #                arguments = [PathJoinSubstitution([FindPackageShare("am400_bringup"),"config","optris","19102025_LT.xml"])],
    #                #output='screen'
    #                ),
 #
    #Node(package = 'optris_drivers2',
    #                executable = 'optris_colorconvert_node',
    #                name = 'convert',
    #                remappings=[
    #                ("/thermal_image", "thermal_image_pi640"),
    #                ("/thermal_image_view", "/thermal_image_viewpi640")],
    #                ),
                    
    Node(package = 'ueye_cam',
            name="ueye",
            executable="standalone_node",  # dashing: node_executable, foxy: executable
            output='screen',  # 'both'?
            emulate_tty=True,  # dashing: prefix=['stdbuf -o L'], foxy, just use emulate_tty=True
            parameters=[load_parameters()]
            ),

 
 
   ]),
 
 
    rqt_irimages,
])])