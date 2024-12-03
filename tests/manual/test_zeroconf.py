import time

from zeroconf import ServiceBrowser, Zeroconf


class MyListener:
    def __init__(self):
        self.services = {}

    def add_service(self, zeroconf, type, name):
        print(f"Service {name} of type {type} added.")
        self.services[name] = type

    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} of type {type} removed.")
        if name in self.services:
            del self.services[name]

    def update_service(self, zeroconf, type, name):
        print(f"Service {name} of type {type} updated.")


def discover_services():
    zeroconf = Zeroconf()
    listener = MyListener()

    # Service type '_http._tcp.local.' is an example; adjust as needed for your use case.
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

    try:
        # Keep the service discovery running.
        print("Discovering services...")
        while True:
            time.sleep(1)
    finally:
        zeroconf.close()


if __name__ == "__main__":
    discover_services()
