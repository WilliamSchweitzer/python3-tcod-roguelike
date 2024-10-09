#!/usr/bin/env python3
import copy

import tcod

from engine import Engine
import entityFactories
from inputHandlers import EventHandler
from procgen import generateDungeon

def main() -> None:
    screenWidth = 80
    screenHeight = 50

    mapWidth = 80
    mapHeight = 45

    roomMaxSize = 10
    roomMinSize = 6
    maxRooms = 30

    maxMonstersPerRoom = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    eventHandler = EventHandler()

    player = copy.deepcopy(entityFactories.player)

    gameMap = generateDungeon(
        maxRooms=maxRooms,
        roomMinSize=roomMinSize,
        roomMaxSize=roomMaxSize,
        mapWidth=mapWidth,
        mapHeight=mapHeight,
        maxMonstersPerRoom=maxMonstersPerRoom,
        player=player,
    )

    engine = Engine(eventHandler=eventHandler, gameMap=gameMap, player=player)

    with tcod.context.new_terminal(
        screenWidth,
        screenHeight,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        rootConsole = tcod.console.Console(screenWidth, screenHeight, order="F")
        while True:
            engine.render(console=rootConsole, context=context)

            events = tcod.event.wait()

            engine.handleEvents(events)

if __name__ == "__main__":
    main()
