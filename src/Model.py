#!/usr/bin/env python

import os
import json
import random
import uuid
import math
import numpy as np

# The model holds the state of the player, entities and game world. It has no methods at all, just data.


class Model(object):

    # The __init__ method is a special method called a constructor.
    # The first parameter 'self' is required by Python and refers to the object being created.
    def __init__(self):

        # initialise game state
        self.game_running = False
        self.game_victory = False
        self.game_demise = False
        # initial menu state
        self.menu_running = False
        self.action_menu_running = False
        self.status_screen_running = False

        # define path to assets
        root_path = os.path.dirname(os.path.realpath(__file__))
        self.entity_path = root_path + "/data/entities/"

        # define size of game world in cells
        self.max_x = 8
        self.max_y = 8

        # define player origin coordinate
        self.player_origin_x = 0
        self.player_origin_y = 7

        # define default cursor option height
        self.menu_option = 1

        # define dice values
        self.player_dice = 0
        self.player_dice_mod = 0
        self.mob_dice = 0
        self.mob_dice_mod = 0
        self.player_dice_mod_display = 0

        # the array M is going to hold the array information for each cell
        # the first four coordinates tell if walls exist on those sides
        # and the fifth indicates if the cell has been visited in the search
        # M(WEST, NORTH, EAST, SOUTH, CHECK_IF_VISITED)
        self.dungeon_map = np.zeros((self.max_y, self.max_x, 5), dtype=np.uint8)

        # set starting row and column
        x = 0
        y = 0
        history = [(y, x)]  # the history is the stack of visited locations

        # trace a path though the cells of the maze and open walls along the path
        # we do this with a while loop, repeating the loop until there is no history
        # which would mean we backtracked to the initial start
        while history:
            self.dungeon_map[y, x, 4] = 1  # designate this location as visited
            # check if the adjacent cells are valid for moving to
            check = []
            if x > 0 and self.dungeon_map[y, x - 1, 4] == 0:
                check.append('W')
            if y > 0 and self.dungeon_map[y - 1, x, 4] == 0:
                check.append('N')
            if x < self.max_x - 1 and self.dungeon_map[y, x + 1, 4] == 0:
                check.append('E')
            if y < self.max_y - 1 and self.dungeon_map[y + 1, x, 4] == 0:
                check.append('S')

            if len(check):  # if there is a valid cell to move to.
                # mark the walls between cells as open if we move
                history.append([y, x])
                move_direction = random.choice(check)
                if move_direction == 'W':
                    self.dungeon_map[y, x, 0] = 1
                    x -= 1
                    self.dungeon_map[y, x, 2] = 1
                if move_direction == 'N':
                    self.dungeon_map[y, x, 1] = 1
                    y -= 1
                    self.dungeon_map[y, x, 3] = 1
                if move_direction == 'E':
                    self.dungeon_map[y, x, 2] = 1
                    x += 1
                    self.dungeon_map[y, x, 0] = 1
                if move_direction == 'S':
                    self.dungeon_map[y, x, 3] = 1
                    y += 1
                    self.dungeon_map[y, x, 1] = 1
            else:  # if there are no valid cells to move to.
                # retrace one step back in history if no move is possible
                y, x = history.pop()

        # set visited back to false (except cell that the player originates from)
        for pos_x in range(0, self.max_x):
            for pos_y in range(0, self.max_y):
                self.dungeon_map[pos_y, pos_x, 4] = 0
        # set player origin coordinates to visited
                self.dungeon_map[self.player_origin_y, self.player_origin_x, 4] = 1

        # create player entity
        player_entity = {}
        for entity_filename in os.listdir(self.entity_path):
            # execute conditional block if a json file exists in the entities path and it is the player json
            if entity_filename.endswith(".json") and 'player' in entity_filename:
                # load the player json into a dictionary object
                player_entity = json.load(open(self.entity_path + entity_filename, 'r'))
                # change dictionary values according to entity type (player)
                player_entity["entity_id"] = uuid.uuid4()
                player_entity["skill"] = random.randint(1, 6) + 6
                player_entity["luck"] = random.randint(1, 6) + 6
                player_entity["stamina"] = random.randint(1, 6) + random.randint(1, 6) + 12
                player_entity["pos_x"] = self.player_origin_x
                player_entity["pos_y"] = self.player_origin_y
                player_entity["points"] = 0
                player_entity["status"] = ["standing"]
        self.entities = [player_entity]

        # create non-player entities
        # iterate through each file in the entities path
        for entity_filename in os.listdir(self.entity_path):
            # execute conditional block if a json file exists in the entities path and it is a mob or item json
            if entity_filename.endswith(".json"):
                # load the entity json into a dictionary object
                entity_dictionary = json.load(open(self.entity_path + entity_filename, 'r'))
                if entity_dictionary["entity_type"] == 'item' \
                        and entity_dictionary["entity_name"] == "ring_of_yendor":
                    entity = {"entity_name": entity_dictionary["entity_name"],
                              "entity_type": entity_dictionary["entity_type"],
                              "entity_image_vectors": entity_dictionary["entity_image_vectors"],
                              "entity_id": uuid.uuid4(), "skill": random.randint(1, 6) + 6,
                              "luck": random.randint(1, 6) + 6,
                              "stamina": random.randint(1, 6) + random.randint(1, 6) + 12,
                              "pos_x": random.randint(int(self.max_x/2), self.max_x - 1),
                              "pos_y": random.randint(0, int(self.max_y/2 - 1)),
                              "takeable": entity_dictionary["takeable"], "direction": entity_dictionary["direction"]}
                    finished = False
                    while not finished:
                        found = False
                        for other_entity in self.entities:
                            if other_entity["pos_x"] == entity["pos_x"] \
                                    and other_entity["pos_y"] == entity["pos_y"] \
                                    and other_entity["entity_type"] != 'wall':
                                found = True
                        if not found:
                            finished = True
                        else:
                            entity["pos_x"] = random.randint(0, self.max_x - 1)
                            entity["pos_y"] = random.randint(0, self.max_y - 1)
                    self.entities.append(entity)
                if entity_dictionary["entity_type"] == 'mob' \
                        or (entity_dictionary["entity_type"] == 'item'
                            and entity_dictionary["entity_name"] != "ring_of_yendor"):
                    max_encounter = int(math.floor(self.max_x * self.max_y) * 0.07)
                    for _ in range(0, max_encounter):
                        entity = {"entity_name": entity_dictionary["entity_name"],
                                  "entity_type": entity_dictionary["entity_type"],
                                  "entity_image_vectors": entity_dictionary["entity_image_vectors"],
                                  "entity_id": uuid.uuid4(),
                                  "skill": random.randint(1, 6) + 6,
                                  "luck": random.randint(1, 6) + 6,
                                  "stamina": random.randint(1, 6) + random.randint(1, 6) + 12,
                                  "pos_x": random.randint(0, self.max_x - 1),
                                  "pos_y": random.randint(0, self.max_y - 1),
                                  "takeable": entity_dictionary["takeable"],
                                  "direction": entity_dictionary["direction"]}
                        finished = False
                        while not finished:
                            found = False
                            for other_entity in self.entities:
                                if other_entity["pos_x"] == entity["pos_x"] \
                                        and other_entity["pos_y"] == entity["pos_y"] \
                                        and other_entity["entity_type"] != 'wall':
                                    found = True
                            if not found:
                                finished = True
                            else:
                                entity["pos_x"] = random.randint(0, self.max_x - 1)
                                entity["pos_y"] = random.randint(0, self.max_y - 1)
                        self.entities.append(entity)
