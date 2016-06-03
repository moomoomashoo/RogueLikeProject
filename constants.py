# Colors
BLACK           = (0, 0, 0)
WHITE           = (255, 255, 255)
GREEN           = (0, 255, 0)
DARK_GREEN      = (0, 200, 0)
RED             = (255, 0, 0)
BLUE            = (0, 0, 255)
LIGHT_BLUE      = (100, 100, 255)
GREY            = (100, 100, 100)
YELLOW          = (255, 255, 0)
BROWN           = (255, 100, 100)
ORANGE          = (200, 200, 100)
PURPLE          = (255, 0, 255)

# Different types of wall
PERM_WALL = 0
WALL = 1
PERM_FLOOR = 2
FLOOR = 3

SPAWN_POINT = "S"
EXIT_POINT = "E"

GHOST = "G"
min_ghosts = 0
max_ghosts = 2

SHOOTER = "Sh"
min_shooters = 0
max_shooters = 2

CANNON = "Ca"
min_cannons = 1
max_cannons = 4

BOUNCER = "B"
min_bouncers = 2
max_bouncers = 4

FLYER = "F"
min_flyers = 3
max_flyers = 8

CHEST = "C"
min_chests = 1
max_chests = 2

TREASURE = "T"
min_treasure = 10
max_treasure = 20

# The amount the level should be filled initially
# HIGHER = EMPTIER MAP
percent_fill = 0.41
 
# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# How many tiles should be in each level
screen_tiles_width = 60
screen_tiles_height = 60

#The constant tile size
tile_size = 48

#frame rate
frame_rate = 60

# Random seed
SEED = 420