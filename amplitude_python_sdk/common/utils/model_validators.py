"""
This module contains Pydantic model validators that are shared between different models.
"""


def check_user_id_or_device_id(values):
    """
    At least one of device_id and user_id MUST be set according to the
    Amplitude documentation. This validator enforces that requirement.
    """
    uid, did = values.get("user_id"), values.get("device_id")
    if not (uid or did):
        raise ValueError("Must provide at least one of user_id and device_id")
    return values
