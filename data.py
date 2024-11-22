from player import Player #MW: import the Player class into this file so it has all information regarding the player (ex. current towers placed, number of lives remaining, current level, or available money)

player = Player() #MW:creates an instance of the player class

towerTypes = { #MW: towerTypes is a nested dictionary (dictionary within a dictionary) that stores information about the stats of each type of monkey 
    #cooldown in seconds, range is radius around monkey
    "dartmonkey": #MW: information for the dart monkey tower
        {
        "price": 250, #MW: price of the tower
        "upgrade_price": 200, #MW: price to upgrade the tower
        "cooldown": 0.7, #MW: cooldown time for the tower (how long the monkey has to wait before attacking again)
        "damage": 1, #MW: damage each bullet of the monkey does to bloons
        "slow": 0, #MW: how much the monkey slows the bloons down when it hits them
        "range": 125, #MW: radius of the moneky's range (circle that represents where the monkey can attack)
        "bullet": "basketball", #MW: the kind of object the monkey uses as a bullet (in this case the monkey throws basketballs)
        "description": "Cheap starting tower" #MW: description of the monkey (appears when you hover over it in the side bar)
        },
    "ninjamonkey": #MW: information for the ninja monkey
        {
        "price": 600, 
        "cooldown": 0.3, 
        "upgrade_price": 500,
        "damage": 1, 
        "slow": 0, 
        "range": 175,
        "bullet": "shuriken",
        "description": "Fast shuriken shooter"
        },
    "boat": #MW: information for the boat 
        {
        "price": 700, 
        "cooldown": 0.5, 
        "upgrade_price": 300,
        "damage": 2, 
        "slow": 0, 
        "range": 250,
        "bullet": "bomb",
        "description": "Only place in water"
        },
    "sniper": #MW: information for the sniper
        {
        "price": 500, 
        "cooldown": 1.0,
        "upgrade_price": 500,
        "damage": 2, 
        "slow": 0, 
        "range": 10000,
        "bullet": "ball",
        "description": "Huge range; pops 4 layers"
        },
    "gluegunner": #MW: information for the glue gunner
        {
        "price": 300, 
        "cooldown": 1.2, 
        "upgrade_price": 300,
        "damage": 0, 
        "slow": 1,
        "range": 175,
        "bullet": "glue",
        "description": "Slows bloons with glue"
        },
    "supermonkey": #MW: information for the super monkey
        {
        "price": 3500, 
        "cooldown": 0.001,
        "upgrade_price": 2000,
        "damage": 1,
        "slow": 0,
        "range": 225,
        "bullet": "ball",
        "description": "Shoots super fast lasers"
        },

    #upgraded monkeys    
    "dartmonkey_upgraded": #MW: information for the upgraded version of the dart monkey
        {
        #range increased, cooldown reduced
        "price": 450,
        "upgrade_price": 200,
        "cooldown": 0.4, 
        "damage": 1, 
        "slow": 0, 
        "range": 150,
        "bullet": "basketball",
        "description": "Cheap starting tower"
        },
    "ninjamonkey_upgraded": #MW: information for the upgraded version of the ninja monkey
        {
        #damage increased, range increased, cooldown reduced
        "price": 1100,
        "upgrade_price": 500,
        "cooldown": 0.2, 
        "damage": 2, 
        "slow": 0, 
        "range": 200,
        "bullet": "shuriken",
        "description": "Fast shuriken shooter"
        },
    "boat_upgraded": #MW: information for the upgraded version of the boat
        {
        #cooldown reduced
        "price": 1000,
        "upgrade_price": 300,
        "cooldown": 0.4, 
        "damage": 2, 
        "slow": 0, 
        "range": 250,
        "bullet": "bomb",
        "description": "Only place in water"
        },
    "sniper_upgraded": #MW: information for the upgraded version of the sniper
        {
        #cooldown reduced, damage increased
        "price": 1000,
        "upgrade_price": 500,
        "cooldown": 0.6,
        "damage": 4, 
        "slow": 0, 
        "range": 10000,
        "bullet": "ball",
        "description": "Huge range; pops 4 layers"
        },
    "gluegunner_upgraded": #MW: information for the upgraded version of the glue gunner
        {
        #cooldown reduced, range increased
        "price": 600,
        "upgrade_price": 300,
        "cooldown": 0.8, 
        "damage": 0, 
        "slow": 1,
        "range": 200,
        "bullet": "glue",
        "description": "Slows bloons with glue"
        },
    "supermonkey_upgraded": #MW: information for the upgraded version of the super monkey
        {
        #damage increased, range increased
        "price": 6500,
        "upgrade_price": 2000,
        "cooldown": 0.001,
        "damage": 2,
        "slow": 0,
        "range": 275,
        "bullet": "ball",
        "description": "Shoots super fast lasers"
        }
}

bloons = { #MW: another nested dictionary that holds the stats of each kind of bloon
    #strength correlates with required number of hits to be killed
    "red": #MW: information for the red bloon
        {
        "strength": 1, #MW: how much damage the bloon does to the players lives if it reaches the end of the map
        "speed": 2, #MW: how fast the bloon moves across the map
        },
    "blue": #MW: information for the blue bloon
        {
        "strength": 2,
        "speed": 3,
        },
    "green": #MW: information for the green bloon
        {
        "strength": 3,
        "speed": 4,
        },
    "yellow": #MW: information for the yellow bloon
        {
        "strength": 4,
        "speed": 5,
        },
    "pink": #MW: information for the pink bloon
        {
        "strength": 5,
        "speed": 6,
        },
    "ceramic": #MW: information for the ceramic bloon
        {
        "strength": 20,
        "speed": 4,
        },
    "moab": #MW: information for the moab
        {
        "strength": 350,
        "speed": 1,
        },
}

