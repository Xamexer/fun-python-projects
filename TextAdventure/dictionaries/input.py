from enum import Enum

class Input(Enum):
    MENU = 0
    CONFIRM = 1
    BACK = 2
    LEFT = 3
    UP = 4
    RIGHT = 5
    DOWN = 6

input = {
    Input.MENU : ["f","F"],
    Input.CONFIRM : ["g","G"],
    Input.BACK : ["v","V"],
    Input.LEFT : ["KEY_LEFT","a","A"],
    Input.UP : ["KEY_UP","w","W"],
    Input.RIGHT : ["KEY_RIGHT","d","D"],
    Input.DOWN : ["KEY_DOWN","s","S"]
}