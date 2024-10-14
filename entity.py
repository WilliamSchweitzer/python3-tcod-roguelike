from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from renderOrder import RenderOrder

if TYPE_CHECKING:
    from componenets.ai import BaseAI
    from componenets.fighter import Figter
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    # Generic object to represent players, enemies, items, etc.
    
    gamemap: GameMap

    def __init__(
        self,
        gamemap: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocksMovement: bool = False,
        renderOrder: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocksMovement = blocksMovement
        self.renderOrder = renderOrder
        if gamemap:
            # If gameMap isn't provided now then it will be set later.
            self.gameMap = gamemap
            gamemap.entites.add(self)

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location. Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "gamemap"): # Possibly uninitialized.
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        fighter: Fighter
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocksMovement=True,
            renderOrder=RenderOrder.ACTOR
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.entity = self

    @property
    def isAlive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)
