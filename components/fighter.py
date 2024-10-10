from components.baseComponent import BaseComponent


class  Fighter(BaseComponent):
    def __init__(self, hp: int, defense: int, power: int):
        self.maxHP = hp
        self._hp = hp
        self.defense = defense
        self.power = power

    @property
    def hp(self) -> int:
        return self._hp


    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.maxHp))
