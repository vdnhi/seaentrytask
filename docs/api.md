### Event API
```
Path: /event
GET: Get events by condition (default get first 10 latest events).
Query parameters: 
{
    “from": "integer",
    "to": "integer",      
    "channels": "string”,
    "location”: "string",
    "base": "integer",
    "offset": "integer",
    “user_id”: “integer”,
    “token”: “string”
}

Response:
    200: [{
        "id": "integer",
        "channels": array of "string",
        "title": "string"
        ”content": "string"
        "image_urls": array of "string"
        "create_uid":  "integer",
        "location": "string"
        "start_date": "integer",
        "end_date": "integer",
        "updated_at": "integer",
        “count_like”: “integer”,
        “count_participation”: “integer”,
        “has_participated: “boolean”,
        “has_liked”: “boolean”
    }]
    400: “Invalid input”
    500: Internal server error

POST: Create new event (requires authentication)
	Request body: {
       “channels": array of "string",
       "title": "string",
       "content": "string",
       "create_uid": "integer",
       "location": "string",
       "start_date": "integer",
       "end_date": "integer",
       “token”: “string”,
 	  “role”: “number”
     }
	
	Response:
	200: {
	  “event_id”: “integer”
},
400: Invalid input
401: Unauthorized
500: Internal server error
```

### Single Event API
```
Path: /event/{event_id}
  Path parameters: 
	“event_id”: “integer”
GET: Get single event
	Query parameters: {
	  “token”: “string”
	}
Response:
200: {
    "id": "integer",
    "channels": array of "string",
    "title": "string"
 ”content": "string"
    "image_urls": array of "string"
    "create_uid": "integer",
    "location": "string"
    "start_date": "integer",
    "end_date": "integer",
    “create_time”: “integer”,
    "updated_time": "integer",
    “count_like”: “integer”,
    “count_participation”: “integer”,
    “has_liked”: “boolean”,
    “has_participated”: “boolean”
},
404: Event with id = event_id not found
	500: Internal server error

PATCH: Update an event (requires authentication)
Request body: 
{
    “channels": array of "string"
    "title": "string"
    "content": "string"
    "create_uid": "integer",
    "location": "string"
    "start_date": "integer",
    "end_date": "integer",
    “token”: “string”,
    “role”: “number”
}

Response:
200: {
    “event_id”: “integer”
},
400: Invalid input
401: Unauthorized
500: Internal server error

DELETE: Delete an event (requires authentication)
Query params:
  “token”: “string”,
Response:
200: Delete successful
401: Unauthorized
404: Event with event_id not found
500: Internal server error
```

### Upload Image
```
Path: /event/{event_id}/uploadImage
POST: Upload images for event with id = event_id (requires authentication)
Path parameters: 
  “event_id”: “integer”

Request body: multipart/form-data
  “images”: array of “string/binary”

Response:
200: Upload images successfully
401: Unauthorized
404: Event not found
500: Internal server error
```

### Like API
```
Path: /event/{event_id}/like
Path parameters:
  “event_id”: “integer”,
 

GET: Get likes of an event
Query parameters:
  “base”: “integer”,
  “offset”: “integer”

Response:
200: [
  “user_id”: “integer”,
  “username”: “string”
]
404: Event not found
500: Internal server error

POST: Like operation for an event (requires authentication)

Request body: {
  “token: “string”
}

Response:
200: Operation successful
401: Unauthorized
404: Event not found
500: Internal server error

DELETE: Remove like of an event (requires authentication)
	Query params:
  	  “token”: “string”
	Response:
	200: Operation successful
	401: Unauthorized
	404: Event not found
	500: Internal server error
```

### Participation API
```
Path: /event/{event_id}/participation
	Path parameters:
	  “event_id”: “integer”
GET: Get participations of an event
Response: 
Query parameters:
  “base”: “integer”,
  “offset”: “integer”
200: [
  “user_id”: “integer”,
  “username”: “string”
]
404: Event not found
500: Internal server error

POST: Update participant for an event (requires authentication)

Request body: {
  “token”: “string”
}

Response: 
200: Operation successful
401: Unauthorized
404: Event not found
500: Internal server error

DELETE: Remove user participation of an event (requires authentication)
	Query params:
  	  “token”: “string”
	Response:
	200: Operation successful
	401: Unauthorized
	404: Event not found
	500: Internal server error
```

### Comment API
```
Path: /event/{event_id}/comment
	Path parameters:
	  “event_id”: “integer”
GET: Get comments of an event
Response: 
Query params:
  “base”: “integer”,
  “offset”: “integer”

200: [
  {
    “username”: “string”,
    “content”: “string”,
	“create_time”: “string”
  }
]
404: Event not found
500: Internal server error

POST: Add new comment to an event (requires authentication)

Request body: {
  “user_id”: “integer”,
  “content: “string”
}

Response: 
200: Operation successful
401: Unauthorized
404: Event not found
500: Internal server error
```

### Channel (category) API
```
Path: /event/channel
GET: Get channels information
Query params:
  “channels
Response:
200: [
  {
    “id”: “integer”,
    “name”: “string”
  }
]
	500: Internal server error
```

### Authorization API
```
Path: /user/register
POST: Register new user:
Request body: {
  	  "username": "string",
  "password": "string",
  	  “fullname”: “string”,
  	  “email”: “string”
    }

Response:
200: {
  	  “user_id”: “integer”,
  	  “token”: “token”
},
400: Invalid input
500: Internal server error
```

```
Path: /user/prelogin
POST: Get random key if user existed
	Request body: {
  “username”: “string”
}

Response: 
200: {
  “key”: “string”
}
404: User not found
500: Internal server error
```

```
Path: /user/login
POST: Login
Request body: {
       “username”: “string”,
       “password”: “string”, // this password is encrypted with random key get from prelogin step
}
	
Response: 
200: {
    “token”: “string”,
    “user_id”: “integer”
    }
400: Invalid input
404: Invalid password
500: Internal server error
```