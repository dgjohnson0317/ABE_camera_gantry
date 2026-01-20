# Launch file general format

## def Generate launch description
The entire `generate launch description` function can be formatted in two different ways. The first, and more easily readable option, is defining nodes for each package you would like to have running, as shown below. 

```py
    pi_640_launch = Node(package = 'optris_drivers2',
                    executable = 'optris_imager_node',
                    name = 'pi640',
                    remappings=[
                    ("/thermal_image", "/thermal_image_pi640")],
                    arguments = [PathJoinSubstitution([FindPackageShare("am400_bringup"),"config","optris","19102025_LT.xml"])],
                    #output='screen'
                    )
```
This `pi_640_launch` node can then be input as a variable into the `return LaunchDescription` to ensure that it will run when launching this file. 

The other option for formatting is to input your nodes directly under the `return LaunchDescription`. For a single pi640 node, this would look like the following: 
```py
    return LaunchDescription([
    GroupAction([
    Node(package = 'optris_drivers2',
                    executable = 'optris_imager_node',
                    name = 'pi640',
                    remappings=[
                    ("/thermal_image", "/thermal_image_pi640")],
                    arguments = [PathJoinSubstitution([FindPackageShare("am400_bringup"),"config","optris","19102025_LT.xml"])],
                    #output='screen'
                    ),
    
    ]),
    
    ])
```

There does seem to be a parameters file that you need to load, which i am unsure of how exactly it needs to be formatted in the ros stack, 

The launch parameters are loaded using the load_parameters function, which I pulled straight from the ueye_cam package launch file. I am sure there is a cleaner way to do this in a bigger launch file but for now it is at least working as a launch file. 

### Dependency installation
I am unsure what you are allowed to download and install to get everything working, or now to ensure dependencies are downloaded with apptainer, but I am fairly sure the following list should be all of them, as well as the changes needed to make sure this builds and works. 

- sudo apt install libtclap-dev
- line 1873 changed in driver/driver.cpp : for (const std::pair<const std::string, INT>& value : COLOR_DICTIONARY) {
- sudo apt install libomp5 libomp-dev
- sudo /etc/init.d/ueyeusbdrc start
- sudo systemctl start ueyeusbdrc
- sudo apt-get install libqt53dextras5
- sudo apt-get install libqt5quickcontrols2-5 libqt5multimedia5 libqt5webengine5 libqt5quick5 libqt5qml5
- sudo apt update && sudo apt upgrade -y && sudo apt install -y qtcreator qtbase5-dev qt5-qmake cmake && sudo apt autoremove

**These three might not actually be needed or real dependencies:**
- sudo apt install libqt5
- sudo apt install pyqt5
- sudo apt install qt

