from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from renderOrder import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.fighter import Fighter
    from components.inventory import Inventory
    from gameMap import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    # Generic object to represent players, enemies, items, etc.
    
    parent: GameMap

    def __init__(
        self,
        parent: Optional[GameMap] = None,
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
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            gameMap.entites.add(self)

    @property
    def gameMap(self) -> GameMap:
        return self.parent.gameMap

    def spawn(self: T, gameMap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gameMap
        gameMap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gameMap: Optional[GameMap] = None) -> None:
        """Place this entity at a new location. Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gameMap:
            if hasattr(self, "parent"): # Possibly uninitialized.
                if self.parent is self.gameMap:
                    self.gameMap.entities.remove(self)
            self.parent = gameMap
            gameMap.entities.add(self)

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
        fighter: Fighter,
        inventory: Inventory,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocksMovement=True,
            renderOrder=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

    @property
    def isAlive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)

class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unamed>",
        consumable: Consumable,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocksMovement=False,
            renderOrder=RenderOrder.ITEM,
        )

        self.consumable = consumable
        self.consumable.parent = self
