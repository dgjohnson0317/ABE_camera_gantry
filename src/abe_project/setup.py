from setuptools import find_packages, setup

package_name = 'abe_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[  # <-- add this
            ('share/ament_index/resource_index/packages',
                ['resource/' + package_name]),
            ('share/' + package_name, ['package.xml']),
            ('share/' + package_name + '/launch', ['launch/gantry.launch.py']),
            ('share/' + package_name + '/urdf', ['urdf/camera_gimbal.xacro']),
            ('share/' + package_name + '/urdf', ['urdf/gantry.xacro']),
            # add meshes if needed
            # ('share/' + package_name + '/meshes', ['meshes/your_mesh_file.stl']),
        ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='root@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
