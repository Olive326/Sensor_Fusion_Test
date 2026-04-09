import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu


class FakeDepth(Node):

    def __init__(self):
        super().__init__('fake_depth')
        self.publisher_ = self.create_publisher(Float32, '/depth', 10)
        timer_period = 0.025  # 40hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0
        self.get_logger().info('Fake Depth started at 40Hz')

    def timer_callback(self):
    
        # simulate ROV is moving up and up
        true_depth = 1.0 - 0.5 * np.cos(self.i)
        # mimi sensor noise by adding Gaussian
        noise_depth = true_depth + np.random.normal(0.0, 0.01)

        msg = Float32()
        msg.data = float(noise_depth)

        msg.fluid_pressure = noise_depth * 1000.0 * 9.81
        msg.variance = 0.0001
      

        self.publisher_.publish(msg)
        self.i += 0.025


def main(args=None):
    rclpy.init(args=args)

    node = FakeDepth()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()