# amplitude-python-sdk

**Unofficial** SDK for the Amplitude HTTP API, providing a user-friendly interface through Pydantic models.

See [the Amplitude docs](https://developers.amplitude.com/docs) for more information on the various API methods and their parameters.

**WARNING: This library is in very early development, and APIs are not guaranteed to be stable. Please bear that in mind when using this library.**

# Installation

```
pip install amplitude-python-sdk
```

## Dependencies

* [pydantic](https://github.com/samuelcolvin/pydantic) is used to create cleaner and more readable data models within this library.
* [requests](https://github.com/psf/requests) is used to handle all HTTP interactions with the Amplitude API.

# Usage

## Methods supported

Currently, only the [Identify API](https://developers.amplitude.com/docs/identify-api) and the [HTTP API V2](https://developers.amplitude.com/docs/http-api-v2) are supported. Support for other API methods coming soon!

## Identify API Example

```python
import logging

from amplitude_python_sdk.common.exceptions import AmplitudeAPIException
from amplitude_python_sdk.v1.client import AmplitudeV1APIClient
from amplitude_python_sdk.v1.models.identify import Identification, UserProperties

client = AmplitudeV1APIClient(api_key='<YOUR API KEY HERE>')
try:
    resp = client.identify([Identification(user_id='example', user_properties=UserProperties()])
except AmplitudeAPIException:
    logging.exception('Failed to send identify request to Amplitude')
```

## Event API Client Example

```python
import logging

from amplitude_python_sdk.common.exceptions import AmplitudeAPIException
from amplitude_python_sdk.v2.clients.event_client import EventAPIClient
from amplitude_python_sdk.v2.models.event import Event
from amplitude_python_sdk.v2.models.event.options import EventAPIOptions

client = EventAPIClient(api_key='<YOUR API KEY HERE>')

try:
    events = [
        Event(
            user_id='example',
            event_type='Clicked on Foo',
            event_properties={
                'foo_id': 'bar',
                'click_position': 5,
            }
        )
    ]
    client.upload(
        events=events,
        options=EventAPIOptions(min_id_length=1),
    )
except AmplitudeAPIException:
    logging.exception('Failed to log event to Amplitude')
```

## Batch Event Upload API Example

Exactly the same as the Event V2 API example, just substitute `client.batch_upload` for `client.upload`.
