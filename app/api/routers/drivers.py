# app/api/routers/drivers.py
# Imports
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.db_raw import *
from app.schemas.drivers import *
from app.core.security import verify_token

# Defines the Router
drivers_router = APIRouter(
prefix="/drivers",
tags=["Drivers"])

security = HTTPBearer()

"""GET"""

# Get Driver's Details by ID
@drivers_router.get("/{driver_id}", response_model=DriverOut, status_code=status.HTTP_200_OK)
async def get_driver_details(driver_id: int):
    # Perform the Operation
    row = fetch_driver_details(driver_id)

    # Validation
    if row is None:
        raise HTTPException(status_code=404, detail="Driver ID Not Found")
    
    # Driver Details
    driver = {
        "driver_id": row[0],
        "licence_number": row[2],
        "state_issue": row[3],
        "last_name": row[4],
        "first_name": row[5],
        "dob": row[6],
        "height_inches": row[7],
        "weight_pounds": row[8],
        "eyes_colour": row[9]
    }

    # Return the Results
    return driver

# Get All Driver's Details
@drivers_router.get("", status_code=status.HTTP_200_OK)
async def get_all_drivers():
    # Perform the Operation
    row = fetch_all_drivers()

    # Validation
    if row is None:
        raise HTTPException(status_code=404, detail="Driver ID Not Found")
    
    # All Drivers
    drivers = {
        "driver_id": row[0],
        "state_issue": row[1],
        "last_name": row[2],
        "first_name": row[3]
    }

    # Return
    return drivers

"""POST"""

# Insert a New Driver
@drivers_router.post("", response_model=DriverOut, status_code=status.HTTP_201_CREATED)
async def insert_new_driver(
    payload: DriverCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_token(credentials.credentials)

    driver_id = create_driver(
        driver=payload,
        address=payload.address
    )

    return DriverOut(
        driver_id=driver_id,
        licence_number=payload.licence_number,
        state_issue=payload.state_issue,
        last_name=payload.last_name,
        first_name=payload.first_name,
        dob=payload.dob,
        height_inches=payload.height_inches,
        weight_pounds=payload.weight_pounds,
        eyes_colour=payload.eyes_colour
    )

"""DELETE"""

# Deletes the Driver by ID
@drivers_router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_driver(
    driver_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_token(credentials.credentials)

    deleted = delete_driver(driver_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return {"message": f"Driver {driver_id} deleted successfully"}

"""PUT"""

# Updates Driver's Details by ID
@drivers_router.put("/{driver_id}", response_model=DriverOut, status_code=status.HTTP_201_CREATED)
async def update_existing_driver(
    driver_id: int,
    payload: DriverCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    verify_token(credentials.credentials)

    row = update_driver(driver_id, payload)

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    return {
        "driver_id": row[0],
        "licence_number": row[1],
        "state_issue": row[2],
        "last_name": row[3],
        "first_name": row[4],
        "dob": row[5],
        "height_inches": row[6],
        "weight_pounds": row[7],
        "eyes_colour": row[8]
    }
