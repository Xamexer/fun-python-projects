import os
from character import Hero, Enemy
from weapons import short_bow, iron_sword

hero = Hero(name="Hero", health=50)
enemy = Enemy(name="Zet", health=40, weapon=short_bow)

weapon_switched = False

while True:
    os.system("cls")
    hero.attack(enemy)
    enemy.attack(hero)
    hero.health_bar.draw()
    enemy.health_bar.draw()

    if hero.health < hero.maxHealth / 2 and not weapon_switched:
        hero.equip(iron_sword)
        weapon_switched = True

    if hero.health <= 0:
        print("The enemy wins!")
        break
    elif enemy.health <= 0:
        print("The hero wins!")
        break

    input("Press Enter to continue...")
