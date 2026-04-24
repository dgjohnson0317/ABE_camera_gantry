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
        self.pan_pub = self.create_publisher(Float32, '/motor/pan_cmd', 3)
        self.tilt_pub = self.create_publisher(Float32, '/motor/tilt_cmd', 3)

        # Frame dimensions (you can parametrize this)
        self.frame_width = 382 #for pi400
        self.frame_height = 288

        # Control gains (tune these)
        self.kp_pan = 200.0 # steps/ sec per pixel of error (try 200-500)
        self.kp_tilt = 200.0
        
        self.deadband = 0.2
        #self.smoothing_factor = .2

        self.get_logger().info("Camera Tracker Node started")

    def callback(self, msg):
        try:
            # Parse centroid from String like "(x, y)"
            centroid = json.loads(msg.data) if msg.data.startswith('{') else eval(msg.data)
            cx, cy = centroid
        except Exception as e:
            self.get_logger().error(f"Invalid centroid data: {msg.data}")
            return

        print(f"Received centroid: ({cx}, {cy})")
        # Center of frame
        cx_target = self.frame_width / 2
        cy_target = self.frame_height / 2

        # Normalized error (-1, 1)
        error_x = (cx_target - cx) / (self.frame_width / 2)
        error_y = (cy_target - cy) / (self.frame_height / 2)

        # Deadband to prevent jitter
        if abs(error_x) < self.deadband:
            error_x = 0.0
        if abs(error_y) < self.deadband:
            error_y = 0.0

        # Convert to velocity
        vel_pan = self.kp_pan * error_x
        vel_tilt = self.kp_tilt * error_y

        # Clamp angles
        max_speed = 800.0
        vel_pan = max(-max_speed, min(max_speed, vel_pan))
        vel_tilt = max(-max_speed, min(max_speed, vel_tilt))

        # Publish velocities
        self.pan_pub.publish(Float32(data=vel_pan))
        self.tilt_pub.publish(Float32(data=vel_tilt))
        
        self.get_logger().info(
            f"errx={error_x:.2f}, erry={error_y:.2f} | "
            f"vel_pan={vel_pan:.1f}, vel_tilt={vel_tilt:.1f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = CameraTracker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()