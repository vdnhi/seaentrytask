import enum as enum


class HttpStatus(enum.Enum):
	Ok = 200
	BadRequest = 400
	Unauthorized = 401
	NotFound = 404
	InternalServerError = 500
