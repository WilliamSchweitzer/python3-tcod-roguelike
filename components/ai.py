from  __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np
import tcod

from actions import Action, MeleeAction, MovementAction, WaitAction

if TYPE_CHECKING:
    from entity import Actor


class BaseAI(Action):
    def perform(self) -> None:
        raise NotImplementedError()

    def getPathTo(self, destX: int, destY: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then return an empty list.
        """

        # Copy the walkable array.
        cost = np.array(self.entity.gameMap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gameMap.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking.)
            if entity.blocksMovement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemeies will crowd behind each other in
                # hallways. A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pazss that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y)) # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((destX, destY))[1:].tolist()
        

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy)) # Chebyshev distance.

        if self.engine.gameMap.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return MeleeAction(self.entity, dx, dy).perform()

            self.path = self.getPathTo(target.x, target.y)

        if self.path:
            destX, destY = self.path.pop(0)
            return MovementAction(
                self.entity, destX - self.entity.x, destY - self.entity.y,
            ).perform()

        return WaitAction(self.entity).perform()
