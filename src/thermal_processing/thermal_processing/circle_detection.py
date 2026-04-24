import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class CircleDetector(Node):
    def __init__(self):
        super().__init__('circle_detector')
        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/thermal_image', 
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(Image, '/circles_image', 10)

    def image_callback(self, msg):
        # Convert ROS2 image → OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono16')

        frame_min = cv_image.min()
        frame_max = cv_image.max()
        
        img_8bit = ((cv_image - frame_min) / (frame_max - frame_min) *255).astype(np.uint8)
        
        # Blur to remove noise
        gray = img_8bit
        gray = cv2.medianBlur(img_8bit, 3)
        

        # ---- Hough Circle Detection ----
        circles = cv2.HoughCircles(
            gray,
            cv2.HOUGH_GRADIENT,
            dp=2.5,           # smear out noise, reduces false positives
            minDist=60,       # prevents overlapping circles
            param1=180,       # high edge threshold
            param2=60,        # stricter circle detection
            minRadius=15,
            maxRadius=80
        )


        # Draw detected circles on the image
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(img_8bit, (x, y), r, (0, 255, 0), 3)
                cv2.circle(img_8bit, (x, y), 2, (0, 0, 255), 3)

        # Publish the processed image
        out_msg = self.bridge.cv2_to_imgmsg(img_8bit, encoding='mono8')
        self.publisher.publish(out_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CircleDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()