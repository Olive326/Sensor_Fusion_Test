# base image
FROM ros:jazzy

# install python dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-numpy \
    ros-jazzy-rclpy \
    ros-jazzy-std-msgs \
    ros-jazzy-sensor-msgs \
    && rm -rf /var/lib/apt/lists/*


# create workspace inside container
WORKDIR /ros2_ws

# copy package into the container
COPY src/sensor_fusion_pkg src/sensor_fusion_pkg

# build pkg
RUN /bin/bash -c "source /opt/ros/jazzy/setup.bash && \
    colcon build --packages-select sensor_fusion_pkg"

# source 
RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

# launch
CMD ["/bin/bash", "-c", \
    "source /opt/ros/jazzy/setup.bash && \
     source /ros2_ws/install/setup.bash && \
     ros2 launch /ros2_ws/src/sensor_fusion_pkg/launch/fusion_launch.py"]