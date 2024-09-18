import launch
from launch_ros.actions import Node


def generate_launch_description():
    return launch.LaunchDescription(
        [
            Node(
                package="ntrip",
                executable="ntrip",
                name="ntrip_client",
                output="screen",
                parameters=[
                    {
                        "ip": "on.smartnetna.com"
                    },  # Change to the IP address of Your NTRIP service
                    {"port": 9950},  # Change to your port number, WGS84
                    {"user": "uni02100102"},  # Change to your username
                    {"passwd": "707128"},  # Change to your password
                    {"mountpoint": "MSM_VRS_ITRF14"},  # Change to your mountpoint
                    {
                        "report_interval": 1
                    },  # the report interval to the NTRIP Caster, default is 1 sec
                ],
            ),
        ]
    )
