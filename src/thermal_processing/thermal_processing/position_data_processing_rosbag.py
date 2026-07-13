import rclpy
from rclpy.node import Node
import tf2_ros
import numpy as np

from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
from scipy.spatial.transform import Rotation as R


class TCPVisualizer(Node):
    def __init__(self):
        super().__init__('tcp_visualizer')

        # TF
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publishers
        self.twist_pos_pub = self.create_publisher(Twist, '/tcp/position', 10)
        self.twist_vel_pub = self.create_publisher(Twist, '/tcp/velocity', 10)
        self.twist_acc_pub = self.create_publisher(Twist, '/tcp/acceleration', 10)


        # State
        self.prev_t = None
        self.prev_pos = None
        self.prev_vel = None
        self.prev_quat = None
        self.prev_omega = None

        self.path_points = []

        # Timer (adjust for bag playback rate)
        self.timer = self.create_timer(0.01, self.update)

    def vec3_to_twist(self, linear, angular):
        msg = Twist()
        msg.linear.x, msg.linear.y, msg.linear.z = linear
        msg.angular.x, msg.angular.y, msg.angular.z = angular
        return msg


    def update(self):
        try:
            t = self.tf_buffer.lookup_transform(
                'base',
                'rob1_nozzle_tcp',
                rclpy.time.Time(),
                timeout=rclpy.duration.Duration(seconds=0.1)
            )

            time = t.header.stamp.sec + t.header.stamp.nanosec * 1e-9

            pos = np.array([
                t.transform.translation.x,
                t.transform.translation.y,
                t.transform.translation.z
            ])

            q_now = np.array([
                t.transform.rotation.x,
                t.transform.rotation.y,
                t.transform.rotation.z,
                t.transform.rotation.w
            ])

            # Defaults
            vel = np.zeros(3)
            acc = np.zeros(3)
            omega = np.zeros(3)
            alpha = np.zeros(3)
            rotvec = np.zeros(3)

            if self.prev_t is None:
                # First frame → just store and exit
                self.prev_t = time
                self.prev_pos = pos
                self.prev_quat = q_now
                return

            dt = time - self.prev_t
            if dt <= 0:
                return

            # -----------------------
            # Linear velocity + accel
            # -----------------------
            vel = (pos - self.prev_pos) / dt

            if self.prev_vel is not None:
                acc = (vel - self.prev_vel) / dt

            # -----------------------
            # Angular velocity + accel
            # -----------------------
            if self.prev_quat is not None:
                r_prev = R.from_quat(self.prev_quat)
                r_now = R.from_quat(q_now)

                r_delta = r_now * r_prev.inv()
                rotvec = r_delta.as_rotvec()
                omega = rotvec / dt

            if self.prev_omega is not None:
                alpha = (omega - self.prev_omega) / dt

            # -----------------------
            # Publish
            # -----------------------
            self.twist_pos_pub.publish(self.vec3_to_twist(pos, rotvec))
            self.twist_vel_pub.publish(self.vec3_to_twist(vel, omega))
            self.twist_acc_pub.publish(self.vec3_to_twist(acc, alpha))

            # -----------------------
            # Update state
            # -----------------------
            self.prev_t = time
            self.prev_pos = pos
            self.prev_quat = q_now
            self.prev_vel = vel
            self.prev_omega = omega

        except Exception as e:
            self.get_logger().warn(str(e))
# -----------------------
# MAIN
# -----------------------
def main():
    rclpy.init()
    node = TCPVisualizer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()