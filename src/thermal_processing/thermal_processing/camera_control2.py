import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
import json
import time

class CameraTracker(Node):
    def __init__(self):
        super().__init__('camera_tracker')

        self.subscription = self.create_subscription(
            String,
            '/thermal_image_max_location',
            self.callback,
            10
        )

        self.pan_pub = self.create_publisher(Float32, '/motor/pan_cmd', 3)
        self.tilt_pub = self.create_publisher(Float32, '/motor/tilt_cmd', 3)

        self.frame_width = 382
        self.frame_height = 288

        # Tune these
        self.kp_pan = 200.0
        self.kp_tilt = 200.0

        self.kd_pan = 150.0
        self.kd_tilt = 150.0

        self.deadband = 0.02
        self.max_speed = 800.0

        # State for derivative
        self.prev_error_x = 0.0
        self.prev_error_y = 0.0
        self.prev_time = time.time()

        self.get_logger().info("Camera Tracker (PD Control) started")

    def callback(self, msg):
        try:
            centroid = json.loads(msg.data) if msg.data.startswith('{') else eval(msg.data)
            cx, cy = centroid
        except:
            self.get_logger().error(f"Invalid centroid data: {msg.data}")
            return

        # Time delta
        current_time = time.time()
        dt = current_time - self.prev_time
        self.prev_time = current_time

        if dt <= 0:
            return

        # Center of frame
        cx_target = self.frame_width / 2
        cy_target = self.frame_height / 2

        # Normalized error [-1, 1]
        error_x = (cx_target - cx) / (self.frame_width / 2)
        error_y = (cy_target - cy) / (self.frame_height / 2)

        # Deadband
        if abs(error_x) < self.deadband:
            error_x = 0.0
        if abs(error_y) < self.deadband:
            error_y = 0.0

        # Derivative (rate of change)
        d_error_x = (error_x - self.prev_error_x) / dt
        d_error_y = (error_y - self.prev_error_y) / dt

        self.prev_error_x = error_x
        self.prev_error_y = error_y

        # PD control
        vel_pan = self.kp_pan * error_x + self.kd_pan * d_error_x
        vel_tilt = self.kp_tilt * error_y + self.kd_tilt * d_error_y

        # Clamp
        vel_pan = max(-self.max_speed, min(self.max_speed, vel_pan))
        vel_tilt = max(-self.max_speed, min(self.max_speed, vel_tilt))

        # Publish
        self.pan_pub.publish(Float32(data=vel_pan))
        self.tilt_pub.publish(Float32(data=vel_tilt))

        self.get_logger().info(
            f"err=({error_x:.2f},{error_y:.2f}) "
            f"vel=({vel_pan:.1f},{vel_tilt:.1f})"
        )


def main(args=None):
    rclpy.init(args=args)
    node = CameraTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()