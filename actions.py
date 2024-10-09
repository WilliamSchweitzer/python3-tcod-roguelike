from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity) -> None:
        """Perform this action with the objects needed to determine its scope.

        `engine` is the scope this action is being performed in.

        `entity` is the object performing the action.

        This method must be overridden by the Action subclasses.
        """

        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, engine: Engine, entity: Entity)  -> None:
        raise SystemExit()

class ActionWithDirection(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        destX = entity.x + self.dx
        destY = entity.y + self.dy
        target = engine.gameMap.getBlockingEntityAtLocation(destX, destY)
        if not target:
            return # No entity to attack.

        print(f"You kick the {target.name} in the mouth, reducing it's health a bit.")


class MovementAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        destX = entity.x + self.dx
        destY = entity.y + self.dy

        if not engine.gameMap.inBounds(destX, destY):
            return # Destination is out of bounds
        if not engine.gameMap.tiles["walkable"][destX, destY]:
            return # Destination is blocked by a tile.
        if engine.gameMap.getBlockingEntityAtLocation(destX, destY):
            return # Destination is blocked by entity.

        entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self, engine: Engine, entity: Entity) -> None:
        destX = entity.x + self.dx
        destY = entity.y + self.dy

        if engine.gameMap.getBlockingEntityAtLocation(destX, destY):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
