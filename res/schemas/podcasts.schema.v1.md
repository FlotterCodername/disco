| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| $schema | string (uri) |  | Which JSONSchema the file follows. |
| podcast | array[object] |  |  |

## podcast (Array) (Optional)

Array items:

| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| forward_channel | string | Yes |  |
| forward_guild | string | Yes |  |
| name | string | Yes |  |
| url_artwork | string (uri) |  |  |
| url_feed | string (uri) | Yes |  |
