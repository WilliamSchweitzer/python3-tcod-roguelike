from __future__ import annotations

from typing import TYPE_CHECKING

import color

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from gameMap import GameMap


def getNamesAtLocation(x: int, y: int, gameMap: GameMap) -> str:
    if not gameMap.inBounds(x, y) or not gameMap.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in gameMap.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def renderBar(
    console: Console, currentValue: int, maximumValue: int, totalWidth: int
) -> None:
    barWidth = int(float(currentValue) / maximumValue * totalWidth)

    console.draw_rect(x=0, y=45, width=totalWidth, height=1, ch=1, bg=color.barEmpty)

    if barWidth > 0:
        console.draw_rect(
            x=0, y=45, width=barWidth, height=1, ch=1, bg=color.barFilled
        )

    console.print(
        x=1, y=45, string=f"HP: {currentValue}/{maximumValue}", fg=color.barText
    )

def renderNamesAtMouseLocation(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouseX, mouseY = engine.mouseLocation

    namesAtMouseLocation = getNamesAtLocation(
        x=mouseX, y=mouseY, gameMap=engine.gameMap
    )

    console.print(x=x, y=y, string=namesAtMouseLocation)
