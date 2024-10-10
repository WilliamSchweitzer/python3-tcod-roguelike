from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by the Action subclasses.
        """

        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self)  -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self,  entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy
    @property
    def destXY(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blockingEntity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination."""
        return self.engine.gameMap.getBlockingEntityAtLocation(*self.destXY)

    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        target = self.blockingEntity
        if not target:
            return # No entity to attack.

        print(f"You kick the {target.name} in the mouth, reducing it's health a bit.")


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        if not self.engine.gameMap.inBounds(destX, destY):
            return # Destination is out of bounds
        if not self.engine.gameMap.tiles["walkable"][destX, destY]:
            return # Destination is blocked by a tile.
        if self.engine.gameMap.getBlockingEntityAtLocation(destX, destY):
            return # Destination is blocked by entity.

        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        if self.blockingEntity:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
