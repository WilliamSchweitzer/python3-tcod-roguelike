from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.baseComponent import BaseComponent
from inputHandlers import GameOverEventHandler
from renderOrder import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor


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
        if self._hp == 0 and self.parent.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.parent:
            deathMessage = "You died!"
            deathMessageColor = color.playerDie
            self.engine.eventHandler = GameOverEventHandler(self.engine)
        else:
            deathMessage = f"{self.parent.name} had died!"
            deathMessageColor = color.enemyDie

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocksMovement = False
        self.parent.ai = None
        self.parent.name = f"Remains of {self.parent.name}"
        self.parent.renderOrder = RenderOrder.CORPSE

        self.engine.messageLog.addMessage(deathMessage, deathMessageColor)
