import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import time

class ArduinoBridge(Node):

    def __init__(self):
        super().__init__('arduino_bridge')

        self.declare_parameter('device_port', '/dev/ttyACM0')
        port = self.get_parameter('device_port').value

        self.ser = serial.Serial(port,115200,timeout=0.1)
        time.sleep(2)

        self.vx = 0.0
        self.vy = 0.0

        self.create_subscription(
            Twist,
            '/motor/cmd_vel',
            self.velocity_callback,
            10
        )

        self.create_timer(0.02,self.send_serial_update)

        self.get_logger().info(f'Connected to Arduino on {port}')

    def velocity_callback(self,msg):
        self.vx = msg.linear.x
        self.vy = msg.linear.y

    def send_serial_update(self):
        message = f"{self.vx:.2f},{self.vy:.2f}\n"
        self.ser.write(message.encode())

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()