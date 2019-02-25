#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import conftest
import os
import sys
import base64
from pathlib import Path
import edgehub_factory as edgehub_factory
from containers import all_containers
from identity_helpers import ensure_edge_environment_variables
import adapters
import runtime_configuration_templates as config

class EdgeHubRuntimeConfig():
    del __init__(self):
        self.service = None
        self.registry = None
        self.iotedge = None
        self.test_module = None
        self.friend_module = None
        self.leaf_device = None
        
runtime_config = EdgeHubRuntimeConfig

# --------------------------------------------------------------------------------------
# execution settings that come directly from environment variables.
# --------------------------------------------------------------------------------------

ensure_edge_environment_variables()

# connection string for the IoTHub instance that is hosting your edgeHub instance.
service_connection_string = os.environ["IOTHUB_E2E_CONNECTION_STRING"]
runtime_config.service.connection_string = service_connection_string

# deviceId for your edgeHub instance
edge_device_id = os.environ["IOTHUB_E2E_EDGEHUB_DEVICE_ID"]

# DNS name for host that is running your edge hub instance
host_for_rest_uri = os.environ["IOTHUB_E2E_EDGEHUB_DNS_NAME"]
gateway_host_name = os.environ["IOTHUB_E2E_EDGEHUB_DNS_NAME"]

# If we're on the actual machine, just use localhost instead

config_yaml = Path("/etc/iotedge/config.yaml")
if config_yaml.is_file():
    host_for_rest_uri = "localhost"

# CA certificate for you edgeHub instance.
# only used in some SDKs if friend_module_connect_from_environment == False
#
# Other SDKs may need this added to the "Trusted Root Certificate Authorities"
# portion of the trust store if you're using connect_from_environment == False.
# (You know who you are)
#
# retrived from edge-e2e/scripts/get_ca_cert.sh
ca_certificate = None
if "IOTHUB_E2E_EDGEHUB_CA_CERT" in os.environ:
    ca_certificate = {
        "cert": base64.b64decode(os.environ["IOTHUB_E2E_EDGEHUB_CA_CERT"]).decode(
            "utf-8"
        )
    }

