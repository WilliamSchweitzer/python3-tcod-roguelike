from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from entity import Actor, Item
import tileTypes

if TYPE_CHECKING:
    from engine import engine
    from entity import Entity


class GameMap:
    def __init__(
        self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()
    ):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tileTypes.wall, order="F")

        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        ) # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        ) # Tiles the player has previously seen

       # self.tiles[30:33, 22] = tileTypes.wall

    @property
    def gameMap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.isAlive
        )

    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def getBlockingEntityAtLocation(
        self, locationX: int, locationY: int
    ) -> Optional[Entity]:
        for entity in self.entities:
            if (
                entity.blocksMovement
                and entity.x == locationX
                and entity.y == locationY
            ):
                return entity

        return None

    def getActorAtLocation(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        
        return None

    def inBounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.

        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.rgb[0 : self.width, 0 :  self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tileTypes.SHROUD,
        )

        entitiesSortedForRendering = sorted(
            self.entities, key=lambda x: x.renderOrder.value
        )

        for entity in entitiesSortedForRendering:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
