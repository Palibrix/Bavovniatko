"""
Component pair compatibility checkers registry.
This module manages compatibility checkers for component pairs.
"""

# Registry to store checkers by component pair key
_CHECKERS = {}


def register_checker(component1, component2, checker_class):
    """
    Register a compatibility checker for a pair of component types.

    Args:
        component1: First component type (e.g., 'camera')
        component2: Second component type (e.g., 'frame')
        checker_class: Checker class to handle this component pair
    """
    # Sort component types for consistent key generation
    key = frozenset([component1, component2])
    _CHECKERS[key] = checker_class()


def get_checker(component1, component2):
    """
    Get the appropriate compatibility checker for a pair of component types.

    Args:
        component1: First component type
        component2: Second component type

    Returns:
        Compatibility checker instance, or None if no checker exists
    """
    key = frozenset([component1, component2])
    return _CHECKERS.get(key)


# For testing, we'll import this directly to ensure it's registered
# In production, you would implement auto-discovery
from api.v1.compatibility.checkers.camera_frame import CameraFrameCompatibilityChecker
from api.v1.compatibility.checkers.antenna_receiver import AntennaReceiverCompatibilityChecker
from api.v1.compatibility.checkers.antenna_transmitter import AntennaTransmitterCompatibilityChecker
# from api.v1.compatibility.checkers.battery_flight_controller import BatteryFlightControllerCompatibilityChecker
from api.v1.compatibility.checkers.battery_motor import BatteryMotorCompatibilityChecker
# from api.v1.compatibility.checkers.battery_speed_controller import BatterySpeedControllerCompatibilityChecker
from api.v1.compatibility.checkers.battery_transmitter import BatteryTransmitterCompatibilityChecker
from api.v1.compatibility.checkers.camera_transmitter import CameraTransmitterCompatibilityChecker
from api.v1.compatibility.checkers.frame_propeller import FramePropellerCompatibilityChecker
from api.v1.compatibility.checkers.frame_transmitter import FrameTransmitterCompatibilityChecker
from api.v1.compatibility.checkers.flight_controller_speed_controller import FlightControllerSpeedControllerCompatibilityChecker
from api.v1.compatibility.checkers.motor_frame import MotorFrameCompatibilityChecker
from api.v1.compatibility.checkers.motor_speed_controller import MotorSpeedControllerCompatibilityChecker
from api.v1.compatibility.checkers.receiver_flight_controller import ReceiverFlightControllerCompatibilityChecker