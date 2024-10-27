| Property | Type            | Required | Description |
|----------|-----------------|----------|-------------|
| $schema  | string (uri)    | No       |             |
| podcast  | array of object | No       |             |

## podcast (Array, Optional)

Array items:

| Property        | Type         | Required | Description |
|-----------------|--------------|----------|-------------|
| forward_channel | string       | Yes      |             |
| forward_guild   | string       | Yes      |             |
| name            | string       | Yes      |             |
| url_artwork     | string (uri) | No       |             |
| url_feed        | string (uri) | Yes      |             |
