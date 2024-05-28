"""
Gandi API key
"""
api_key = "-- API_KEY --"

"""
Gandiv5 LiveDNS API Location
https://api.gandi.net/v5
"""
api_endpoint = "https://api.gandi.net/v5"

"""
Domain to be used
"""
domain = "mydomain.tld"

"""
Subdomains to be updated.
Subdomains will be created first if not already present
"""
subdomains = ["subdomain1", "subdomain2", "subdomain3"]

"""
DNS record TTL
300 seconds = 5 minutes
"""
ttl = "300"

"""
IP address lookup service
"ipclaranet" for "http://ip.clara.net",
"ipinfoio" for "http://ipinfo.io/ip",
"ifconfigme" for "http://ifconfig.me/ip",
"ifconfigco" for "https://ifconfig.co/ip",
"akamai" for "http://whatismyip.akamai.com/"
"""
ifconfig = "choose_from_above_or_run_your_own"
