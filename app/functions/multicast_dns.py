from zeroconf import ServiceInfo, Zeroconf


def register_service(hostname: str, port: int) -> tuple[Zeroconf, ServiceInfo]:
    zeroconf = Zeroconf()
    service_type = "_http._tcp.local."
    service_name = f"{hostname}.{service_type}"
    service_info = ServiceInfo(
        type_=service_type,
        name=service_name,
        address=b"\x00\x00\x00\x00",  # Placeholder; this will be auto-detected
        port=port,
        properties={},
        server=f"{hostname}.local.",
    )
    zeroconf.register_service(service_info)
    return zeroconf, service_info
