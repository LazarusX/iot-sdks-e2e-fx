import connexion
import six

from swagger_server.models.connect_response import ConnectResponse  # noqa: E501
from swagger_server import util


def service_connect_put(connectionString):  # noqa: E501
    """Connect to service

    Connect to the Azure IoTHub service.  More specifically, the SDK saves the connection string that is passed in for future use. # noqa: E501

    :param connectionString: Service connection string
    :type connectionString: str

    :rtype: ConnectResponse
    """
    return 'do some magic!'


def service_connection_id_device_method_device_id_put(connectionId, deviceId, methodInvokeParameters):  # noqa: E501
    """call the given method on the given device

     # noqa: E501

    :param connectionId: Id for the connection
    :type connectionId: str
    :param deviceId: 
    :type deviceId: str
    :param methodInvokeParameters: 
    :type methodInvokeParameters: 

    :rtype: object
    """
    return 'do some magic!'


def service_connection_id_disconnect_put(connectionId):  # noqa: E501
    """Disconnect from the service

    Disconnects from the Azure IoTHub service.  More specifically, closes all connections and cleans up all resources for the active connection # noqa: E501

    :param connectionId: Id for the connection
    :type connectionId: str

    :rtype: None
    """
    return 'do some magic!'


def service_connection_id_module_method_device_id_module_id_put(connectionId, deviceId, moduleId, methodInvokeParameters):  # noqa: E501
    """call the given method on the given module

     # noqa: E501

    :param connectionId: Id for the connection
    :type connectionId: str
    :param deviceId: 
    :type deviceId: str
    :param moduleId: 
    :type moduleId: str
    :param methodInvokeParameters: 
    :type methodInvokeParameters: 

    :rtype: object
    """
    return 'do some magic!'
