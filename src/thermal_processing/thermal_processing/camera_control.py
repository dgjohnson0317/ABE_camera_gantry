import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
import json

class CameraTracker(Node):
    def __init__(self):
        super().__init__('camera_tracker')

        self.subscription = self.create_subscription(
            String,
            '/thermal_image_max_location',
            self.callback,
            10
        )

        # Publishers to your motor controller
        self.pan_pub = self.create_publisher(Float32, '/motor/pan_cmd', 10)
        self.tilt_pub = self.create_publisher(Float32, '/motor/tilt_cmd', 10)

        # Frame dimensions (you can parametrize this)
        self.frame_width = 640
        self.frame_height = 480

        # Control gains (tune these)
        self.kp_pan = 0.3
        self.kp_tilt = 0.3
        self.smoothing_factor = .2

        self.current_pan = 90
        self.current_tilt = 90

        self.get_logger().info("Camera Tracker Node started")

    def callback(self, msg):
        try:
            # Parse centroid from String like "(x, y)"
            centroid = json.loads(msg.data) if msg.data.startswith('{') else eval(msg.data)
            cx, cy = centroid
        except Exception as e:
            self.get_logger().error(f"Invalid centroid data: {msg.data}")
            return

        # Compute pixel error
        cx_target = self.frame_width / 2
        cy_target = self.frame_height / 2
        error_x = cx_target - cx
        error_y = cy_target - cy
        # Scale errors into servo degrees (small proportional response)
        delta_pan = self.kp_pan * (error_x / (self.frame_width / 2)) * 90  # maps ±320 px → ±90°
        delta_tilt = self.kp_tilt * (error_y / (self.frame_height / 2)) * 90  # maps ±240 px → ±90°

        # Compute desired target positions
        target_pan = 90 + delta_pan
        target_tilt = 90 + delta_tilt

        # Clamp angles
        target_pan = max(0, min(180, target_pan))
        target_tilt = max(0, min(180, target_tilt))

        # Exponential smoothing
        self.current_pan = (1 - self.smoothing_factor) * self.current_pan + self.smoothing_factor * target_pan
        self.current_tilt = (1 - self.smoothing_factor) * self.current_tilt + self.smoothing_factor * target_tilt

        # Publish smoothed angles
        self.pan_pub.publish(Float32(data=self.current_pan))
        self.tilt_pub.publish(Float32(data=self.current_tilt))

        self.get_logger().info(
            f"Target Pan={target_pan:.1f}, Tilt={target_tilt:.1f} | "
            f"Smoothed Pan={self.current_pan:.1f}, Tilt={self.current_tilt:.1f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = CameraTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()