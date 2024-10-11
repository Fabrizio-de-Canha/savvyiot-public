from endpoints.authenticate import get_token_header, get_admin_header
import models
from deps import get_session

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session, Query
import models.messages
from schemas.devices.device import DeviceBase, EditDeviceBase
from schemas.messages.message import MessageQuery, MessagesResponse

router = APIRouter()


@router.get("")
def read_devices(
    user: dict = Depends(get_token_header),
    db: Session = Depends(get_session),
) -> list[DeviceBase]:
    """
    Retrieve devices.
    """

    results = db.query(models.Device).all()
    devices: list[DeviceBase] = [DeviceBase.model_validate(device) for device in results]
    return devices

@router.get("/{id}")
def read_single_device(
    id: str,
    user: dict = Depends(get_token_header),
    db: Session = Depends(get_session),
) -> DeviceBase:
    """
    Retrieve devices.
    """

    query_object: Query = db.query(models.Device).filter(models.Device.mac_id == id)
    device = query_object.first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.post("")
def create_devices(
    user: str = Depends(get_admin_header),
    db: Session = Depends(get_session),
) -> list[DeviceBase]:
    """
    Add Devices.
    """

    results = db.query(models.Device).all()
    devices: list[DeviceBase] = [DeviceBase.model_validate(device) for device in results]
    return devices

@router.post("/deviceData")
def get_device_data(
    input: MessageQuery,
    user: str = Depends(get_token_header),
    db: Session = Depends(get_session),
) -> list[MessagesResponse]:
    """
    retrieve data from device
    """

    tenant = user["tenant"]

    results: list[MessagesResponse]= (
        db.query(models.Message)
        .filter(
            models.Message.device_mac == input.device_mac,
            models.Message.tenant == tenant,
            models.Message.value_type == input.value_type
            )
        .order_by(models.Message.message_timestamp.desc())
        .limit(input.limit)
        .all()
    )
    
    return results

@router.put("")
def edit_device(
    input: EditDeviceBase,
    user: str = Depends(get_admin_header),
    db: Session = Depends(get_session),
) -> DeviceBase:
    """
    Edit devices.
    """

    device = db.query(models.Device).filter(models.Device.mac_id == input.mac_id).first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if(input.name):
        device.name = input.name
    if(input.device_type):
        device.device_type = input.device_type
    if(input.active):
        device.active = input.active

    db.commit()
    return device

@router.delete(
        "/{id}", 
        status_code=204
)
def delete_devices(
    id: str,
    user: str = Depends(get_admin_header),
    db: Session = Depends(get_session),
):
    """
    Retrieve users.
    """

    query_object: Query = db.query(models.Device).filter(models.Device.mac_id == id)
    device = query_object.first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    query_object.delete()
    db.commit()
    return