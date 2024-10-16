from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
from components.baseComponent import BaseComponent
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def getAction(self, consumer: Actor) -> Optional[actions.Action]:
        """Try to return the action for this item."""
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        """Invoke this items ability.

        `action` is the context for this activation.
        """
        raise NotImplementedError()

    def consume(self) -> None:
        """Remove the consumed item from its containing inventory."""
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amountRecovered = consumer.fighter.heal(self.amount)

        if amountRecovered > 0:
            self.engine.messageLog.addMessage(
                f"You consume the {self.parent.name}, and recover {amountRecovered} HP!",
                color.healthRecovered,
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")
