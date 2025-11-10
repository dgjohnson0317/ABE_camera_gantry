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
        self.kp_pan = 0.005
        self.kp_tilt = 0.005

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

        # Simple proportional control
        pan_speed = self.kp_pan * error_x
        tilt_speed = self.kp_tilt * error_y

        # Publish control signals
        self.pan_pub.publish(Float32(data=pan_speed))
        self.tilt_pub.publish(Float32(data=tilt_speed))

        self.get_logger().info(f"Pan: {pan_speed:.3f}, Tilt: {tilt_speed:.3f}")


def main(args=None):
    rclpy.init(args=args)
    node = CameraTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()