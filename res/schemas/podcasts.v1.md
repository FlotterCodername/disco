This configuration stores everything related to podcast feeds.

### Podcasts top level
| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| $schema | string (uri) |  | Which JSONSchema the file follows. |
| podcast | array[object] |  | Podcast feeds to forward to a Discord channel. |

#### `podcast[]` (Optional)

Array items:

| Property | Type | Required | Description |
|----------|:----:|:--------:|-------------|
| forward_channel | string | Yes | The exact name of the channel where podcast episodes shall appear. |
| forward_guild | string | Yes | The exact name of the Discord server ('guild') where `forward_channel` is located. |
| name | string | Yes | Your chosen name of the podcast (must be unique). May appear in user-facing text. |
| url_artwork | string (uri) |  | The URL for the podcast cover art. This is also be used as a fallback whenever episode artwork is not available. |
| url_feed | string (uri) | Yes | The URL for the podcast RSS feed. |
