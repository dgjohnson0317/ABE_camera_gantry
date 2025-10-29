# Thermal Plate Package

## Overview
This document contains the general top down view of the Thermal Plate Package, which is an N x N thermocouple grid. 
The location of this package is in the ros_epic_v2/../../src/draw_data_fusion directory on David Johnsons gu502gv
### package file
The package file for this document is `thermal_plate_gradient.py`. Inside this document there are some important functions/sections to consider. 

Firstly, the `__init__` function inside the `Thermo_Plate` Class creates the publisher node, called `/rob_cmd/"name"`. The `self.thermo_plate_publisher` starts a publisher that will be called later, notably a Rviz Marker called `thermal_cube_grid_topic`. In this function is also the subscription (`self.dataq_subscription`) to the DI2008s that will be used for this project, however only one is being called currently. There likely will need to be more work in order to parse multiple dataqs, particularly when there are 8 for the thermocouple plate and other dataqs for other purposes. 

The `publish grid` function acts as the primary logic for this package. This is where the marker type, frame_id (think of the links with the URDF), and scale. This also generates a grid of cubes based on Number of Dataqs (which will have to be defined manually at the moment). 

The `normalize value` function acts as a method to normalize all temperature values into a range between 0 and 1 that can be parsed into colors later for display later. The output from this function is input into the `value_to_color` function, which at the moment seems to be working well, but it is challenging to test with the current daq/thermocouple setup. 

 When calling thermocouples it should be noted that the individual topic names in Rviz follow the following format:
`/rob_cmt/di2008_tc_output/di2008s[#A]/analog[#B]/data`.

However, when parsing the .msg from the DI2008, we must first subscribe to the topic `/rob_cmt?di2008_tc_output`, which will give global access to the msg output from this topic as a `DI2008Array`. This message (msg) can then be parsed as follows: `msg.di2008s[#A].analog[#B].data`, where #A and #B are the serial number and channel number (beginning at index 0) respectively. As stated above, this will likely need to change as more Dataq 2008s are added to the system to ensure consistent grid formation between builds. 

The final function `main` (notice it is outside of the Class structure) simply spins up the node, and initializes everything. This also serves as an entry point for ROS2, which will be highlighted in the setup.py file. This is also where the Node (or the class name) is called. 

### setup.py
For a new package setup.py file, there are some requirements that are mostly generalized between each setup.py file. Everything in the `draw_data_fusion/setup.py` file seems to follow a template, except the entry points. The entry points are where you call your file, specifically where you define the filepath for any specific node of interest. 

This document will not go thorugh how to write a setup.py file at the moment, instead this is mainly used to highlight the points of interest needed to get a package/node/topic running and publishing. 

### launch.py
Similarly to the setup.py file above, there are two main points of interest in the launch.py file. Currently, the launch file of interst is `simple.launch.py`. 

The first significant portion of the script is the Node definition, where the Node is defined as `weld_plate_gradient`, and there are input variables, notably the package_name (folder), the executable name (.py), and the node name in that order. finally, there are outputs and/or input parameters needed for the node. 

Next, the same variable name should be added to the `return LaunchDescription` at the end of the launch file, specifically as an action under GroupAction.

### testing and topic or node validation
It may be useful to run `ros2 node list` and `ros2 topic list` to help debug issues when tryingn to run nodes and publish topics, especially considering the amount of messages being output by the current ROS build.

In order to load the marker, one should go to the left window in Rviz, click add, and find the marker "by topic". 
