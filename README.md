# Car Rental API (WIP)

API service for a car rental platform where users can rent out their cars

### Requirements

Quiver is a vehicle rental platform that wants to make it easy for users to rent out their vehicles. The goal is to build a API service for that.

- Users can create an acocunt that serves for both Vehicle owner or renter

#### as Vehicle owner

- User can add their vehicles to rent out with important information like; name, model, type, pricing, description, location, color, engine information, photos etc
- user can update vehicle information
- User can see list of vehicles they have added
- User can filter vehicles by status i.e active, reserved, available
- User can see rent history of a vehicle. e.g when a vehicle was reserved, when it became active, when it became available, when it was canceled
- user can cancel reservation

#### as Renter

- User can find vehicles they want to rent by running a quick search or seeing catalogs of vehicles
- User can reserve desired vehicle by submitting rent and return date. User cannot reserve a vehicle that has been reserved at a set time
- user can cancel reservation
- User can see rental history

### API Endpoints

#### Auth

- [x] Create account /auth/register [POST]
- [x] Login /auth/login [POST]
- [x] Current user /auth/me [GET]
- [x] Forgot password /auth/forgot-password/reset-link [POST]
- [x] Reset password /auth/forgot-password/validate [POST]
- [x] Reset password /auth/forgot-password/update [POST]

#### User

- [x] Change password /user/change-password [POST]-[HOST,GUEST]
- [x] get user's profile /user/profile/:id [GET]-[HOST/GUEST]
- [x] get current user's profile /user/me/profile [GET]-[HOST/GUEST]
- [x] get current user's vehicles /user/me/vehicles [GET]-[HOST/GUEST]
- [x] update profile /user/profile [PUT]-[HOST/GUEST]
- [ ] rental history /user/rentals [GET]-[GUEST]

#### Vehicles

- [x] create /vehicles [POST]-[HOST]
- [x] list /vehicles?status=[available / active / unavailable] [GET]
- [ ] upload vehicle photos /vehicles/:id/upload [POST][HOST]
- [x] vehicle detail /vehicles/:id [GET]
- [x] update vehicle detail /vehicles/:id [PUT]-[HOST]
- [x] delete /vehicles/:id [DELETE]-[HOST]
- [x] vehicle reservations /vehicles/:id/bookings [GET]

#### Bookings

- [x] make a booking /bookings [POST]-[GUEST]
- [x] cancel booking /bookings/:id/cancel [PUT]-[HOST,GUEST]
- [ ] update booking /bookings/:id [PUT]
- [ ] booking detail /bookings/:id [GET]
- [x] confirm a booking /bookings/:id/confirm [PUT][HOST]
      booking status = canceled, confirmed

### Technology used

- Python
- FastAPI
- PostgreSQL
- JWT for authentication
- Brevo for sending mail
- BetterStack for log monitoring

### Getting started

```sh
# install dependencies
pip install -r requirements.txt

# run app
uvicorn app.main:app --reload
```

## Todo

- [ ] refresh token
- [x] move from id to uuid
- [ ] email template
- [x] change user_crud.handle_get_current_user to jwt_utils.verify_token_access(token)
- [x] find a way to use middleware to implment token verification
