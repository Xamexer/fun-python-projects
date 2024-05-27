class Weapon:
    def __init__(self,name: str, weaponType: str, damage: int, value: int) -> None:
        self.name = name
        self.weaponType = weaponType
        self.damage = damage
        self.value = value

    def __str__(self) -> str:
        return f"Name: {self.name}, Type: {self.weaponType}, Damage: {self.damage}, Value: {self.value}"
    
iron_sword = Weapon(name="Iron Sword",weaponType="sharp",damage=5,value=10)
short_bow = Weapon(name="Short Bow",weaponType="ranged",damage=4,value=8)
fists = Weapon(name="Fists",weaponType="blunt",damage=2,value=0)