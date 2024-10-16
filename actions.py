from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity

class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gameMap.engine

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

class WaitAction(Action):
    def perform(self) -> None:
        pass

class ActionWithDirection(Action):
    def __init__(self,  entity: Actor, dx: int, dy: int):
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

    @property
    def targetActor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.gameMap.getActorAtLocation(*self.destXY)

    def perform(self) -> None:
        raise NotImplementedError()

class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.targetActor
        if not target:
            raise exceptions.Impossible("There is nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attackDesc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attackColor = color.playerAtk
        else:
            attackColor = color.enemyAtk

        if damage > 0:
            self.engine.messageLog.addMessage(
                f"{attackDesc} for {damage} hit points.", attackColor
            )
            target.fighter.hp -= damage
        else:
            self.engine.messageLog.addMessage(
                f"{attackDesc} but does no damage.", attackColor
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        destX, destY = self.destXY

        if not self.engine.gameMap.inBounds(destX, destY):
            # Destination is out of bounds
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.gameMap.tiles["walkable"][destX, destY]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.gameMap.getBlockingEntityAtLocation(destX, destY):
            # Destination is blocked by entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)

class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.targetActor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
