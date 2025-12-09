# Camera Calibration
This file intends to outline the steps required to use the ros2 camera_calibration package.

## Installation and usage
### Downloading camera_calibration package
To download the camera_calibration package, you can use the following command. This will download and install the camera calibration package to your local ros2 install, where it will then be sources each time you source ros2 (using `source /opt/ros/humble/setup.bash`)
```
sudo apt install ros-humble-camera-calibration
```

### Running camera_calibrator node 
As per other documentation, the camera calibration node can be launched using the following script. Also, the table below outlines the input parameters that can be input to this script. 
```
ros2 run camera_calibration cameracalibrator --size <NxM> --square <WIDTH> --pattern <PATTERN> --ros-args -r image:=/<IMAGE_TOPIC_NAME> 
```

**Used parameters**:
|  |  |
| :---: | --- |
| --pattern | Calibration pattern to detect. Can be 'chessboard', 'circles', or 'acircles' |
| --size | NxM size as interior corners. For acircles the size parameter is described in detail below. |
| --square | Shape width/diameter in meters |

At any point, if there are questions that have not been addressed in this document, you can add the `--help` arguement as described above to output details about the package, such as:
```
ros2 run camera_calibration cameracalibrator --help
```

### `acircles`
 
The illustrations below attempt to help display the alternating circles (**acircles**) pattern used for the calibration board, as well as a non working pattern.

**Current board** - 20.5mm x 25mm board, NxM = 3x7
| | | | | | | |
| --- | --- | --- | --- | --- | --- | --- |
|  O  |    |  O  |    |  O  |    |  O  |  
|    |  O  |    |  O  |    |  O  |    | 
|  O  |    |  O  |    |  O  |    |  O  | 
|    |  O  |    |  O  |    |  O  |    | 
|  O  |    |  O  |    |  O  |    |  O  |
|    |  O  |    |  O  |    |  O  |    | 

It should also be noted that the calibration board CAN NOT be symmetrical. To be specific, the circles can be 3x7, 3x9 etc, but cannot be 4x7, as shown below:

**Non-working board** - 25mm x 25mm board, Nxm = 4x7 (kind of)
| | | | | | | |
| --- | --- | --- | --- | --- | --- | --- |
|  O  |    |  O  |    |  O  |    |  O  | 
|    |  O  |    |  O  |    |  O  |    | 
|  O  |    |  O  |    |  O  |    |  O  |
|    |  O  |    |  O  |    |  O  |    | 
|  O  |    |  O  |    |  O  |    |  O  |
|    |  O  |    |  O  |    |  O  |    | 
|  O  |    |  O  |    |  O  |    |  O  |

I believe the N dimension (ie 3 or 4 in the above cases) count the number of "row pairs", where a pair is something similar to what is shown below. This pair association allows the grid to understand orientation as the camera/board orientation is being altered for calibration. 

**Single "row"** - NxM = 1x9
| | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  O  |    |  O  |    |  O  |    |  O  |     |  O  | 
|    |  O  |    |  O  |    |  O  |    |  O  |    |

### Service calls for image visibility
For the calibration board, the camera calibration node seems to require the dots to be black, and the background white. With optris_imager_node and optris_colorconvert_node running, we will need to alter the coloration of the colorconvert image, output as `/thermal_image_view` unless renamed elsewhere. 

Using optris service calls, we can change the color palette (pallete 4) to allow for the hot regions to be black, and cold to be white. At the current settings, ambient is about 40c and the cold temperature is 20c, with the pallete scaling being set to manual (1).These settings can be changed in rqt using the service caller, found in `rqt/plugins/services/service caller`.


## Calibrations 
Using the following command, you can launch cameracalibrator, alter the calibration board x and y positions, as well as skew and rotation until the calibrate button appears in the calibrator window, allowing you to generate and commit the output .yaml file to a location. 
```
ros2 run camera_calibration cameracalibrator --size 3x7 --square 0.0298 --pattern acircles --ros-args -r image:=/thermal_image_view 
```
Shown below are the the terminal outputs after calibrating the Optris PI400

```
**** Calibrating ****
mono pinhole calibration...
*** Added sample 80, p_x = 0.291, p_y = 0.564, p_size = 0.386, skew = 0.004
D = [-0.42081310932840893, 2.3335736361131207, -0.008217402186179286, -0.00323314367009305, 0.0]
K = [1153.9427601218163, 0.0, 159.70131960583637, 0.0, 1151.3435718030678, 222.59841073794567, 0.0, 0.0, 1.0]
R = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
P = [1138.55908203125, 0.0, 158.48125087439257, 0.0, 0.0, 1139.740478515625, 222.0780220814995, 0.0, 0.0, 0.0, 1.0, 0.0]
None
```
#### `ost.txt`:
```
# oST version 5.0 parameters


[image]

width
382

height
288

[narrow_stereo]

camera matrix
1153.942760 0.000000 159.701320
0.000000 1151.343572 222.598411
0.000000 0.000000 1.000000

distortion
-0.420813 2.333574 -0.008217 -0.003233 0.000000

rectification
1.000000 0.000000 0.000000
0.000000 1.000000 0.000000
0.000000 0.000000 1.000000

projection
1138.559082 0.000000 158.481251 0.000000
0.000000 1139.740479 222.078022 0.000000
0.000000 0.000000 1.000000 0.000000

('Wrote calibration data to', '/tmp/calibrationdata.tar.gz')
```

The ost data is written to a tar.gz zip file, as shown in the last line of the code block above. This zip file contains some calibration images, the ost block from above (in ost.txt), as well as the yaml file for the camera calibration (ost.yaml) shown below:
#### `ost.yaml`:
```
image_width: 382
image_height: 288
camera_name: narrow_stereo
camera_matrix:
  rows: 3
  cols: 3
  data: [1153.94276,    0.     ,  159.70132,
            0.     , 1151.34357,  222.59841,
            0.     ,    0.     ,    1.     ]
distortion_model: plumb_bob
distortion_coefficients:
  rows: 1
  cols: 5
  data: [-0.420813, 2.333574, -0.008217, -0.003233, 0.000000]
rectification_matrix:
  rows: 3
  cols: 3
  data: [1., 0., 0.,
         0., 1., 0.,
         0., 0., 1.]
projection_matrix:
  rows: 3
  cols: 4
  data: [1138.55908,    0.     ,  158.48125,    0.     ,
            0.     , 1139.74048,  222.07802,    0.     ,
            0.     ,    0.     ,    1.     ,    0.     ]
```


## Links: 
https://medium.com/starschema-blog/offline-camera-calibration-in-ros-2-45e81df12555
 
https://industrial-training-master.readthedocs.io/en/latest/_source/session9/Cameras-and-Calibration.html
 
https://docs.ros.org/en/kilted/p/camera_calibration/doc/tutorial_mono.html

https://wiki.ros.org/camera_calibration

https://wiki.ros.org/optris_drivers 
