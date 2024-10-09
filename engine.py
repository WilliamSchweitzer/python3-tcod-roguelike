from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from actions import EscapeAction, MovementAction
from entity import Entity
from gameMap import GameMap
from inputHandlers import EventHandler

class Engine:
    def __init__(self, eventHandler: EventHandler, gameMap: GameMap, player: Entity):
        self.eventHandler = eventHandler
        self.gameMap = gameMap
        self.player = player
        self.updateFov()

    def handleEvents(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.eventHandler.dispatch(event)

            if action is None:
                continue
            
            action.perform(self, self.player)

            self.updateFov()

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
