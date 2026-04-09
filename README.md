# Sensor_Fusion_test-ROV Vertoical velocity Estimation

## Topic Overview
- /imu/data
- /depth
- vertical_velocity

## Code structure
<img width="400" height="200" alt="Screenshot from 2026-04-09 10-23-30" src="https://github.com/user-attachments/assets/2fab6c9f-a404-420f-84d8-f043f13bfc46" />


## How to run the node
### Step1 - Buid
cd /src
colcon build
### Step2 - Source
source install/setup.bash
### Step3 - Launch
ros2 launch ~/ros2/src/sensor_fusion_pkg/launch/fusion_launch.py

## Run in Docker
### Step1 - Build the image
sudo docker build -t rov_fusion .
### Step2 - Run the container
sudo docker run -it --network host -e ROS_DOMAIN_ID=0 rov_fusion
### Step3 - Verify from inside container
sudo docker exec -it $(sudo docker ps -q) /bin/bash
source /opt/ros/jazzy/setup.bash
source /ros2_ws/install/setup.bash
ros2 topic echo /vertical_velocity

