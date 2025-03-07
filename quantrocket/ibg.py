# Copyright 2017-2023 QuantRocket - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Functions for working with IB Gateway.

Functions
---------
get_credentials
    Return username and trading mode (paper/live) for IB Gateway.

set_credentials
    Set username/password and trading mode (paper/live) for IB Gateway.

list_gateway_statuses
    Query statuses of IB Gateways.

start_gateways
    Start one or more IB Gateways.

stop_gateways
    Stop one or more IB Gateways.

Notes
-----
Usage Guide:

* IB Gateway: https://qrok.it/dl/qr/ibgateway
"""

import getpass
from quantrocket.houston import houston
from quantrocket._cli.utils.output import json_to_cli
from quantrocket.utils._typing import Union, Literal

__all__ = [
    "get_credentials",
    "set_credentials",
    "list_gateway_statuses",
    "start_gateways",
    "stop_gateways",
]

def get_credentials(gateway: str) -> dict[str, str]:
    """
    Return username and trading mode (paper/live) for IB Gateway.

    Parameters
    ----------
    gateway : str, required
        name of IB Gateway service to get credentials for (for example, 'ibg1')

    Returns
    -------
    dict
        credentials

    Notes
    -----
    Usage Guide:

    * IB Gateway: https://qrok.it/dl/qr/ibgateway
    """
    statuses = list_gateway_statuses(gateways=[gateway])
    if not statuses:
        raise ValueError("no such IB Gateway: {0}".format(gateway))

    response = houston.get("/{0}/credentials".format(gateway))
    houston.raise_for_status_with_json(response)
    # It's possible to get a 204 empty response
    if not response.content:
        return {}
    return response.json()

def set_credentials(
    gateway: str,
    username: str = None,
    password: str = None,
    trading_mode: Literal["paper", "live"] = None
    ) -> dict[str, str]:
    """
    Set username/password and trading mode (paper/live) for IB Gateway.

    Can be used to set new credentials or switch between paper and live trading
    (must have previously entered live credentials). Setting new credentials will
    restart IB Gateway and takes a moment to complete.

    Credentials are encrypted at rest and never leave your deployment.

    Parameters
    ----------
    gateway : str, required
        name of IB Gateway service to set credentials for (for example, 'ibg1')

    username : str, optional
        IBKR username (optional if only modifying trading environment)

    password : str, optional
        IBKR password (if omitted and username is provided, will be prompted
        for password)

    trading_mode : str, optional
        the trading mode to use ('paper' or 'live')

    Returns
    -------
    dict
        status message

    Notes
    -----
    Usage Guide:

    * IB Gateway: https://qrok.it/dl/qr/ibgateway
    """
    statuses = list_gateway_statuses(gateways=[gateway])
    if not statuses:
        raise ValueError("no such IB Gateway: {0}".format(gateway))

    if username and not password:
        password = getpass.getpass(prompt="Enter IBKR Password: ")

    data = {}
    if username:
        data["username"] = username
    if password:
        data["password"] = password
    if trading_mode:
        data["trading_mode"] = trading_mode

    response = houston.put("/{0}/credentials".format(gateway), data=data, timeout=180)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_get_or_set_credentials(*args, **kwargs):
    if kwargs.get("username", None) or kwargs.get("password", None) or kwargs.get("trading_mode", None):
        return json_to_cli(set_credentials, *args, **kwargs)
    else:
        return json_to_cli(get_credentials, gateway=kwargs.get("gateway", None))

def list_gateway_statuses(
    status: Literal["running", "stopped", "error"] = None,
    gateways: Union[list[str], str] = None
    ) -> dict[str, str]:
    """
    Query statuses of IB Gateways.

    Parameters
    ----------
    status : str, optional
        limit to IB Gateways in this status. Possible choices: running, stopped, error

    gateways : list of str, optional
        limit to these IB Gateways

    Returns
    -------
    dict of gateway:status (if status arg not provided), or list of gateways (if status arg provided)

    Notes
    -----
    Usage Guide:

    * IB Gateway: https://qrok.it/dl/qr/ibgateway
    """
    params = {}
    if gateways:
        params["gateways"] = gateways
    if status:
        params["status"] = status

    response = houston.get("/ibgrouter/gateways", params=params)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_list_gateway_statuses(*args, **kwargs):
    return json_to_cli(list_gateway_statuses, *args, **kwargs)

def start_gateways(
    gateways: Union[list[str], str] = None,
    wait: bool = False
    ) -> dict[str, str]:
    """
    Start one or more IB Gateways.

    Parameters
    ----------
    gateways : list of str, optional
        limit to these IB Gateways

    wait: bool
        wait for the IB Gateway to start before returning (default is to start
        the gateways asynchronously)

    Returns
    -------
    dict
        status message

    Notes
    -----
    Usage Guide:

    * IB Gateway: https://qrok.it/dl/qr/ibgateway
    """
    params = {"wait": wait}
    if gateways:
        params["gateways"] = gateways

    # use a long timeout in case the user takes a long time to see the 2FA notifications
    response = houston.post("/ibgrouter/gateways", params=params, timeout=60*60*24)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_start_gateways(*args, **kwargs):
    return json_to_cli(start_gateways, *args, **kwargs)

def stop_gateways(
    gateways: Union[list[str], str] = None,
    wait: bool = False
    ) -> dict[str, str]:
    """
    Stop one or more IB Gateways.

    Parameters
    ----------
    gateways : list of str, optional
        limit to these IB Gateways

    wait: bool
        wait for the IB Gateway to stop before returning (default is to stop
        the gateways asynchronously)

    Returns
    -------
    dict
        status message

    Notes
    -----
    Usage Guide:

    * IB Gateway: https://qrok.it/dl/qr/ibgateway
    """
    params = {"wait": wait}
    if gateways:
        params["gateways"] = gateways

    response = houston.delete("/ibgrouter/gateways", params=params, timeout=60)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_stop_gateways(*args, **kwargs):
    return json_to_cli(stop_gateways, *args, **kwargs)

def load_ibg_config(filename: str) -> dict[str, str]:
    """
    Upload a new IB Gateway permissions config.

    Permission configs are only necessary when running multiple IB Gateways with
    differing market data permissions.

    Parameters
    ----------
    filename : str, required
        the config file to upload

    Returns
    -------
    dict
        status message
    """
    with open(filename) as file:
        response = houston.put("/ibgrouter/config", data=file.read())
    houston.raise_for_status_with_json(response)
    return response.json()

def get_ibg_config() -> dict[str, str]:
    """
    Return the current IB Gateway permissions config.

    Returns
    -------
    dict
        the config as a dict
    """
    response = houston.get("/ibgrouter/config")
    houston.raise_for_status_with_json(response)
    # It's possible to get a 204 empty response
    if not response.content:
        return {}
    return response.json()

def _cli_load_or_show_config(filename=None):
    if filename:
        return json_to_cli(load_ibg_config, filename)
    else:
        return json_to_cli(get_ibg_config)
