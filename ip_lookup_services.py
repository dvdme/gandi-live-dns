from abc import ABC, abstractmethod

import requests


class IPLookupServiceBase(ABC):

    IPV4 = "ipv4"
    IPV6 = "ipv6"
    _TIMEOUT = 10

    @property
    def result(self):
        _result = {}
        IPLookupServiceBase.force_ipv4(True)
        _addr = self.get()
        _result[self.IPV4] = _addr if self.is_ipv4(_addr) else None
        IPLookupServiceBase.force_ipv4(False)
        _addr = self.get()
        _result[self.IPV6] = _addr if self.is_ipv6(_addr) else None
        return _result

    def is_ipv4(self, address):
        return not self.is_ipv6(address)

    def is_ipv6(self, address):
        return ":" in address

    @abstractmethod
    def get(self):
        pass

    @staticmethod
    def force_ipv4(enable):
        requests.packages.urllib3.util.connection.HAS_IPV6 = not enable


class Akamai(IPLookupServiceBase):

    _SERVICE_ADDRESS = "http://whatismyip.akamai.com/"

    def get(self):
        return requests.get(self._SERVICE_ADDRESS, timeout=self._TIMEOUT).text.strip()


class IfConfigCo(IPLookupServiceBase):

    _SERVICE_ADDRESS = "https://ifconfig.co/ip"

    def get(self):
        return requests.get(self._SERVICE_ADDRESS, timeout=self._TIMEOUT).text.strip()


class IfConfigMe(IPLookupServiceBase):

    _SERVICE_ADDRESS = "http://ifconfig.me/ip"

    def get(self):
        return requests.get(self._SERVICE_ADDRESS, timeout=self._TIMEOUT).text.strip()


class IpInfoIo(IPLookupServiceBase):

    _SERVICE_ADDRESS = "http://ipinfo.io/ip"

    def get(self):
        return requests.get(self._SERVICE_ADDRESS, timeout=self._TIMEOUT).text.strip()


class IpClaraNet(IPLookupServiceBase):

    _SERVICE_ADDRESS = "http://ip.clara.net"

    def get(self):
        return requests.get(self._SERVICE_ADDRESS, timeout=self._TIMEOUT).text.strip()


class IPLookupServices:

    _IP_LOOKUP_SERVICES_MAP = {
        "ipclaranet": IpClaraNet,
        "ipinfoio": IpInfoIo,
        "ifconfigme": IfConfigMe,
        "ifconfigco": IfConfigCo,
        "akamai": Akamai,
    }

    def __init__(self, service_name):
        self._service_name = service_name.lower()
        if self._service_name not in self._IP_LOOKUP_SERVICES_MAP.keys():
            raise ValueError(f"Service {self._service_name} is not known")

    def get_result(self):
        return self._IP_LOOKUP_SERVICES_MAP[self._service_name]().result
