# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information
import copy

#--------------------------------------------------------------------------
# object types

IOTHUB_SERVICE = "iothub_service"
IOTHUB_DEVICE = "iothub_device"
IOTHUB_MODULE = "iothub_module"
IOTEDGE_DEVICE = "iotedge_device"
EDGEHUB_MODULE = "edgehub_module"

valid_object_types = [
    IOTHUB_SERVICE,
    IOTHUB_DEVICE,
    IOTHUB_MODULE,
    IOTEDGE_DEVICE,
    EDGEHUB_MODULE,
]

#--------------------------------------------------------------------------
# transports

MQTT = "mqtt"
MQTTWS = "mqttws"
AMQP = "amqp"
AMQPWS = "amqpws"
HTTP = "http"

valid_transports = [MQTT, MQTTWS, AMQP, AMQPWS, HTTP]

#--------------------------------------------------------------------------
# languages

NODE = "node"
C = "c"
CSHARP = "csharp"
JAVA = "java"
PYTHON = "python"
PYTHONPREVIEW = "pythonpreview"

valid_languages = [NODE, C, CSHARP, JAVA, PYTHON, PYTHONPREVIEW]

#--------------------------------------------------------------------------
# adapter types

REST_ADAPTER = "rest_adapter"
DIRECT_AZURE_ADAPTER = "direct_azure_adapter"
DIRECT_PYTHON_SDK_ADAPTER = "direct_python_sdk_adapter"

valid_adapters = [
    REST_ADAPTER,
    DIRECT_AZURE_ADAPTER,
    DIRECT_PYTHON_SDK_ADAPTER,
]

#--------------------------------------------------------------------------
# API surfaces

MODULE_API = "ModuleApi"
DEVICE_API = "DeviceApi"
SERVICE_API = "ServiceApi"
REGISTRY_API = "RegistryApi"

valid_api_surfaces = [MODULE_API, DEVICE_API, SERVICE_API, REGISTRY_API]

#--------------------------------------------------------------------------
# connection types

CONNECTION_STRING = connection_string
ENVIRONMENT = "environment"
CONNECTION_STRING_WITH_GATEWAY = "connection_string_with-gateway"

valid_connection_types = [
    CONNECTION_STRING,
    ENVIRONMENT,
    CONNECTION_STRING_WITH_GATEWAY,
]

#--------------------------------------------------------------------------
# value markers

SET_AT_RUNTIME = "undefined, needs to be set at runtime"
NOT_USED_YET = "unused for now, will be used in future code"

class IotHubServiceRest():
    def __init(self, api_name):
        self.test_object_type = IOTHUB_SERVICE
        self.connection_type = CONNECTION_STRING
        self.docker_image = NOT_USED_YET
        self.language = SET_AT_RUNTIME
        self.connection_string = SET_AT_RUNTIME
        self.adapter_type = REST_ADAPTER
        self.rest_uri = SET_AT_RUNTIME
        self.api_name = api_name
        self.api_surface = SERVICE_API
        self.adapter_name = "ServiceClient"

class IotHubServiceDirect(IotHubServiceRest):
    def __init(self, api_name):
        IotHubServiceRest.__init__(self, api_name)
        self.language = PYTHONPREVIEW
        self.adapter_type = DIRECT_AZURE_ADAPTER
        # del self.rest_uri
        del self.docker_image

class IotHubRegistryRest():
    def __init(self, api_name):
        self.test_object_type = IOTHUB_SERVICE
        self.connection_type = CONNECTION_STRING
        self.docker_image = NOT_USED_YET
        self.language = SET_AT_RUNTIME
        self.connection_string = SET_AT_RUNTIME
        self.adapter_type = REST_ADAPTER
        self.rest_uri = SET_AT_RUNTIME
        self.api_name = api_name
        self.api_surface = SERVICE_API
        self.adapter_name = "RegistryClient"

class IotHubRegistryDirect(IotHubRegistryRest):
    def __init(self, api_name):
        IotHubRegistryRest.__init__(self, api_name)
        self.language = PYTHONPREVIEW
        self.adapter_type = DIRECT_AZURE_ADAPTER
        # del self.rest_uri
        del self.docker_image

class IotEdgeDevice():
    def __init__(self):
        self.test_object_type = IOTEDGE_DEVICE
        self.connection_string = SET_AT_RUNTIME
        self.device_id = SET_AT_RUNTIME

class EdgeHubModuleRest():
    def __init(self, api_name):
        self.test_object_type = EDGEHUB_MODULE
        self.connection_type = ENVIRONMENT
        self.docker_image = NOT_USED_YET 
        self.language = SET_AT_RUNTIME
        self.connection_string = SET_AT_RUNTIME
        self.device_id = SET_AT_RUNTIME
        self.module_id = SET_AT_RUNTIME
        self.adapter_type = REST_ADAPTER
        self.rest_uri = SET_AT_RUNTIME
        self.api_name = api_name
        self.api_surface = MODULE_API
        self.adapter_name = "ModuleApi"
        self.transport = MQTT
        self.gatewayhostname = SET_AT_RUNTIME

class EdgeHubModuleDirect(EdgeHubModuleRest):
    def __init__(self, api_name):
        EdgeHubModuleRest(self, api_name)
        self.language = PYTHONPREVIEW
        self.adapter_type = DIRECT_PYTHON_SDK_ADAPTER
        a #del self.rest_uri
        del self.docker_image

class  EdgeHubLeafDeviceRest():()
    def __init(self, api_name):
        self.test_object_type = IOTHUB_DEVICE
        self.connection_type = CONNECTION_STRING_WITH_GATEWAY
        self.docker_image = NOT_USED_YET 
        self.language = SET_AT_RUNTIME
        self.connection_string = SET_AT_RUNTIME
        self.device_id = SET_AT_RUNTIME
        self.adapter_type = REST_ADAPTER
        self.rest_uri = SET_AT_RUNTIME
        self.api_name = api_name
        self.api_surface = DEVICE_API
        self.AdapterName = "DeviceApi"
        self.transport = MQTT
        self.gatewayhostname = SET_AT_RUNTIME

class EdgeHubLeafDeviceDirect(EdgeHubLeafDeviceRest):
    def __init__(self, api_name):
        EdgeHubLeafDeviceRest(self, api_name)
        self.language = PYTHONPREVIEW
        self.adapter_type = DIRECT_PYTHON_SDK_ADAPTER
        # del self.rest_uri
        del self.docker_image
