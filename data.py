from player import Player

player = Player()

towerTypes = {
    #cooldown in seconds, range is radius around monkey
    "dartmonkey": 
        {
        "price": 250, 
        "upgrade_price": 200,
        "cooldown": 0.7, 
        "damage": 1, 
        "slow": 0, 
        "range": 125,
        "bullet": "basketball",
        "description": "Cheap starting tower"
        },
    "ninjamonkey": 
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
    "boat": 
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
    "sniper": 
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
    "gluegunner": 
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
    "supermonkey": 
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
    "dartmonkey_upgraded": 
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
    "ninjamonkey_upgraded": 
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
    "boat_upgraded": 
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
    "sniper_upgraded":
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
    "gluegunner_upgraded": 
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
    "supermonkey_upgraded": 
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

bloons = {
    #strength correlates with required number of hits to be killed
    "red":
        {
        "strength": 1,
        "speed": 2,
        },
    "blue":
        {
        "strength": 2,
        "speed": 3,
        },
    "green":
        {
        "strength": 3,
        "speed": 4,
        },
    "yellow":
        {
        "strength": 4,
        "speed": 5,
        },
    "pink":
        {
        "strength": 5,
        "speed": 6,
        },
    "ceramic":
        {
        "strength": 20,
        "speed": 4,
        },
    "moab":
        {
        "strength": 350,
        "speed": 1,
        },
}

bloonColors = {
    1: "red", 
    2: "blue", 
    3: "green",
    4: "yellow", 
    5: "pink"
}

levels = {
    0: [],
    1: [(30,"red"), (10, "blue")], 
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

class Coord(object):

    #hardcoded waypoint values for map 1
    waypoints = {
    1: (range(173-3,173+4), "left"), 
    2: (range(616-3,616+4),"up"), 
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

    waypoints2 = {
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
    nonTrackValues = [
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

    nonTrackValues2 = [
    ((58,61), (252,532)),
    ((58,61), (252,532)),
    ((199,224), (630,422)),
    ((579,61), (767,532)),
    ((301,488), (526,581))
    ]

    #coordinates that the boat can be placed in
    boatValues = [(0,458), (300,596)]

    boatValues2 = [(310,48), (514,165)]

    #music button coordinates
    music = [(917, 953), (536, 572)]