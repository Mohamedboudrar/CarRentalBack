from fastapi import APIRouter

router = APIRouter()

@router.put('/')
async def update_profile():
  return {"message": "Profile updated"}

@router.post('/change-password')
async def reset_password():
  return {"message": "Password change successful"}

