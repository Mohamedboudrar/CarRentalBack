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
- [ ] Forgot password /auth/forgot-password [POST]
- [ ] Reset password /auth/reset-password [POST]

#### User

- [x] Change password /user/change-password [POST]-[HOST,GUEST]
- [x] get user's profile /user/profile/:id [GET]-[HOST/GUEST]
- [x] get current user's profile /user/profile/me [GET]-[HOST/GUEST]
- [x] create profile /user/profile [POST]-[HOST/GUEST]
- [x] update profile /user/profile [PUT]-[HOST/GUEST]
- [ ] rental history /user/rentals [GET]-[HOST/GUEST]

#### Vehicles

- [ ] create /vehicles [POST]-[HOST]
- [ ] list /vehicles?status=[available / active / unavailable] [GET]-[HOST]
- [ ] vehicle detail /vehicles/:id [GET]
- [ ] update vehicle detail /vehicles/:id [PUT]-[HOST]
- [ ] delete /vehicles/:id [DELETE]-[HOST]

- [ ] vehicle timeline /vehicles/:id/timeline [GET]-[HOST]
- [ ] vehicle reservations /vehicles/:id/reservations [GET]
- [ ] change vehicle status /vehicles/:id/status [PUT] {"status": "available / active / unavailable" }[HOST]

#### Bookings

- [ ] make a booking /bookings [POST]-[GUEST]
- [ ] cancel booking /bookings/:id/cancel [PUT]-[HOST,GUEST]
- [ ] update booking /bookings/:id [PUT]
- [ ] booking detail /bookings/:id [GET]
- [ ] confirm a booking /bookings/:id/confirm [PUT][HOST]
      booking status = canceled, confirmed
