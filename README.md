# Gandi Live DNS

A dynamic DNS updater for the [Gandi](https://www.gandi.net) registrar. It uses Gandi's [LiveDNS REST API](http://doc.livedns.gandi.net/) to update the zone file for one or more subdomains of a domain to point at the external address computer it has been run from.

## Features

- Supports multiple subdomains;
- IPv4 and IPv6 support, depending on the IP lookup service (see table bellow);
- Creates the subdomain if it not exists;
- Only tries to update if the IP addresses do not match.

### IP Lookup Services

Different IP lookup service providers are supported. Not all services support both IPv4 and IPv6.

See table bellow:

| Service                       | IPv4          | IPv6         |
| ----------------------------- | ------------- | -------------|
| http://whatismyip.akamai.com  | Yes           | No           |
| https://ifconfig.co/ip        | Yes           | Yes          |
| http://ifconfig.me/ip         | Yes           | Yes          |
| http://ipinfo.io/ip           | Yes           | No           |

## How to run

A Gandi API Key is needed, see how to get it in [https://api.gandi.net/docs/authentication/](https://api.gandi.net/docs/authentication/).

- Clone the repository;
- Rename `example.config.py` to `config.py`;
- Set the config with the appropriate values (for reference, see comments in the file);

### From git

- Create a virtual environment: `python3 -m venv venv`;
- Run it: `python3 gandi_live_dns.py`

### From Docker

#### Building locally

- `docker build -t gandi-live-dns:local .`
- `docker run --rm -it -v $(pwd)/config.py:/usr/src/gandi_live_dns/config.py gandi-live-dns:local --force`

### Command line options

```
usage: gandi_live_dns.py [-h] [-v] [-f] [-r REPEAT]

options:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -f, --force           force an update/create
  -r REPEAT, --repeat REPEAT
                        keep running and repeat every N seconds
```

choose one as described in the config file.

### Run continuously

#### Run with the repeat flag

Use `--repeat <seconds>` to run continuously.

Example command with Docker to run continuously in the background:

- `docker run --restart unless-stopped -d -it -v $(pwd)/config.py:/usr/src/gandi_live_dns/config.py gandi-live-dns:local --repeat 1800`

#### Cron the script

Run the script every five minutes.
```
*/5 * * * * python3 gandi-live-dns.py >/dev/null 2>&1
```

### Issues

Use GitHub issues, avoid sending email's to the mail that is in git history as it is not available anymore.

### Acknowledgment

- First ideia: `https://github.com/cavebeat/gandi-live-dns`

#### (Past) Inspiration

This DynDNS updater is inspired by https://github.com/jasontbradshaw/gandi-dyndns which worked very well
with the classic DNS from Gandiv4 Website and their XML-RPC API.

Gandi has created a new API, i accidently switched to the new DNS Record System, so someone had to start a new updater.
