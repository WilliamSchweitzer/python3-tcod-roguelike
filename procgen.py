from __future__ import annotations

import random
from typing import Iterator, Tuple, TYPE_CHECKING

import tcod

import entityFactories
from gameMap import GameMap
import tileTypes

if TYPE_CHECKING:
    from engine import Engine

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def center(self) -> Tuple[int, int]:
        centerX = int((self.x1 + self.x2) / 2)
        centerY = int((self.y1 + self.y2) / 2)

        return centerX, centerY

    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with other RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def placeEntities(
    room: RectangularRoom, dungeon: GameMap, maximumMonsters: int, maximumItems: int,
) -> None:
    numberOfMonsters = random.randint(0, maximumMonsters)
    numberOfItems = random.randint(0, maximumItems)

    for i in range(numberOfMonsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entityFactories.orc.spawn(dungeon, x, y)
            else:
                entityFactories.troll.spawn(dungeon, x, y)

    for i in range(numberOfItems):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entityFactories.healthPotion.spawn(dungeon, x, y)

def tunnelBetween(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # Move horizontally, then vertically.
        cornerX, cornerY = x2, y1
    else:
        # Move vertically, then horizontally.
        cornerX, cornerY = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
        yield x, y


def generateDungeon(
    maxRooms: int,
    roomMinSize: int,
    roomMaxSize: int,
    mapWidth: int,
    mapHeight: int,
    maxMonstersPerRoom: int,
    maxItemsPerRoom: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, mapWidth, mapHeight, entities=[player])

    rooms: List[RectangularRoom] = []

    for r in range(maxRooms):
        roomWidth = random.randint(roomMinSize, roomMaxSize)
        roomHeight = random.randint(roomMinSize, roomMaxSize)

        x = random.randint(0, dungeon.width - roomWidth - 1)
        y = random.randint(0, dungeon.height - roomHeight - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        newRoom = RectangularRoom(x, y, roomWidth, roomHeight)

        # Run through the other rooms and see if they intersect with this one.
        if any(newRoom.intersects(otherRoom) for otherRoom in rooms):
            continue # The room intersects, so stop this loop and continue to next
        # If there are no intersections then the room is valid

        # Dig out this rooms inner area.
        dungeon.tiles[newRoom.inner] = tileTypes.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*newRoom.center, dungeon)
        else:
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnelBetween(rooms[-1].center, newRoom.center):
                dungeon.tiles[x, y] = tileTypes.floor

        placeEntities(newRoom, dungeon, maxMonstersPerRoom, maxItemsPerRoom)

        # Append the new room to the list.
        rooms.append(newRoom)

    return dungeon
