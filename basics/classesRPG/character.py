from weapons import fists
from weapons import Weapon
from health_bar import HealthBar

class Character:
    race = "Human"
    def __init__(self,name: str,health: int) -> None:
        self.name = name
        self.health = health
        self.maxHealth = health
        self.weapon = fists

    def attack(self,target) -> None:
        target.health -= self.weapon.damage
        target.health = max(target.health,0)
        target.health_bar.update()
        print(f"{self.name} attacks {target.name} with {self.weapon.name} for {self.weapon.damage} damage!")

    def __str__(self) -> str:
        return f"Name: {self.name}, Health: {self.health}/{self.maxHealth}, Damage: {self.damage}"


class Hero(Character):
    def __init__(self,name: str,health: int) -> None:
        super().__init__(name=name,health=health)
        self.defaultWeapon = self.weapon
        self.health_bar = HealthBar(entity=self,color="green")

    def equip(self,weapon: Weapon) -> None:
        self.weapon = weapon
        print(f"{self.name} equips {weapon.name} as their weapon!")

    def drop(self) -> None:
        self.weapon = self.defaultWeapon
        print(f"{self.name} drops their weapon!")


class Enemy(Character):
    def __init__(self,name: str,health: int,weapon: Weapon) -> None:
        super().__init__(name=name,health=health)
        self.weapon = weapon
        self.health_bar = HealthBar(entity=self,color="red")