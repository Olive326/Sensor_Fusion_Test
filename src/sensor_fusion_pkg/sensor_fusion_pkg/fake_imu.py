import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Imu, FluidPressure


class FakeImu(Node):

    def __init__(self):
        super().__init__('fake_imu')
        self.publisher_ = self.create_publisher(Imu, '/imu/data', 10)
        timer_period = 0.01  # 100hz
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.t = 0
        self.get_logger().info('Fake IMU started at 100Hz')

    def timer_callback(self):
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        true_accel_z = 9.81 + 0.3 * np.sin(self.t)

        msg.linear_acceleration.x = np.random.normal(0.0, 0.01)
        msg.linear_acceleration.y = np.random.normal(0.0, 0.01)
        msg.linear_acceleration.z = true_accel_z + np.random.normal(0.0, 0.05)

        msg.angular_velocity.x = np.random.normal(0.0, 0.001)
        msg.angular_velocity.y = np.random.normal(0.0, 0.001)
        msg.angular_velocity.z = np.random.normal(0.0, 0.001)

        msg.orientation_covariance[0] = -1.0

        self.publisher_.publish(msg)
        self.t += 0.01


def main(args=None):
    rclpy.init(args=args)

    node = FakeImu()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()