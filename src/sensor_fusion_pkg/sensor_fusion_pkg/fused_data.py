import rclpy
import numpy as np
from rclpy.node import Node

from sensor_msgs.msg import Imu, FluidPressure
from std_msgs.msg import Float32


# Use Allan Variance gain noise and bias instabilitty
IMU_N = 0.003 
IMU_B = 0.0001

DEPTH_SIGMA = 0.01

def compute_noise_matrices(dt, N, B, depth_sigma):
    """
    Convert Allan Variance parameters into EKF noise matrices.
    R: process noise
    Q: measurement noise
    """
    sigma_a  = N * (1.0 / np.sqrt(dt))   #
    sigma_b  = B * np.sqrt(dt)            

 
    R = np.diag([
        0.5 * (sigma_a ** 2) * (dt ** 2),   
        (sigma_a ** 2) * dt,               
        sigma_b ** 2                         
    ])

    # Measurement noise Q 1x1
    Q = np.array([[depth_sigma ** 2]])      

    return R, Q



class FusionNode(Node):

    def __init__(self):
        super().__init__('fused_data')
        dt = 0.01
        R, Q = compute_noise_matrices(dt, IMU_N, IMU_B, DEPTH_SIGMA)

        self.get_logger().info(f'R (process noise):\n{R}')
        self.get_logger().info(f'Q (measurement noise):\n{Q}')

        self.ekf = EKF(
            dt = dt,
            R = R,
            Q = Q,
            P0 = np.diag([0.1, 1.0, 0.1])

        )

        # two subscribes-imu & depth sensor
        self.imu_sub = self.create_subscription(Imu, '/imu/data', self.imu_callback, 10)
        self.depth_sub = self.create_subscription(FluidPressure, '/depth', self.depth_callback, 10)

        # One publisher- fused data
        self.vel_pub_ = self.create_publisher(Float32, '/vertical_velocity', 10)
        
        self.latest_accel_z = 0.0
        self.latest_depth = 0.0
        

    def imu_callback(self, msg):
        #linear accelerator
        self.latest_accel_z = msg.linear_acceleration.z
        self.ekf.predict(self.latest_accel_z)

    def depth_callback(self, msg):
        self.latest_depth = msg.fluid_pressure / (1000.0 * 9.81) # convert to meter
        self.ekf.update(self.latest_depth)

        vel_z_msg = Float32()
        vel_z_msg.data = float(self.ekf.velocity())
        self.vel_pub_.publish(vel_z_msg)
        self.get_logger().info(f'v_z estimate: {vel_z_msg.data:.4f} m/s')


class EKF:
    """
    state = x = [z, v_z, b_a]
    predict: IMU accel_z at xx Hz
    update: depth sensor measurement
    """
    def __init__(self, dt, R, Q, P0):
        self.dt = dt
        self.R = R
        self.Q = Q
        self.x = np.zeros((3,1))
        self.P = P0.copy()
        self.I = np.eye(3)

    def predict(self, accel_z):
        A = np.array([
            [1, self.dt, 0],
            [0, 1,     -self.dt],
            [0, 0,       1]
        ])
        g = 9.81
        B = np.array([[0], [self.dt], [0]])
        u = accel_z - g
        
        self.x = A @ self.x + B*u
        self.P = A @ self.P @ A.T + self.R

    def update(self, depth_meas):
        H = np.array([[1, 0, 0]])

        z_pred = self.x[0,0]
        innov = depth_meas - z_pred

        S = H @ self.P @ H.T + self.Q
        K = self.P @ H.T @ np.linalg.inv(S)

        self.x = self.x + K*innov
        self.P = (self.I - K @ H)  @ self.P
    
    def velocity(self):
        return self.x[1,0]

   

def main(args=None):
    rclpy.init(args=args)

    fused_data = FusionNode()

    rclpy.spin(fused_data)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    fused_data.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()