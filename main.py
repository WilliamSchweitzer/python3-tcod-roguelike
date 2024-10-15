#!/usr/bin/env python3
import copy

import tcod

import color
from engine import Engine
import entityFactories
from procgen import generateDungeon

def main() -> None:
    screenWidth = 80
    screenHeight = 50

    mapWidth = 80
    mapHeight = 43

    roomMaxSize = 10
    roomMinSize = 6
    maxRooms = 30

    maxMonstersPerRoom = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entityFactories.player)

    engine = Engine(player=player)

    engine.gameMap = generateDungeon(
        maxRooms=maxRooms,
        roomMinSize=roomMinSize,
        roomMaxSize=roomMaxSize,
        mapWidth=mapWidth,
        mapHeight=mapHeight,
        maxMonstersPerRoom=maxMonstersPerRoom,
        engine=engine,
    )

    engine.updateFov()

    engine.messageLog.addMessage(
        "Welcome to your doom, adventurer.", color.welcomeText
    )

    with tcod.context.new_terminal(
        screenWidth,
        screenHeight,
        tileset=tileset,
        title="Yet Another Roguelike Tutorial",
        vsync=True,
    ) as context:
        rootConsole = tcod.console.Console(screenWidth, screenHeight, order="F")
        while True:
            rootConsole.clear()
            engine.eventHandler.on_render(console=rootConsole)
            context.present(rootConsole)
            
            engine.eventHandler.handle_events(context)


if __name__ == "__main__":
    main()
