from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from inputHandlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from gameMap import GameMap

class Engine:
    gameMap: GameMap

    def __init__(self, player: Entity):
        self.eventHandler: EventHandler = EventHandler(self)
        self.player = player

    def handleEnemyTurns(self) -> None:
        for entity in self.gameMap.entities - {self.player}:
            print(f"The {entity.name} wonders why it won't attack back.")

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

        context.present(console)

        console.clear()
