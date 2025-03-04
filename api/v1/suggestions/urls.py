from rest_framework.routers import DefaultRouter

from .views.antenna_suggestion_views import AntennaSuggestionAPIViewSet, AntennaTypeSuggestionAPIViewSet, \
    AntennaConnectorSuggestionAPIViewSet, ExistingAntennaDetailSuggestionAPIViewSet
from .views.camera_suggestion_views import VideoFormatSuggestionAPIViewSet, CameraSuggestionAPIViewSet, \
    ExistingCameraDetailSuggestionAPIViewSet
from .views.frame_suggestion_views import FrameSuggestionAPIViewSet, ExistingFrameCameraDetailSuggestionAPIViewSet, \
    ExistingFrameMotorDetailSuggestionAPIViewSet, ExistingFrameVTXDetailSuggestionAPIViewSet
from .views.motor_suggestion_views import MotorSuggestionAPIViewSet, ExistingMotorDetailSuggestionAPIViewSet, \
    RatedVoltageSuggestionAPIViewSet
from .views.propeller_suggestion_views import PropellerSuggestionAPIViewSet
from .views.receiver_suggestion_views import ReceiverProtocolTypeSuggestionAPIViewSet, ReceiverSuggestionAPIViewSet, \
    ExistingReceiverDetailSuggestionAPIViewSet
from .views.stack_suggestion_views import StackSuggestionAPIViewSet, GyroSuggestionAPIViewSet, \
    FlightControllerSuggestionAPIViewSet, SpeedControllerSuggestionAPIViewSet, \
    FlightControllerFirmwareSuggestionAPIViewSet, SpeedControllerProtocolSuggestionAPIViewSet, \
    SpeedControllerFirmwareSuggestionAPIViewSet
from .views.transmitter_suggestion_views import TransmitterSuggestionAPIViewSet, OutputPowerSuggestionAPIViewSet

app_name = 'api-v1-suggestions'
router = DefaultRouter(trailing_slash=True)
router.register(r'antennas', AntennaSuggestionAPIViewSet, basename="antenna")
router.register(r'antenna_types', AntennaTypeSuggestionAPIViewSet, basename="antenna_type")
router.register(r'antenna_connectors', AntennaConnectorSuggestionAPIViewSet, basename="antenna_connector")
router.register(r'antenna_details', ExistingAntennaDetailSuggestionAPIViewSet, basename="antenna_detail")

router.register(r'video_formats', VideoFormatSuggestionAPIViewSet, basename="video_format")
router.register(r'cameras', CameraSuggestionAPIViewSet, basename="camera")
router.register(r'camera_details', ExistingCameraDetailSuggestionAPIViewSet, basename="camera_detail")

router.register(r'frames', FrameSuggestionAPIViewSet, basename="frame")
router.register(r'frame_camera_details', ExistingFrameCameraDetailSuggestionAPIViewSet, basename="frame_camera_detail")
router.register(r'frame_motor_details', ExistingFrameMotorDetailSuggestionAPIViewSet, basename="frame_motor_detail")
router.register(r'frame_vtx_details', ExistingFrameVTXDetailSuggestionAPIViewSet, basename="frame_vtx_detail")

router.register(r'motors', MotorSuggestionAPIViewSet, basename="motor")
router.register(r'motor_details', ExistingMotorDetailSuggestionAPIViewSet, basename="motor_detail")
router.register(r'voltages', RatedVoltageSuggestionAPIViewSet, basename="rated_voltage")

router.register(r'propellers', PropellerSuggestionAPIViewSet, basename="propeller")

router.register(r'protocols', ReceiverProtocolTypeSuggestionAPIViewSet, basename="receiver_protocol_type")
router.register(r'receivers', ReceiverSuggestionAPIViewSet, basename="receiver")
router.register(r'receiver_details', ExistingReceiverDetailSuggestionAPIViewSet, basename="receiver_detail")

router.register('stacks', StackSuggestionAPIViewSet, basename="stack")
router.register('flight_controllers', FlightControllerSuggestionAPIViewSet, basename="flight_controller")
router.register('speed_controllers', SpeedControllerSuggestionAPIViewSet, basename="speed_controller")
router.register('gyros', GyroSuggestionAPIViewSet, basename="gyro")
router.register('fc_firmwares', FlightControllerFirmwareSuggestionAPIViewSet, basename="fc_firmware")
router.register('sc_firmwares', SpeedControllerFirmwareSuggestionAPIViewSet, basename="sc_firmware")
router.register('sc_protocols', SpeedControllerProtocolSuggestionAPIViewSet, basename="sc_protocol")


router.register('transmitters', TransmitterSuggestionAPIViewSet, basename="transmitter")
router.register('output_powers', OutputPowerSuggestionAPIViewSet, basename="output_power")


urlpatterns = [

] + router.urls
