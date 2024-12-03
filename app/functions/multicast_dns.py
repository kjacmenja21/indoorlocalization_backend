import asyncio
import logging

from zeroconf import ServiceInfo, Zeroconf


class MulticastDNS:
    def __init__(self, hostname: str, port: int) -> None:
        self.zeroconf = Zeroconf()
        self.service_type = "_http._tcp.local."
        self.hostname = hostname
        self.port = port
        self.service_info = ServiceInfo(
            type_=self.service_type,
            name=f"{self.hostname}.{self.service_type}",
            addresses=[b"\x00\x00\x00\x00"],  # Placeholder; this will be auto-detected
            port=self.port,
            properties={},
            server=f"{self.hostname}.local.",
        )

    async def register_service(self):
        logging.info(f"Registering service {self.service_info.name}")
        await asyncio.to_thread(self.zeroconf.register_service, self.service_info)

    async def unregister_service(self):
        logging.info(f"Unregistering service {self.service_info.name}")
        await asyncio.to_thread(self.zeroconf.unregister_service, self.service_info)
        await asyncio.to_thread(self.zeroconf.close)