bloonColors = { #MW: dictionary holding the names of all colours of bloons (excluding ceramic and moab)
    1: "red", 
    2: "blue", 
    3: "green",
    4: "yellow", 
    5: "pink"
}

levels = { #MW: a dictionary containing lists that contain information for each level (each index of the list says how many balloons there are for each tyoe)
    0: [],
    1: [(30,"red"), (10, "blue")], #MW: for example, in level one, there are 30 red balloons and 10 blue balloons
    2: [(30,"red"), (25,"blue"), (5, "green")], 
    3: [(15,"red"), (25,"blue"), (25,"red"), (20,"green")], 
    4: [(10,"red"), (15, "blue"), (20, "green"), (20, "yellow")],
    5: [(30, "red"), (25, "blue"), (20, "green"), 
    (20, "yellow"), (15, "pink")],
    6: [(30, "green"), (30, "yellow"), (30, "pink")], 
    7: [(50, "pink"), (50, "yellow"), (30, "pink")],
    8: [(15, "yellow"), (15, "pink"), (15, "yellow"), 
    (7, "ceramic"), (15, "pink")],
    9: [(50, "blue"), (10, "ceramic"), (20, "pink"), 
    (30, "yellow"), (15, "pink")],
    10: [(1, "moab"), (10, "ceramic")]
}

class Coord(object): #MW: create a class containing waypoints for each map (waypoints tell the bloons what direction to face so they can follow the path of the map)

    #hardcoded waypoint values for map 1
    waypoints = { #MW: dictionary containing all waypoints for the first map, range is used to create a set of coordinates
    1: (range(173-3,173+4), "left"), #MW: for example, the first waypoint's x coordinate is within the range of 173-3 to 173+4 and the bloon should be facing left when its x coordinate is within that range (in game.py the x coordinate is compared to these values because going left is in the x direction)
    2: (range(616-3,616+4),"up"), #MW: in this gas, the second waypoint's y coordinate is within the range of 616-3 ot 616+4 and the bloon should be facing up when its y coordinate is within that range (in game.py the y coordinate is compared to these values because going up is in the y direction)
    3: (range(100-3,100+4), "left"),
    4: (range(92-3,92+4), "down"),
    5: (range(300-3,300+4), "right"),
    6: (range(200-3,200+4), "up"),
    7: (range(212-3,212+4), "right"),
    8: (range(299-3,299+4),"down"),
    9: (range(300-3,300+4), "right"),
    10: (range(400-3,400+4), "up"),
    11: (range(210-3,210+4), "right"),
    12: (range(502-3,502+4), "down"),
    13: (range(398-3,398+4), "right"),
    14: (range(620-3,620+4), "up"),
    15: (range(278-3,278+4), "right"),
    16: (range(742-3,742+4), "down"),
    17: (range(483-3,483+4), "left"),
    18: (range(379-3,379+4), "up"),
    19: (range(401-3,401+4), "left")}

    waypoints2 = { #MW: dictionary of waypoints for the second map
    1: (range(277-3, 277+4), "down"),
    2: (range(197-3, 197+4), "right"),
    3: (range(551-3, 551+4), "up"),
    4: (range(38-3, 38+4), "right"),
    5: (range(792-3, 792+4), "down"),
    6: (range(564-3, 564+4), "left"),
    7: (range(550-3, 550+4), "up"),
    8: (range(461-3, 461+4), "left"),
    9: (range(275-3, 275+4), "down"),
    10: (range(566-3, 566+4), "left"),
    11: (range(31-3, 31+4), "up"),
    12: (range(88-3, 88+4), "left")
    }

    #coordinates that monkeys can be placed in
    nonTrackValues = [ #MW: list of lists that contain coordinates that monkeys can be placed on in the first map
    ((0,0), (706,71)),
    ((774,0), (805,502)),
    ((0,71), (65,371)),
    ((122,137), (169,263)),
    ((171,133), (329,186)),
    ((331,131), (368,264)),
    ((232,246), (270,321)),
    ((369,131), (576,188)),
    ((530,188), (587,363)),
    ((433,250), (469,320)),
    ((637,68), (710,139)),
    ((590,200), (780,248)),
    ((652,321), (706,446)),
    ((477,423), (648,447)),
    ((59,329), (464,375)),
    ((408,374), (470,452)),
    ((322,511), (812,593)),
    ((310,459), (350,509)),
    ((0,429), (343,450))
    ]

    nonTrackValues2 = [ #MW: list of lists that contain coordinates that monkeys can be placed on in the second map
    ((58,61), (252,532)),
    ((58,61), (252,532)),
    ((199,224), (630,422)),
    ((579,61), (767,532)),
    ((301,488), (526,581))
    ]

    #coordinates that the boat can be placed in
    boatValues = [(0,458), (300,596)] #MW: list of lists that contain coordinates that the boat can be placed on in the first map

    boatValues2 = [(310,48), (514,165)] #MW: list of lists that contain coordinates that the boat can be placed on in the second map

    #music button coordinates
    music = [(917, 953), (536, 572)] #MW: list of lists that contain coordinates for the music button