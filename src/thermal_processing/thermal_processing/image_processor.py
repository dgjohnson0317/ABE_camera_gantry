import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import numpy as np

class ThermalROIDetector(Node):
    def __init__(self):
        super().__init__('thermal_roi_detector')
        self.bridge = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            '/thermal_image',  # adjust to your actual Optris topic
            self.image_callback,
            10
        )

        self.image_publisher = self.create_publisher(Image, '/thermal_image_annotated' , 10)
        self.location_publisher = self.create_publisher(String, '/thermal_image_max_location' , 10)
        
    def image_callback(self, msg):
        # Convert ROS image to OpenCV
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='mono16')

        # Normalize to 8-bit for visualization
        frame_min = cv_image.min()
        frame_max = cv_image.max()
        img_8bit = ((cv_image - frame_min) / (frame_max - frame_min) * 255).astype(np.uint8)

        # --- HOT REGION DETECTION ---

        # Step 1: Threshold for top few percent of hot pixels
        thresh_val = np.percentile(cv_image, 98)  # top 2%
        _, thresh = cv2.threshold(cv_image, thresh_val, 65535, cv2.THRESH_BINARY)

        # Step 2: Morphological filtering to merge nearby hot spots
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Step 3: Find connected components
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh.astype(np.uint8))

        if num_labels > 1:
            # Skip background (index 0)
            largest_idx = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1
            centroid = tuple(map(int, centroids[largest_idx]))
        else:
            # Fallback: just use the hottest pixel
            _, _, _, max_loc = cv2.minMaxLoc(cv_image)
            centroid = max_loc

        # Step 4: Define fixed ROI around the centroid
        roi_size = 40
        x1 = max(centroid[0] - roi_size // 2, 0)
        y1 = max(centroid[1] - roi_size // 2, 0)
        x2 = min(centroid[0] + roi_size // 2, cv_image.shape[1])
        y2 = min(centroid[1] + roi_size // 2, cv_image.shape[0])

        roi = cv_image[y1:y2, x1:x2]
        avg_temp = np.mean(roi)

        # Step 5: Annotate visualization image
        color = 128  # white in mono8
        cv2.rectangle(img_8bit, (x1, y1), (x2, y2), color, 2)
        cv2.circle(img_8bit, centroid, 6, color, 2)
        #cv2.putText(img_8bit, f"Avg: {avg_temp*.01:.1f}", (centroid[0]+10, centroid[1]),
        #           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

        # Step 6: Publish annotated image and location
        annotated_msg = self.bridge.cv2_to_imgmsg(img_8bit, encoding='mono8')
        self.image_publisher.publish(annotated_msg)
        self.location_publisher.publish(String(data=str(centroid)))
        

def main(args=None):
    rclpy.init(args=args)
    node = ThermalROIDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
