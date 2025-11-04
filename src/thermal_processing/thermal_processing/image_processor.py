import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class ThermalROIDetector(Node):
    def __init__(self):
        super().__init__('thermal_roi_detector')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/optris/image_raw',  # adjust to your actual Optris topic
            self.image_callback,
            10
        )

    def image_callback(self, msg):
        # Convert ROS image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono16')

        # Normalize to 8-bit for visualization
        img_8bit = cv2.convertScaleAbs(cv_image, alpha=(255.0 / 65535.0))

        # Example: find hottest spot
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(cv_image)
        cv2.circle(img_8bit, max_loc, 10, (255, 255, 255), 2)
        cv2.putText(img_8bit, f"Max: {max_val:.1f}", (max_loc[0]+15, max_loc[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255), 1)

        # Display for testing
        cv2.imshow("Thermal ROI", img_8bit)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ThermalROIDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
