from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.ai
import components.inventory
from components.baseComponent import BaseComponent
from exceptions import Impossible
from inputHandlers import SingleRangedAttackHandler

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


class ConfusionConsumable(Consumable):
    def __init__(self, numberOfTurns: int):
        self.numberOfTurns = numberOfTurns

    def getAction(self, consumer: Actor) -> Optional[actions.Action]:
        self.engine.messageLog.addMessage(
            "Select a target location.", color.needsTarget
        )
        self.engine.eventHandler = SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: actions.ItemAction(consumer, self.parent, xy),
        )
        return None

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        target = action.targetActor

        if not self.engine.gameMap.visible[action.targetXY]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if target is consumer:
            raise Impossible("You cannot confuse yourself!")

        self.engine.messageLog.addMessage(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            color.statusEffectApplied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target, previousAi=target.ai, turnsRemaining=self.numberOfTurns,
        )
        self.consume()


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

        for actor in self.engine.gameMap.actors:
            if actor is not consumer and self.parent.gameMap.visible[actor.x, actor.y]:
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
