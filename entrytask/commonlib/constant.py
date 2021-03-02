import enum as enum

LOGIN_CACHE_TIMEOUT = 60
SESSION_TIMEOUT = 3600
TOKEN_LENGTH = 64
RANDOM_KEY_LENGTH = 32


class HttpStatus(enum.Enum):
	Ok = 200
	BadRequest = 400
	Unauthorized = 401
	NotFound = 404
	InternalServerError = 500
