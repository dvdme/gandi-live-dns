import argparse
import logging
import sys
import time

import requests

import config
from ip_lookup_services import IPLookupServices

logger = logging.getLogger(__name__)
LOG_LEVEL = logging.INFO
logging.basicConfig(
    stream=sys.stdout,
    format="%(levelname)s %(asctime)s %(message)s",
    encoding="utf-8",
    level=LOG_LEVEL,
)


class GandiDynamicDNS:

    IPV4 = "ipv4"
    IPV6 = "ipv6"

    def __init__(self, subdomain, domain, force_update=False):
        self._subdomain = subdomain
        self._domain = domain
        self._force_update = force_update
        self._headers = {
            "authorization": f"Bearer {config.api_key}",
            "content-type": "application/json",
        }
        self._record_exists = {self.IPV4: False, self.IPV6: False}
        self._dns_needs_update = {self.IPV4: True, self.IPV6: True}
        logger.info(f"Subdomain: {self._subdomain}, Domain: {self._domain}")
        self._update_addresses()
        self._update_record_exists()

    def _update_addresses(self):
        self._addresses = IPLookupServices(config.ifconfig).get_result()
        logger.debug(f"Addresses: {self._addresses}")

    def _update_record_exists(self):
        for ip_version in [self.IPV4, self.IPV6]:
            rtype = "AAAA" if ip_version == self.IPV6 else "A"
            res = requests.get(
                f"{config.api_endpoint}/livedns/domains/{self._domain}/records/{self._subdomain}/{rtype}",
                headers=self._headers,
                timeout=10,
            )
            self._record_exists[ip_version] = res.status_code == requests.codes.ok
            if not self._force_update:
                dns_value = (
                    res.json()["rrset_values"][0]
                    if self._record_exists[ip_version]
                    and len(res.json()["rrset_values"]) > 0
                    else None
                )
                self._dns_needs_update[ip_version] = (
                    not dns_value == self._addresses[ip_version]
                )
            logger.debug(f"{ip_version}: {res}")

    def _update_record(self, ip_version, create=False):
        verb = "POST" if create else "PUT"
        rtype = "AAAA" if ip_version == self.IPV6 else "A"
        res = requests.request(
            verb,
            f"{config.api_endpoint}/livedns/domains/{self._domain}/records/{self._subdomain}/{rtype}",
            headers=self._headers,
            json={
                "rrset_values": [self._addresses[ip_version]],
                "rrset_ttl": config.ttl,
            },
            timeout=10,
        )
        if res.status_code == requests.codes.created:
            logger.info(
                f"{'Updated' if verb == 'PUT' else 'Created'} {self._subdomain}.{self._domain} with value {self._addresses[ip_version]}"
            )
        else:
            logger.error(
                f"Failed to {'update' if verb == 'PUT' else 'Creatcreateed'} {self._subdomain}.{self._domain}"
            )

    def execute(self):
        for ip_version in [self.IPV4, self.IPV6]:
            if self._dns_needs_update[ip_version]:
                if self._addresses[ip_version] is not None:
                    self._update_record(
                        ip_version, create=not self._record_exists[ip_version]
                    )
            else:
                logger.info(
                    f"{self._subdomain}.{self._domain} is correct, skipping update"
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "-f", "--force", help="force an update/create", action="store_true"
    )
    parser.add_argument(
        "-r", "--repeat", type=int, help="keep running and repeat every N seconds"
    )
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    try:
        while True:
            for item in config.subdomains:
                gdd = GandiDynamicDNS(item, config.domain, force_update=args.force)
                gdd.execute()
            if args.repeat:
                logger.info(f"Sleeping for {args.repeat} seconds")
                time.sleep(args.repeat)
            else:
                break
    except KeyboardInterrupt:
        sys.exit(0)
