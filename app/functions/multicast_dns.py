import asyncio
import logging
import socket

from zeroconf import ServiceInfo, Zeroconf

from app.config import GeneralConfig


class MulticastDNS:
    def __init__(self, hostname: str, port: int) -> None:
        self.zeroconf = Zeroconf()
        self.service_type = "_http._tcp.local."
        self.hostname = hostname
        self.port = port
        self.service_info = ServiceInfo(
            type_=self.service_type,
            name=f"{self.hostname}.{self.service_type}",
            addresses=[self.get_hostname()],
            port=self.port,
            properties={},
            server=f"{self.hostname}.local.",
        )

    def get_hostname(self) -> bytes:
        return socket.inet_aton(
            socket.gethostbyname(socket.gethostname()),
        )

    async def register_service(self) -> None:
        logging.info("Registering service %s", self.service_info.name)
        await asyncio.to_thread(self.zeroconf.register_service, self.service_info)

    async def unregister_service(self) -> None:
        logging.info("Unregistering service %s", self.service_info.name)
        await asyncio.to_thread(self.zeroconf.unregister_service, self.service_info)
        await asyncio.to_thread(self.zeroconf.close)


async def init_mdns() -> MulticastDNS | None:
    multicast_dns = None
    general_config = GeneralConfig()

    if general_config.mdns_enable:
        multicast_dns = MulticastDNS(
            general_config.mdns_hostname,
            general_config.mdns_port,
        )
        await multicast_dns.register_service()
    return multicast_dns
