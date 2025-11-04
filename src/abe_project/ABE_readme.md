# Steps to build package in workspace
This document indends to highlight all of the steps taken in order to build a local version of ros, and get a package for visualizing the ABE_project working in a local ros2 workspace, instead of apptainer.
## Installing ros2 and colcon
The installation process for ros2 humble was done using the ros2 installation guide found here: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html

Once installation of ros was done, you should also ensure that colcon is downloaded using the following commands
`sudo apt install python3-colcon-common-extensions -y`

## Errors Encountered

### Xacro errors
Once running `source /opt/ros/humble/setup.bash`, `colcon build`, and `source install/setup.bash` while inside the workspace, i was getting the following error:
```cmd
ros2 launch abe_project gantry.launch.py 
[INFO] [launch]: All log files can be found below /home/davidjohnson/.ros/log/2025-10-28-11-08-21-691407-gu502gv-212331
[INFO] [launch]: Default logging verbosity is set to INFO
[ERROR] [launch]: Caught exception in launch (see debug for traceback): executable '[<launch.substitutions.text_substitution.TextSubstitution object at 0x7ce302ae3970>]' not found on the PATH
```
This output indicated some substitution issue, which led me to eventually investigate the xacro files, as this package worked previously inside the apptainer. The xacro package is not natively included in ros, causing this issue. The following cmd output is the resolution for this error. 

Run `sudo apt install ros-humble-xacro`
```cmd
sudo apt install ros-humble-xacro
[sudo] password for davidjohnson: 
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libsbc1 libspeexdsp1
Use 'sudo apt autoremove' to remove them.
The following NEW packages will be installed:
  ros-humble-xacro
0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
Need to get 37.8 kB of archives.
After this operation, 155 kB of additional disk space will be used.
Get:1 http://packages.ros.org/ros2/ubuntu jammy/main amd64 ros-humble-xacro amd64 2.1.1-1jammy.20250829.093455 [37.8 kB]
Fetched 37.8 kB in 1s (37.9 kB/s)         
Selecting previously unselected package ros-humble-xacro.
(Reading database ... 310110 files and directories currently installed.)
Preparing to unpack .../ros-humble-xacro_2.1.1-1jammy.20250829.093455_amd64.deb 
...
Unpacking ros-humble-xacro (2.1.1-1jammy.20250829.093455) ...
Setting up ros-humble-xacro (2.1.1-1jammy.20250829.093455) ...
```

### Joint State Publisher Errors
Upon launching after the xacro package was installed, the following error was output
```cmd
ros2 launch abe_project gantry.launch.py 
[INFO] [launch]: All log files can be found below /home/davidjohnson/.ros/log/2025-10-28-11-15-33-807306-gu502gv-212931
[INFO] [launch]: Default logging verbosity is set to INFO
[ERROR] [launch]: Caught exception in launch (see debug for traceback): "package 'joint_state_publisher_gui' not found, searching: ['/home/davidjohnson/ros2_ws/install/abe_project', '/opt/ros/humble']"

```
Running `sudo apt update` and 
`sudo apt install ros-humble-joint-state-publisher-gui`
should resolve this error, at which point you can run `source opt/ros/humble/setup.bash`, `colcon build`, and `source install/setup.bash` again, and finally launch your package with `ros2 launch <package_name> <package.launch.py>`

### Optris drivers installation
Following instructions from the ros wiki and https://github.com/Computational-Mechanics-Materials-Lab/optris_drivers2, the following command was run to install the ros optris drivers:
https://sdk.optris.com/downloads/
make sure to install the corrent .deb version for your linux installation (for me this was amd64 and ubuntu 22.04).

It also seems that ros2 does not come with the camera-info-manager by default, so I also ran `sudo apt install ros-humble-camera-info-manager`

Finally, for the time being, I have borrowed a config file from the develop package, primarily to ensure that when running `ros2 run optris_drivers2 optris_imager_node <config.xml>`, there are no more errors that I might encounter before going further. 

### Optris image publisher package
Using rqt_image_view, you should be able to view the thermal image published by the thermal camera. Firstly, you should make sure that the camera is publishing an image, using the above command to start the camera node. You should be able to verify it is publishing by running `ros2 topic list` in another terminal, with one of the outputs being `/thermal_image` or something similar. Running `ros2 topic info /topic_name` should output something resembling the following 
```
Type: sensor_msgs/msg/Image
Publisher count: 1
Subscription count: 0
```
You can then run `ros2 run rqt_image_view rqt_image_view` to open a window that shows images in rqt. The current issue is that while the image is publishing, and using `ros2 topic echo --once /topic_name` outputs the corrrect information, the encoding is incorrect and therefore rqt cannot visualize it properly. The resolution to this is to also spin up the optris colorconvert node, by running `ros2 run optris_drivers2 optris_color_convert` in a new terminal. Then running rqt_image_view should display the thermal images. 

### OpenCV
`sudo apt install python3-opencv` should first be run to install open cv. It should be noted that the package.xml should have opencv included in it, although I have not gone through this process yet.





#### Objectives
At the moment, I intend to clone the cmml optris camera directory to be able to get it working in the current build I have going on. However, I am unsure whether I can just copy /src.


## Dependencies
- `python3-opencv`
- `python3-colcon-common-extensions`
- `ros-humble-xacro`
- `ros-humble-camera-info-manager`
- `ros-humble-joint-state-publisher-gui`




