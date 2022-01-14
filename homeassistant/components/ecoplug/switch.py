"""Platform for EcoPlug switch Integration."""
import logging
from typing import Any

from pyecoplug import EcoDiscovery

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType = None,
) -> None:
    """Set up the EcoPlug Switch platform."""

    plugs = {}

    def add(plug):
        if plug.name not in plugs:
            plugs[plug.name] = plug

    def remove(plug):
        if plug.name in plugs:
            del plugs[plug.name]

    disco = EcoDiscovery(add, remove)
    disco.start()

    add_entities(EcoPlugSwitch(plug) for plug in plugs.items())


class EcoPlugSwitch(SwitchEntity):
    """Representation of an EcoPlug Switch."""

    def __init__(self, plug) -> None:
        """Initialize EcoPlug switch."""
        self._plug = plug
        self._name = plug.name
        self._state = self._plug.is_on()

    @property
    def name(self) -> str:
        """Return the display name of this switch."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return turn if the switch is on."""
        return bool(self._state)

    @property
    def should_poll(self) -> bool:
        """Return if polling should take place."""
        return True

    def update(self) -> None:
        """Fetch switch state."""
        self._state = self._plug.is_on()

    def turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        self._plug.turn_on()
        self.update()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the switch."""
        self._plug.turn_off()
        self.update()
