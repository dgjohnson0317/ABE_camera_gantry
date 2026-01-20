from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'abe_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[  # <-- add this
            ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
            ('share/' + package_name, ['package.xml']),

            (os.path.join("share", package_name, "launch"), glob("launch/*")), 
            (os.path.join("share", package_name, "urdf"), glob("urdf/*")), 
            (os.path.join("share", package_name, "config", "optris"), glob("config/optris/*")), 
            
            #('share/' + package_name + '/launch', ['launch/gantry.launch.py']),
            #('share/' + package_name + '/launch', ['launch/rosbag.launch.py']),
            #('share/' + package_name + '/launch', ['launch/camera.launch.py']),
            #('share/' + package_name + '/urdf', ['urdf/camera_gimbal.xacro']),
            #('share/' + package_name + '/urdf', ['urdf/gantry.xacro']),
            #('share/' + package_name + '/config' + '/optris', ['config/optris/optris_config.xml']),
            #('share/' + package_name + '/config' + '/optris', ['config/optris/pi_640_config.xml']),
            #('share/' + package_name + '/rviz', ['rviz/rviz_config.rviz']),
            # add meshes if needed
            # ('share/' + package_name + '/meshes', ['meshes/your_mesh_file.stl']),
        ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='David Johnson',
    maintainer_email='dgj67@msstate.edu',
    description='ABE project launch, urdf, and camera configs',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
