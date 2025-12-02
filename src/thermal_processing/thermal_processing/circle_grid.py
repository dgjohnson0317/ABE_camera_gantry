#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
import yaml
import os

class CircleGridCalibrator(Node):
    def __init__(self):
        super().__init__('circle_grid_calibrator')

        # Parameters
        self.declare_parameter('image_topic', '/circles_image')
        self.declare_parameter('pattern_rows', 3)    # number of circle rows
        self.declare_parameter('pattern_cols', 3)   # number of circle columns
        self.declare_parameter('square_size', 0.024) # meters
        self.declare_parameter('output_file', 'circle_camera_calibration.yaml')

        self.image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.pattern_size = (self.get_parameter('pattern_cols').get_parameter_value().integer_value,
                             self.get_parameter('pattern_rows').get_parameter_value().integer_value)
        self.square_size = self.get_parameter('square_size').get_parameter_value().double_value
        self.output_file = self.get_parameter('output_file').get_parameter_value().string_value

        # ROS2 subscription
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, self.image_topic, self.image_callback, 10)

        # Storage for calibration
        self.objpoints = []  # 3D points in real world space
        self.imgpoints = []  # 2D points in image plane

        # Prepare object points (0,0,0), (1*square_size, 0, 0), ...
        objp = np.zeros((self.pattern_size[0]*self.pattern_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.pattern_size[0], 0:self.pattern_size[1]].T.reshape(-1, 2)
        objp *= self.square_size
        self.objp = objp

        self.frame_count = 0
        self.max_frames = 20  # number of successful frames to collect
        self.get_logger().info(f"Listening to {self.image_topic}, waiting for circle grid images...")

    def image_callback(self, msg):
        try:
            # Convert ROS2 Image → OpenCV grayscale
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono8')
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # Find the circle grid
        found, centers = cv2.findCirclesGrid(cv_image, self.pattern_size, flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

        vis = cv2.cvtColor(cv_image, cv2.COLOR_GRAY2BGR)
        if found:
            cv2.drawChessboardCorners(vis, self.pattern_size, centers, found)
            if self.frame_count < self.max_frames:
                self.imgpoints.append(centers)
                self.objpoints.append(self.objp)
                self.frame_count += 1
                self.get_logger().info(f"Collected frame {self.frame_count}/{self.max_frames}")
        else:
            cv2.putText(vis, "Pattern not found", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        # Show detection
        cv2.imshow("Circle Grid Detection", vis)
        cv2.waitKey(1)

        # If enough frames collected, calibrate and save
        if self.frame_count >= self.max_frames:
            ret, K, dist, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, cv_image.shape[::-1], None, None)
            self.save_calibration(K, dist)
            self.get_logger().info(f"Calibration finished and saved to {self.output_file}")
            rclpy.shutdown()

    def save_calibration(self, K, dist):
        data = {
            'camera_matrix': K.tolist(),
            'distortion_coefficients': dist.tolist()
        }
        with open(self.output_file, 'w') as f:
            yaml.dump(data, f)

def main(args=None):
    rclpy.init(args=args)
    node = CircleGridCalibrator()
    rclpy.spin(node)
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()





#ros2 run circle_calibration circle_calibrator \
#    --ros-args -p image_topic:=/camera/image_raw \
#               -p pattern_rows:=4 \
#               -p pattern_cols:=11 \
#               -p square_size:=0.024 \
#               -p output_file:=circle_camera.yaml


