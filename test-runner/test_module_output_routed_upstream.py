#!/usr/bin/env python

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import pytest
import connections
import random
import test_utilities
import environment
from adapters import print_message as log_message

output_name = "telemetry"


@pytest.mark.callsSendOutputEvent
@pytest.mark.testgroup_edgehub_module_client
def test_module_output_routed_upstream():

    module_client = connections.connect_test_module_client()
    eventhub_client = connections.connect_eventhub_client()

    sent_message = test_utilities.random_string_in_json()
    module_client.send_output_event(output_name, sent_message)

    received_message = eventhub_client.wait_for_next_event(
        environment.edge_device_id,
        test_utilities.default_eventhub_timeout,
        expected=sent_message,
    )
    if not received_message:
        log_message("Message not received")
        assert False

    module_client.disconnect()
    eventhub_client.disconnect()
