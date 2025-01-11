import asyncio
import socket
from unittest.mock import AsyncMock, patch

import pytest
from zeroconf import ServiceBrowser, Zeroconf

from app.functions.multicast_dns import MulticastDNS, init_mdns

# FILE: test_multicast_dns.py


@pytest.fixture
def multicast_dns() -> MulticastDNS:
    return MulticastDNS(hostname="testhost", port=1234)


def test_multicast_dns_init(multicast_dns: MulticastDNS):
    assert multicast_dns.hostname == "testhost"
    assert multicast_dns.port == 1234
    assert multicast_dns.service_type == "_http._tcp.local."
    assert multicast_dns.service_info.name == "testhost._http._tcp.local."


@pytest.mark.asyncio
async def test_get_hostname(multicast_dns: MulticastDNS):
    await multicast_dns.register_service()
    expected = socket.gethostbyname(socket.gethostname())
    actual = socket.inet_ntoa(multicast_dns.get_hostname())
    result = expected == actual
    await multicast_dns.unregister_service()
    assert result


@pytest.mark.asyncio
async def test_multicast_dns_service_browser(multicast_dns: MulticastDNS):

    class ServiceListener:
        def __init__(self):
            self.services = []

        def add_service(self, zeroconf, type, name):
            self.services.append(name)

    zeroconf = Zeroconf()
    listener = ServiceListener()
    browser = ServiceBrowser(zeroconf, multicast_dns.service_type, listener)

    await multicast_dns.register_service()
    await asyncio.sleep(2)  # Give some time for the service to be discovered

    assert any(
        multicast_dns.service_info.name in service for service in listener.services
    )

    await multicast_dns.unregister_service()
    zeroconf.close()
