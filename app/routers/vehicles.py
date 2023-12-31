from fastapi import APIRouter

router = APIRouter()

@router.post('')
async def add_vehicle():
  return {"message": "vehicle added successfull"}

@router.get('')
async def list_vehicles():
  return []

@router.get('/{vehicle_id}')
async def vehicle_detail():
  return {"name": "Tesla Model S"}

@router.put('/{vehicle_id}')
async def update_vehicle():
  return {"message": "Vehicle updated"}

@router.delete('/{vehicle_id}')
async def delete_vehicle():
  return {"message": "vehicle deleted"}

@router.get('/{vehicle_id}/timeline')
async def vehicle_timeline():
  return []

@router.get('/{vehicle_id}/reservations')
async def vehicle_reservations():
  return []

@router.put('/{vehicle_id}/status')
async def update_vehicle_status():
  return []