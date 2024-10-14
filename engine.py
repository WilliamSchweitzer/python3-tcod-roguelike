from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from inputHandlers import MainGameEventHandler

if TYPE_CHECKING:
    from entity import Actor
    from gameMap import GameMap
    from inputHandlers import EventHandler

class Engine:
    gameMap: GameMap

    def __init__(self, player: Actor):
        self.eventHandler: EventHandler = MainGameEventHandler(self)
        self.player = player

    def handleEnemyTurns(self) -> None:
        for entity in set(self.gameMap.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def updateFov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.gameMap.visible[:] = compute_fov(
            self.gameMap.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" is should be added to "explored".
        self.gameMap.explored |= self.gameMap.visible

    def render(self, console: Console, context: Context) -> None:
        self.gameMap.render(console)

        console.print(
            x=1,
            y=47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.maxHP}",
        )

        context.present(console)

        console.clear()
