colliders = None

def initialize_colliders(tiles):
    global colliders
    colliders = {
        'walkable': [tiles['air'], tiles['grass']],
        'solid': [tiles['wall'], tiles['tree']],
        'moveable': [tiles['wall']],
        'solid_sprites': ['box']  # Add sprite types that should be treated as solid
    }


def get_colliders(tiles):
    if colliders is None:
        initialize_colliders(tiles)
    return colliders
