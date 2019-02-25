# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information

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
DIRECT_AZURE_REST_ADAPTER = "direct_azure_rest_adapter"
DIRECT_PYTHON_SDK_ADAPTER = "direct_python_sdk_adapter"

valid_adapters = [
    REST_ADAPTER,
    DIRECT_AZURE_REST_ADAPTER,
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

CONNECTION_STRING = "connection_string"
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

def get_runconfig():
    return {
        "test_objects": {
            "iothub": {
                "type": IOTHUB_SERVICE,
                "connection_type": CONNECTION_STRING,
                "deployment": {"image": NOT_USED_YET, "language": SET_AT_RUNTIME},
                "azure_identity": {"conneciton_string": SET_AT_RUNTIME},
                "adapters": [
                    {
                        "adapter_type": REST_ADAPTER,
                        "uri": "http://localhost:8099",
                        "api_name": "service_api",
                        "api_surface": SERVICE_API,
                    },
                    {
                        "adapter_type": REST_ADAPTER,
                        "uri": "http://localhost:8099",
                        "api_name": "registry_api",
                        "api_surface": REGISTRY_API,
                    },
                ],
            },
            "iotedge": {
                "type": IOTEDGE_DEVICE,
                "azure_identity": {
                    "connection_string": SET_AT_RUNTIME,
                    "device_id": SET_AT_RUNTIME,
                },
            },
            "friend_mod": {
                "type": EDGEHUB_MODULE,
                "connection_type": ENVIRONMENT,
                "parent": "iotedge",
                "deployment": {"image": NOT_USED_YET, "language": SET_AT_RUNTIME},
                "azure_identity": {
                    "connection_string": SET_AT_RUNTIME,
                    "deviceId": SET_AT_RUNTIME,
                    "moduleId": SET_AT_RUNTIME,
                },
                "adapters": {
                    "adapter_type": REST_ADAPTER,
                    "uri": "http://localhost:8099",
                    "api_name": "friend_module",
                    "api_surface": MODULE_API,
                },
                "parameters": {
                    "transport": MQTT,
                    "gatewayhostname": SET_AT_RUNTIME,
                },
            },
            "test_mod": {
                "type": EDGEHUB_MODULE,
                "connection_type": ENVIRONMENT,
                "parent": "iotedge",
                "deployment": {"image": NOT_USED_YET, "language": SET_AT_RUNTIME},
                "azure_identity": {
                    "connection_string": SET_AT_RUNTIME,
                    "deviceId": SET_AT_RUNTIME,
                    "moduleId": SET_AT_RUNTIME,
                },
                "adapters": {
                    "adapter_type": REST_ADAPTER,
                    "uri": "http://localhost:8099",
                    "api_name": "test_module",
                    "api_surface": MODULE_API,
                },
                "parameters": {
                    "transport": SET_AT_RUNTIME,
                    "gatewayhostname": SET_AT_RUNTIME,
                },
            },
            "leaf_device": {
                "type": IOTHUB_DEVICE,
                "connection_type": CONNECTION_STRING_WITH_GATEWAY,
                "deployment": {"image": NOT_USED_YET, "language": SET_AT_RUNTIME},
                "azure_identity": {
                    "connection_string": SET_AT_RUNTIME,
                    "deviceId": SET_AT_RUNTIME,
                },
                "adapters": {
                    "adapter_type": REST_ADAPTER,
                    "uri": "http://localhost:8099",
                    "api_name": "leaf_device",
                    "api_surface": DEVICE_API,
                },
                "parameters": {
                    "transport": SET_AT_RUNTIME,
                    "gatewayhostname": SET_AT_RUNTIME,
                },
            },
        }
    }
