import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String, Float32  # Standard ROS 2 message type for text
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

        self.ser = serial.Serial(port, 115200, timeout=1)
        
        # CRITICAL: Wait 2 seconds for the Mega to reboot after opening Serial
        self.get_logger().info('Waiting for Arduino to reboot...')
        time.sleep(2) 

        # Optional: Send a "Wake Up" character if needed
        self.ser.write(b'\n')

        self.get_logger().info(f'Connected to Arduino on {port}')

        time.sleep(2)  # Wait a moment to ensure connection is stable
        

        # Create a ROS 2 subscriber
        # - Topic name: 'led_toggle'
        # - Message type: String
        # - Callback function: listener_callback
        # - Queue size: 10
        self.create_subscription(
            Float32,
            '/motor/pan_cmd',
            self.pan_callback,
            10
        )
        self.create_subscription(
            Float32,
            '/motor/tilt_cmd',
            self.tilt_callback,
            10
        )
        self.latest_tilt = 90
        self.latest_pan = 90
        self.create_timer(.05, self.send_serial_update)

        self.get_logger().info('Arduino bridge node started. Listening for motor commands')

    def pan_callback(self, msg):
        self.latest_pan = msg.data
    
    def tilt_callback(self, msg):
        self.latest_tilt = msg.data
    
    def send_serial_update(self):
        # Format message
        message = f"PAN:{self.latest_pan:.2f},TILT:{self.latest_tilt:.2f}\n"
        self.ser.write(message.encode('utf-8'))
        self.get_logger().debug(f"Sent: {message.strip()}")
        print(f"Sent: {message.strip()}")  # Also print to console for visibility



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
