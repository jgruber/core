"""Config flow for EcoPlug."""
from pyecoplug import EcoDiscovery

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    devices = {}
    device_count = 0

    def add(plug):
        if plug.name not in devices:
            devices[plug.name] = plug

    def remove(plug):
        pass

    disco = EcoDiscovery(add, remove)
    disco.start()
    device_count = len(devices.items())
    disco.stop()

    return device_count > 0


config_entry_flow.register_discovery_flow(DOMAIN, "EcoPlug", _async_has_devices)
