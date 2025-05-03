import os
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, HTTPException
from datetime import datetime, timedelta, timezone
import httpx
from typing import Optional, List, Dict, Any
import asyncio
import re


load_dotenv()
router = APIRouter()
app = FastAPI()

VERSION = "0.2.0"
BOX_IDS = os.environ['senseBoxIds']
BOX_IDS = BOX_IDS.split(",") if BOX_IDS else []
SENSEBOX_API = "https://api.opensensemap.org/boxes"

# Validate box ID format (12 or 24 character hex string)
BOX_ID_PATTERN = re.compile(r'^[0-9a-f]{12}(?:[0-9a-f]{12})?$')

@router.get("/version")
def get_version():
    """Returns the API version."""
    return {"version": VERSION}

async def get_temperature_sensor_id(client: httpx.AsyncClient, box_id: str) -> Optional[str]:
    """Get the ID of the temperature sensor for a given box."""
    # Validate box ID format
    if not box_id or not isinstance(box_id, str) or not BOX_ID_PATTERN.match(box_id.lower()):
        return None

    url = f"{SENSEBOX_API}/{box_id}"
    try:
        response = await client.get(url)
        response.raise_for_status()
        
        # Handle both sync and async json methods
        if asyncio.iscoroutinefunction(response.json):
            box_data = await response.json()
        else:
            box_data = response.json()
        
        for sensor in box_data.get("sensors", []):
            if "temperatur" in sensor.get("title", "").lower():
                return sensor.get("_id")
                
        # Box exists but has no temperature sensor
        return None
        
    except (httpx.HTTPStatusError, httpx.HTTPError):
        return None

@router.get("/temperature")
async def get_temperature():
    """Get average temperature data from SenseBoxes."""
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    all_recent_temps: List[float] = []
    errors: List[str] = []
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        
        # Create tasks for all box IDs
        for box_id in BOX_IDS:
            tasks.append(process_box(client, box_id, one_hour_ago, all_recent_temps, errors))
            
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
        
        average_temperature = sum(all_recent_temps) / len(all_recent_temps)
            # Assign status based on temperature range
        if average_temperature < 10:
            status = "Too Cold"
        elif 10 <= average_temperature <= 36:
            status = "Good"
        else:
            status = "Too Hot"

        if not all_recent_temps:
            if errors:
                raise HTTPException(
                    status_code=503,
                    detail={
                        "error": "Failed to retrieve temperature data",
                        "details": errors
                    }
                )
            raise HTTPException(
                status_code=503,
                detail={"error": "No recent temperature data available."}
            )
            

        return {
            "average_temperature": average_temperature,
            "status": status,
            "unit": "°C",
            "measurements_count": len(all_recent_temps),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

async def process_box(
    client: httpx.AsyncClient,
    box_id: str,
    one_hour_ago: datetime,
    all_recent_temps: List[float],
    errors: List[str]
):
    """Process a single box to extract temperature data."""
    try:
        sensor_id = await get_temperature_sensor_id(client, box_id)
        if not sensor_id:
            return

        url = f"{SENSEBOX_API}/{box_id}/data/{sensor_id}"
        try:
            response = await client.get(url)
            response.raise_for_status()
            
            # Handle both sync and async json methods
            if asyncio.iscoroutinefunction(response.json):
                measurements = await response.json()
            else:
                measurements = response.json()

            if measurements and isinstance(measurements, list) and len(measurements) > 0:
                for measurement in measurements[:5]:  # Process only the 5 most recent measurements
                    try:
                        timestamp = datetime.fromisoformat(
                            measurement["createdAt"].replace("Z", "+00:00")
                        )
                        if timestamp >= one_hour_ago:
                            all_recent_temps.append(float(measurement["value"]))
                    except (ValueError, KeyError) as e:
                        errors.append(f"Invalid measurement format for box {box_id}: {str(e)}")
        except httpx.HTTPError as e:
            errors.append(f"Error fetching measurements for box {box_id}: {str(e)}")
    except HTTPException as e:
        errors.append(str(e.detail))
    except (ValueError, KeyError, TypeError) as e:
        errors.append(f"Data validation error for box {box_id}: {str(e)}")