def setupExecutionEnvironment():
    """
  Finish getting details needed for executing tests. This includes information that comes from the service,
  such as connection strings, and also endpoint URIs that can't be built until after command lines are parsed
  in conftest.py (which happens after all modules are loaded)
  """
    global runtime_config
    runtime_config.iotedge= config.IotEdgeDevice()
    runtime_config.friend_module = config.IotEdgeModuleRest("friend_module")


    if conftest.language == "ppdirect":
        container_under_test = all_containers["pythonpreview"]
        runtime_config.service = config.IotHubServiceDirect("service")
        runtime_config.registry = config.IotHubRegistryDirect("registry")
        runtime_config.test_module = config.IotEdgeModuleDirect("test_module")
        runtime_config.leaf_device = config.IotEdgeLeafDeviceDirect("leaf_device")
    else:
        container_under_test = all_containers[conftest.language]
        runtime_config.service = config.IotHubServiceRest("service")
        runtime_config.registry = config.IotHubRegistryRest("registry")
        runtime_config.test_module = config.IotEdgeModuleRest("test_module")
        runtime_config.leaf_device = config.IotEdgeLeafDeviceRest("leaf_device")

    hub = edgehub_factory.useExistingHubInstance(service_connection_string, edge_device_id)

    runtime_config.iotedge.device_id = edge_device_id

    runtime_config.test_module.device_id = edge_device_id
    runtime_config.test_module.module_id = container_under_test.module_id
    runtime_config.test_module.connection_string = container_under_test.connection_string
    if conftest.local:
        runtime_config.test_module.rest_uri = "http://localhost:" + str(container_under_test.local_port)
    else:
        runtime_config.test_module.rest_uri = (
            "http://" + host_for_rest_uri + ":" + str(container_under_test.host_port)
        )
    runtime_config.test_module.transport = conftest.transport
    runtime_config.test_module.language = conftest.language

    runtime_config.friend_module.device_id = edge_device_id
    runtime_config.friend_module.module_id = all_containers["friend"].module_id
    runtime_config.friend_module.connection_string = all_containers["friend"].connection_string
    runtime_config.friend_module.rest_uri = (
        "http://" + host_for_rest_uri + ":" + str(all_containers["friend"].host_port)
    )

    runtime_config.leaf_device.module_id = hub.leaf_device_id
    runtime_config.leaf_device.connection_string = hub.leaf_device_connection_string
    if container_under_test.deviceImpl:
        runtime_config.leaf_device.rest_uri = config.test_module.rest_uri
    else
        runtime_config.leaf_device.rest_uri = config.friend_module.rest_uri

    if not runtime_config.test_module.connection_string:
        raise Exception(
            "test module has not been deployed.  You need to deploy your langauge module (even if you're testing locally)"
        )
    if not runtime_config.friend_module.connection_string:
        raise Exception("friend module has not been deployed.")
    if not runtime_config.leaf_device.connection_string:
        raise Exception(
            "Leaf device does not appear to have an iothub identity.  You may need to re-run create-new-edgehub-device.sh"
        )

    if container_under_test.registryImpl:
        runtime_config.registry.rest_uri = config.test_module.rest_uri
    else
        runtime_config.registry.rest_uri = config.friend_module.rest_uri

    if container_under_test.serviceImpl:
        runtime_config.service.rest_uri = config.test_module.rest_uri
    else
        runtime_config.service.rest_uri = config.friend_module.rest_uri

    if not conftest.direct_to_iothub:
        # route all of our devices through edgeHub if necessary
        gatewayHostSuffix = ";GatewayHostName=" + gateway_host_name
        runtime_config.test_module.connection_string += gatewayHostSuffix
        runtime_config.friend_module.connection_string += gatewayHostSuffix
        runtime_config.leaf_device.connection_string += gatewayHostSuffix
    else:
        # no certificate if we're going straight to iothub
        ca_certificate = {}
        runtime_config.test_module.connection_type = config.CONNECTION_STRING
        runtime_config.friend_module.connection_type = config.CONNECTION_STRING


    def friendly_uri(uri):
        if uri == runtime_config.test_module.rest_uri:
            return uri + " (module under test)"
        elif uri == runtime_config.friend_module.rest_uri:
            return uri + " (friend container)"
        else:
            return uri + " (some other container)"


    if language == "ppdirect":
        adapters.add_direct_python_sdk_adapter(
            name="TestModuleClient", api_surface="ModuleApi"
        )
        adapters.add_direct_azure_rest_adapter(
            name="RegistryClient", api_surface="RegistryApi"
        )
        adapters.add_direct_azure_rest_adapter(
            name="ServiceClient", api_surface="ServiceApi"
        )
    else:
        adapters.add_rest_adapter(
            name="TestModuleClient", api_surface="ModuleApi", uri=test_module_uri
        )
        adapters.add_rest_adapter(
            name="RegistryClient", api_surface="RegistryApi", uri=registry_uri
        )
        adapters.add_rest_adapter(
            name="ServiceClient", api_surface="ServiceApi", uri=service_client_uri
        )

    adapters.add_rest_adapter(
        name="FriendModuleClient", api_surface="ModuleApi", uri=friend_module_uri
    )
    adapters.add_rest_adapter(
        name="LeafDeviceClient", api_surface="DeviceApi", uri=leaf_device_uri
    )
    adapters.add_direct_azure_rest_adapter(
        name="EventHubClient", api_surface="EventHubApi"
    )

    print("Run Parameters:")
    print("  language:             {}".format(language))
    print("  module_id:            {}".format(module_id))
    print("  friend_module_id:     {}".format(friend_module_id))
    print("  leaf_device_id:       {}".format(leaf_device_id))
    print("  using environment:    {}".format(test_module_connect_from_environment))
    print("  test transport:       {}".format(test_module_transport))
    print("  friend transport:     {}".format(friend_module_transport))
    print(
        "  destination:          {}".format(
            "iothub" if conftest.direct_to_iothub else "edgehub"
        )
    )
