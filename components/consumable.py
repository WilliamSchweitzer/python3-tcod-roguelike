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

class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, maximumRange: int):
        self.damage = damage
        self.maximumRange = maximumRange

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = None
        closestDistance = self.maximumRange + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closestDistance:
                    target = actor
                    closestDistance = distance

        if target:
            self.engine.messageLog.addMessage(
                f"A lightning bolt strikes the {target.name} with a loud thunder, for {self.damage} damage!"
            )
            target.fighter.takeDamage(self.damage)
            self.consume()
        else:
            raise Impossible("No enemy is close enough to strike.")
