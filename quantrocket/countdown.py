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
Functions for working with the countdown (crontab) service.

Functions
---------
get_timezone
    Return the service timezone

set_timezone
    Set the countdown service timezone

Notes
-----
Usage Guide:

* Scheduling: https://qrok.it/dl/qr/schedule
"""
from quantrocket.houston import houston
from quantrocket._cli.utils.output import json_to_cli

def _load_or_show_crontab(filename=None, *args, **kwargs):
    if filename:
        return json_to_cli(load_crontab, filename, *args, **kwargs)
    else:
        exit_code = 0
        return get_crontab(*args, **kwargs), exit_code

__all__ = [
    "get_timezone",
    "set_timezone",
]

def get_crontab(
    service: str = None
    ) -> str:
    """
    Return the current crontab.

    Parameters
    ----------
    service : str, optional
        the name of the countdown service (default 'countdown')

    Returns
    -------
    str
        string representation of crontab
    """
    service = service or "countdown"
    response = houston.get("/{0}/crontab".format(service))
    houston.raise_for_status_with_json(response)
    return response.text

def load_crontab(
    filename: str,
    service: str = None
    ) -> dict[str, str]:
    """
    Upload a new crontab.

    Parameters
    ----------
    filename : str, required
        the crontab file to upload to the countdown service

    service : str, optional
        the name of the countdown service (default 'countdown')

    Returns
    -------
    dict
        status message
    """
    service = service or "countdown"
    with open(filename) as file:
        response = houston.put("/{0}/crontab".format(service), data=file.read())
    houston.raise_for_status_with_json(response)
    return response.json()

def get_timezone(
    service: str = None
    ) -> dict[str, str]:
    """
    Return the countdown service timezone.

    Parameters
    ----------
    service : str, optional
        the name of the countdown service (default 'countdown')

    Returns
    -------
    dict
        dict with key timezone

    Notes
    -----
    Usage Guide:

    * Scheduling: https://qrok.it/dl/qr/schedule
    """
    service = service or "countdown"
    response = houston.get("/{0}/timezone".format(service))
    houston.raise_for_status_with_json(response)
    return response.json()

def set_timezone(
    tz: str,
    service: str = None
    ) -> dict[str, str]:
    """
    Set the countdown service timezone.

    Parameters
    ----------
    tz : str, required
        the timezone to set (pass a partial timezone string such as 'newyork'
        or 'europe' to see close matches, or pass '?' to see all choices)

    service : str, optional
        the name of the countdown service (default 'countdown')

    Returns
    -------
    dict
        status message

    Notes
    -----
    Usage Guide:

    * Scheduling: https://qrok.it/dl/qr/schedule

    Examples
    --------
    Set the countdown timezone to America/New_York:

    >>> set_timezone("America/New_York")
    """
    service = service or "countdown"
    params = {"tz": tz}
    response = houston.put("/{0}/timezone".format(service), params=params)
    houston.raise_for_status_with_json(response)
    return response.json()

def _cli_get_or_set_timezone(tz=None, *args, **kwargs):
    if tz:
        return json_to_cli(set_timezone, tz, *args, **kwargs)
    else:
        return json_to_cli(get_timezone, *args, **kwargs)
