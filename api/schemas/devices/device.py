from typing import List, Optional, Dict
import uuid
from datetime import datetime

from pydantic import Field

from schemas.base import BaseModel

class DeviceBase(BaseModel):
    mac_id: str
    active: Optional[bool]
    name:  Optional[str]
    created_on: Optional[datetime]
    last_reported: Optional[datetime]
    last_booted: Optional[datetime]
    last_firmware_upgrade: Optional[datetime]
    device_type:  Optional[str]
    rssi: Optional[int]
    firmware_version: Optional[float]

class EditDeviceBase(BaseModel):
    mac_id: str
    active: Optional[bool] = Field(None, description="Device status")
    name:  Optional[str] = Field(None, description="Device display name")
    device_type:  Optional[str] = Field(None, description="Device type")