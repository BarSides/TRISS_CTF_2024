## Getting started
```
$ docker compose up -d
```

The database is automatically initialized and can viewed/modified at `http://localhost:8081/`.

## The Challenge

The challenge is to gain API access as the admin user.  Unfortunately, you have lost your API key, and you don't have
admin user permission anyway.

Username: trissandra

Corp ID: 1337b4da55

To authenticate, you must set the X-Api-Key header:

`X-Api-Key: {corp_id}:{api_key}`

The following endpoints are available in varying levels of completion:

| Method | Path               | Payload                                             |
|--------|--------------------|-----------------------------------------------------|
| GET    | /users             |                                                     |
| GET    | /users/:corp_id    |                                                     |
| POST   |  /apikeys/:corp_id | <TODO: get intern to add json payload example here> |

## Hints

- This challenge may require more than one exploit.
- Look at all inputs and responses, including error messages.

## Flag

BarSides{8a6e053f-ac6e-492b-b83b-72adf192482f}
