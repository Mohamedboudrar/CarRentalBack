from fastapi import APIRouter

router = APIRouter()

@router.post('')
async def make_booking():
  return {"message": "Booking successful"}

@router.put('/{booking_id}/cancel')
async def cancel_booking():
  return {"message": "Booking canceled"}

@router.put('/{booking_id}')
async def update_booking_detail():
  return {"message": "Booking updated"}

@router.get('/{booking_id}')
async def get_booking_detail():
  return {}

@router.put('/{booking_id}/confirm')
async def confirm_booking():
  return {"message": "Booking confirmed"}