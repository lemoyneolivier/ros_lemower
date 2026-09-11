import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'lemower_package'
    file_subpath = 'description/lemower.xacro'


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()


    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True}] # add other parameters here if required
    )



    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
        )


    spawn_entity = Node(package='ros_gz_sim', executable='create',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'lemower',
				'-z', '0.3'],
                    output='screen')



    bridge_params = os.path.join(get_package_share_directory(package_name),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Permet de convertir les messages gz.msgs.Model2 en sensor_msgs/msg/JointState
            # '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model2'
	    'bridge_name:="ros_gz_bridge"',
            'config_file:={bridge_params}'
        ],
        remappings=[
            # Optionnel: si Gazebo publie sous un namespace, vous pouvez le mapper ici
            # ('/model/nom_du_robot/joint_states', '/joint_states')
        ],
        output='screen'
    )


    # Run the node
    return LaunchDescription([
        gazebo,
        node_robot_state_publisher,
        spawn_entity,
	ros_gz_bridge
    ])



