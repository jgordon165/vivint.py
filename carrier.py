#!/usr/bin/env python3
"""
A device class that represents a Carrier object for making calls to a localized Carrier service

Please refer to https://github.com/acd/infinitive for information regarding setup of the infinitive api 
using serial device to connect with Carrier Thermostat/Furnace
"""

import os
import re
import sys
import time
import json
import base64
import urllib3
import argparse
import threading

from urllib.parse import urlencode, unquote, quote, quote_plus

# this is currently hosted locally on the same instance as your vivint.py project, but
# you could use a dns forwarder like NGRK to host these on separate instances
CARRIER_API_ENDPOINT = "http://localhost:8080"

class CarrierDevice():
    def set_carrier_state(self, current_state):
        print("setting carrier state")
        mode = "auto"
        if current_state.get("fan_mode") == "off" or current_state.get("mode") == "off":
            mode = "off"

        cool_active = "false"
        if current_state.get("mode") == "cool" and mode == "auto":
            mode = "cool"

        heat_active = "false"
        if current_state.get("mode") == "heat" and mode == "auto":
            mode = "heat"

        request_kwargs = dict(
            method="PUT",
            url="{}/api/zone/1/config".format(CARRIER_API_ENDPOINT),
            body=json.dumps({"coolSetPoint":current_state.get("cooling_setpoint"),
            "heatSetPoint":current_state.get("heating_setpoint"),
            "mode":mode}).encode("utf-8"),
            headers={
                "Content-Type":
                "application/json;charset=utf-8"
            })

        print(request_kwargs)

        resp = self._pool.request(**request_kwargs)
        
        if resp.status != 200:
            logger.error("response failed: " % (resp.status))
            logger.error("PUT-{}/api/zone/1/config".format(CARRIER_API_ENDPOINT))

    def carrier_state(self, current_state):
        request_kwargs = dict(
            method="GET",
            url="{}/api/zone/1/config".format(CARRIER_API_ENDPOINT),
            headers={"User-Agent": "vivint.py"})
        
        resp = self._pool.request(**request_kwargs)

        if resp.status != 200:
            logger.error("response failed: " % (resp.status))
            logger.error("GET-{}/api/zone/1/config".format(CARRIER_API_ENDPOINT))

        print(resp.data)

        if resp.data == None:
            return current_state

        try:
            resp_body = json.loads(resp.data.decode())
        except Exception as e:
            logger.error(e,'Houston, We have a problem')
            return current_state

        operation_mode = resp_body["mode"]
        if resp_body["mode"] == "auto":
            operation_mode = "heat-cool"

        fan_mode = "always"
        if resp_body["coolActive"] == "false" and resp_body["headActive"] == "false":
            operation_mode = "off"
            fan_mode = "off"

        return {
                "fan_mode": fan_mode,
                "humidity": resp_body["currentHumidity"],
                "temperature": resp_body["currentTemp"],
                "mode": operation_mode,
                "cooling_setpoint": resp_body["coolSetpoint"],
                "heating_setpoint": resp_body["heatSetpoint"]
            }