from __future__ import annotations

from typing import TYPE_CHECKING

from components.baseComponent import BaseComponent
from inputHandlers import GameOverEventHandler
from renderOrder import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class  Fighter(BaseComponent):
    entity: Actor


    def __init__(self, hp: int, defense: int, power: int):
        self.maxHP = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp


    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.maxHP))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            deathMessage = "You died!"
            self.engine.eventHandler = GameOverEventHandler(self.engine)
        else:
            deathMessage = f"{self.entity.name} had died!"

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocksMovement = False
        self.entity.ai = None
        self.entity.name = f"Remains of {self.entity.name}"
        self.entity.renderOrder = RenderOrder.CORPSE

        print(deathMessage)
