# Configuring the application

The application can be configured via TOML files. It will look for these files in the `/opt/disco/run/` directory. The
format and structure of these files is detailed here.

As described on the landing page, the `/opt/disco/` directory should be a volume mounted into the container at runtime
so that you can manage the configuration files on the host system. This also makes it so that logs and databases are
persistent.

## Secrets (required)
Location of the file: `/opt/disco/run/secrets.toml`

### Secrets schema documentation
```{include} ../../res/schemas/secrets.v1.md
```

### Secrets example
```{literalinclude} ../../res/schemas/secrets.v1.example.toml
---
language: toml
---
```

## Bot (optional)
Location of the file: `/opt/disco/run/bot.toml`

### Bot schema documentation
```{include} ../../res/schemas/bot.v1.md
```

### Bot example
```{literalinclude} ../../res/schemas/bot.v1.example.toml
---
language: toml
---
```

## Podcasts (optional)
Location of the file: `/opt/disco/run/podcasts.toml`

### Podcasts schema documentation
```{include} ../../res/schemas/podcasts.v1.md
```

### Podcasts example
```{literalinclude} ../../res/schemas/podcasts.v1.example.toml
---
language: toml
---
```
