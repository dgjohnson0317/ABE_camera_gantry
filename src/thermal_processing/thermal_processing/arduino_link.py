import rclpy
from rclpy.node import Node
from std_msgs.msg import String  # Standard ROS 2 message type for text
import serial  # Python serial communication library

class ArduinoBridge(Node):
    def __init__(self):
        # Initialize the node with the name "arduino_bridge"
        super().__init__('arduino_bridge')

        # Open the serial port (change '/dev/ttyACM0' if necessary)
        # You can check this using: `ls /dev/ttyACM*` or `ls /dev/ttyUSB*`

        # Declare a ROS parameter called 'device_port' with a default value
        self.declare_parameter('device_port', '/dev/ttyACM0')

        # Read the parameter value
        port = self.get_parameter('device_port').get_parameter_value().string_value

        # Now open that port
        self.ser = serial.Serial(port, 115200)

        self.get_logger().info(f'Connected to Arduino on {port}')


        # Create a ROS 2 subscriber
        # - Topic name: 'led_toggle'
        # - Message type: String
        # - Callback function: listener_callback
        # - Queue size: 10
        self.create_subscription(
            String,
            '/motor/pan_cmd',
            self.listener_callback,
            10
        )
        self.create_subscription(
            String,
            '/motor/tilk_cmd',
            self.listener_callback,
            10
        )

        self.get_logger().info('Arduino bridge node started. Listening for motor commands')

    def listener_callback(self, msg):
        # This function is called every time a message is received on the topic

        # Print the received message to the ROS 2 log
        self.get_logger().info(f'Received: "{msg.data}"')

        # Send the message data (as bytes) to the Arduino over serial
        # For example, if msg.data = "1", it sends the character '1'
        self.ser.write(msg.data.encode())

def main(args=None):
    # Initialize the ROS 2 system
    rclpy.init(args=args)

    # Create the node
    node = ArduinoBridge()

    # Keep the node alive and listening for messages
    rclpy.spin(node)

    # Clean up after exiting (e.g., Ctrl+C)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
