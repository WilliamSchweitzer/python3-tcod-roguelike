from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from inputHandlers import MainGameEventHandler
from messageLog import MessageLog
from renderFunctions import renderBar, renderNamesAtMouseLocation

if TYPE_CHECKING:
    from entity import Actor
    from gameMap import GameMap
    from inputHandlers import EventHandler

class Engine:
    gameMap: GameMap

    def __init__(self, player: Actor):
        self.eventHandler: EventHandler = MainGameEventHandler(self)
        self.messageLog = MessageLog()
        self.mouseLocation = (0, 0)
        self.player = player

    def handleEnemyTurns(self) -> None:
        for entity in set(self.gameMap.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass # Ignore NPC exceptions

    def updateFov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.gameMap.visible[:] = compute_fov(
            self.gameMap.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" is should be added to "explored".
        self.gameMap.explored |= self.gameMap.visible

    def render(self, console: Console) -> None:
        self.gameMap.render(console)

        self.messageLog.render(console=console, x=21, y=45, width=40, height=5)

        renderBar(
            console=console,
            currentValue=self.player.fighter.hp,
            maximumValue=self.player.fighter.maxHP,
            totalWidth=20,
        )

        renderNamesAtMouseLocation(console=console, x=21, y=44, engine=self)

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.maxHP}",
        )
