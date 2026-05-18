"""Binary sensor platform for Geekworm X728 UPS."""
from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import X728DataCoordinator
from .const import (
    DOMAIN,
    KEY_AC_PRESENT,
    KEY_BATTERY_LOW,
    KEY_CHARGING,
    KEY_HW_VERSION,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up X728 binary sensors."""
    coordinator: X728DataCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            X728AcPresentSensor(coordinator, entry),
            X728BatteryLowSensor(coordinator, entry),
            X728ChargingSensor(coordinator, entry),
        ]
    )


class X728BaseBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Base binary sensor."""

    def __init__(
        self,
        coordinator: X728DataCoordinator,
        entry: ConfigEntry,
        key: str,
        name: str,
        unique_suffix: str,
    ) -> None:
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{unique_suffix}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Geekworm X728 UPS",
            "manufacturer": "Geekworm",
            "model": coordinator.data.get(KEY_HW_VERSION, "X728"),
        }

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.get(self._key)

    @property
    def available(self) -> bool:
        return self.coordinator.last_update_success and self._key in (
            self.coordinator.data or {}
        )


class X728AcPresentSensor(X728BaseBinarySensor):
    """AC power present sensor."""

    def __init__(self, coordinator, entry):
        super().__init__(
            coordinator, entry, KEY_AC_PRESENT, "X728 AC Power", "ac_present"
        )
        self._attr_device_class = BinarySensorDeviceClass.PLUG
        self._attr_icon = "mdi:power-plug"


class X728BatteryLowSensor(X728BaseBinarySensor):
    """Battery low alert sensor."""

    def __init__(self, coordinator, entry):
        super().__init__(
            coordinator, entry, KEY_BATTERY_LOW, "X728 Battery Low", "battery_low"
        )
        self._attr_device_class = BinarySensorDeviceClass.BATTERY
        self._attr_icon = "mdi:battery-alert"


class X728ChargingSensor(X728BaseBinarySensor):
    """Battery charging sensor."""

    def __init__(self, coordinator, entry):
        super().__init__(
            coordinator, entry, KEY_CHARGING, "X728 Charging", "charging"
        )
        self._attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING
        self._attr_icon = "mdi:battery-charging"
