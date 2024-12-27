This configuration stores everything related to the bot itself.

### Bot top level
| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| $schema | string (uri) |  | Which JSONSchema the file follows. |
| no-reply | object |  | Configuration for the 'no-reply' feature. |

#### `no-reply` (Optional)

| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| enabled | boolean | Yes | Whether the 'no-reply' feature is enabled. |
| message | string |  | The message to send back when the bot receives a message. If empty or not set, a default message in English will be sent. |
