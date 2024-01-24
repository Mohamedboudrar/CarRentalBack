# Car Rental API

API service for a car rental platform where users can rent out their vehicles as well as rent vehicles of other users. Inspired by the AirBnB platform.

### Technology used

- Python programming language
- FastAPI - Really fast python library for building APIs
- PostgreSQL database
- JWT for authentication
- Brevo for sending mail because it is free and easy to setup
- BetterStack for log monitoring <3

### Requirements

- Users can create an account that allows them serve as host and renter depending on context

##### As Host

- User can add their vehicles to rent out with important information like; name, model, type, pricing, description, location, color, engine information, photos etc
- user can update vehicle information
- User can see list of vehicles they own and can filter by status i.e active, reserved, available(see detail here)
- User can see history of a vehicle. e.g when a vehicle was added, booked, when it became active, when it became available, when it was canceled etc
- user can confirm or cancel reservation

##### As Renter

- User can find vehicles they want to rent by running a quick search or seeing catalogs of vehicles. This can be sorted by location, vehicle name, model, color, price etc
- User can book a vehicle by submitting rent and return date. User cannot reserve a vehicle that has been reserved at a set date and time
- user can cancel booking
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
- [x] get current user's vehicles /user/me/vehicles [GET]-[HOST/GUEST]
- [x] update profile /user/profile [PUT]-[HOST/GUEST]

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

### How to Install and Run the Project

This project requires a `.env` file in the project root. Rename the `env.sample` to `.env`

```sh
# file - .env

# Database connection
DATABASE_URL =

# JWT
SECRET_KEY =
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mailing - https://www.brevo.com/
EMAIL_FROM =
BREVO_API_KEY =

# Logging - https://betterstack.com/
BETTERSTACK_LOG_SOURCE_TOKEN =
```

##### Install dependencies and run project

```sh
# install all dependencies
pdm install

# run app
pdm run start
```

## Todos

- [ ] refresh token
- [x] move from id to uuid
- [ ] email template
- [x] change user_crud.handle_get_current_user to jwt_utils.verify_access_token(token)
- [x] find a way to use middleware to implment token verification
- [ ] Containerize using Docker
- [ ] Reviews and rating system
