# secrets.toml

This holds all the secrets required for your bot to function.

This holds all the secrets required for your bot to function.

| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| $schema | string (uri) |  | Which JSONSchema the file follows. |
| disco | object | Yes | This holds all the actual secrets data. |

## `disco`

This holds all the actual secrets data.

| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| token | string | Yes | The 'Bot Token' from your Discord App. |
