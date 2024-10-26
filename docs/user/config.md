# Configuring the application

The application can be configured via TOML files. It will look for these files in the `/opt/disco/run/` directory. The
format and structure of these files is detailed here.

As described on the landing page, the `/opt/disco/` directory should be a volume mounted into the container at runtime
so that you can manage the configuration files on the host system. This also makes it so that logs and databases are
persistent.

## `secrets.toml`
*Forthcoming*

## `podcasts.toml`
*Forthcoming*
