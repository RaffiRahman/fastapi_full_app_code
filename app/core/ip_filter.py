import ipaddress

from fastapi import HTTPException, Request

from app.core.config import settings


class IPFilter:
    def __init__(self, allowed_ips: list[str] | None = None):
        self.allowed_ips: set[str] = set()
        if allowed_ips:
            for ip in allowed_ips:
                self.add_ip(ip)

    def add_ip(self, ip: str):
        """Add an IP or CTDR range to the whitelist."""
        try:
            # Check if it's a CIDR range
            if "/" in ip:
                network = ipaddress.ip_network(ip, strict=False)
                self.allowed_ips.add(str(network))
            else:
                # Single IP address
                ipaddress.ip_address(ip)
                self.allowed_ips.add(ip)
        except ValueError:
            raise ValueError(f"Invalid IP address or CIDR range: {ip}")

    def is_allowed(self, ip: str) -> bool:
        """Check if an IP is allowed."""
        if not self.allowed_ips:
            return True # Allow all if no restrictions set

        try:
            ip_addr = ipaddress.ip_address(ip)
            # Check direct IP match
            if str(ip_addr) in self.allowed_ips:
                return True

            # Check CIDR ranges
            for allowed in self.allowed_ips:
                if "/" in allowed:
                    network = ipaddress.ip_network(allowed, strict=False)
                    if ip_addr in network:
                        return True
            return False
        except ValueError:
            return False

ip_filter = IPFilter(settings.ADMIN_ALLOWED_IPS)


async def verify_admin_ip(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    if not ip_filter.is_allowed(client_ip):
        raise HTTPException(status_code=403, detail="Access denied: Your IP is not whitelisted for admin access.")