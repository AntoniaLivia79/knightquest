#!/usr/bin/env python

# The controller joins the model and the view together

import time
import pygame
from pygame.locals import *
import random


class Controller:

    def __init__(self):

        pass

    def move_player(self, model, move):

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj
                player_index = i

        player_pos_x = player_entity["pos_x"]
        player_pos_y = player_entity["pos_y"]

        model.player_dice = 0
        model.mob_dice = 0
        model.player_dice_mod_display = model.player_dice_mod

        if "engaged" not in player_entity["status"]:

            player_direction = player_entity["direction"]
            compass = [[3, 0, 1, 2], [0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 0, 1]]
            player_view = compass[player_direction]
            if move == 0:
                player_direction -= 1
                if player_direction < 0:
                    player_direction = 3
                player_entity["direction"] = player_direction
            if move == 1:
                if model.dungeon_map[player_pos_y, player_pos_x, player_view[1]] == 1:
                    if player_direction == 0:
                        player_pos_x -= 1
                    if player_direction == 1:
                        player_pos_y -= 1
                    if player_direction == 2:
                        player_pos_x += 1
                    if player_direction == 3:
                        player_pos_y += 1
                    model.dungeon_map[player_pos_y, player_pos_x, 4] = 1
            if move == 2:
                player_direction += 1
                if player_direction > 3:
                    player_direction = 0
                player_entity["direction"] = player_direction
            if move == 3:
                if model.dungeon_map[player_pos_y, player_pos_x, player_view[3]] == 1:
                    if player_direction == 0:
                        player_pos_x += 1
                    if player_direction == 1:
                        player_pos_y += 1
                    if player_direction == 2:
                        player_pos_x -= 1
                    if player_direction == 3:
                        player_pos_y -= 1
                    model.dungeon_map[player_pos_y, player_pos_x, 4] = 1

            player_entity["pos_x"] = player_pos_x
            player_entity["pos_y"] = player_pos_y

            for entity in model.entities:
                if entity["entity_type"] == "mob":
                    if entity["pos_x"] == player_pos_x and entity["pos_y"] == player_pos_y:
                        player_status = player_entity["status"]
                        if "engaged" not in player_status:
                            player_status.append("engaged")
                        player_entity["status"] = player_status
                        model.entities.pop(player_index)
                        model.entities.append(player_entity)

            model.entities.pop(player_index)
            model.entities.append(player_entity)

        else:
            if move == 1:
                self.player_fight(model)

    @staticmethod
    def move_cursor(model, move):
        option_position = model.menu_option
        if move == 1:
            option_position -= 1
            if option_position < 1:
                if not model.action_menu_running:
                    option_position = 4
                else:
                    option_position = 5
        if move == 3:
            option_position += 1
            if option_position > 4 and not model.action_menu_running:
                option_position = 1
            elif option_position > 5 and model.action_menu_running:
                option_position = 1
        model.menu_option = option_position

    def read_menu(self, model):

        model.player_dice = 0
        model.mob_dice = 0
        model.player_dice_mod_display = model.player_dice_mod

        if not model.menu_running:
            model.menu_running = True
            model.menu_option = 1
        else:
            if model.menu_option == 5:
                if model.action_menu_running:
                    model.action_menu_running = False
                    model.menu_option = 1
            else:
                if model.menu_option == 4:
                    if not model.action_menu_running:
                        model.menu_running = False
                    else:
                        self.player_luck(model)
                else:
                    if model.menu_option == 1:
                        if not model.action_menu_running:
                            model.action_menu_running = True
                        else:
                            self.player_fight(model)
                    else:
                        if model.menu_option == 2:
                            if not model.action_menu_running:
                                if model.status_screen_running:
                                    model.status_screen_running = False
                                else:
                                    model.status_screen_running = True
                            else:
                                self.player_flee(model)
                        else:
                            if model.menu_option == 3:
                                if not model.action_menu_running:
                                    self.player_save(model)
                                else:
                                    self.player_interact(model)

    @staticmethod
    def player_fight(model):

        model.menu_running = False
        model.action_menu_running = False
        model.player_dice_mod_display = model.player_dice_mod

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj
                player_index = i
                player_pos_x = player_entity["pos_x"]
                player_pos_y = player_entity["pos_y"]
                player_skill = player_entity["skill"]
                player_stamina = player_entity["stamina"]
                player_points = player_entity["points"]
                player_status = player_entity["status"]

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'mob':
                if entity_obj["pos_x"] == player_pos_x and entity_obj["pos_y"] == player_pos_y:
                    mob_entity = entity_obj
                    mob_skill = mob_entity["skill"]
                    mob_stamina = mob_entity["stamina"]
                    mob_index = i

                    model.mob_dice = random.randint(1, 6)
                    mob_roll = model.mob_dice + mob_skill
                    model.player_dice = random.randint(1, 6)
                    player_roll = model.player_dice + player_skill + model.player_dice_mod

                    if mob_roll > player_roll:
                        damage = mob_roll - player_roll
                        if damage >= player_stamina:
                            model.game_demise = True
                            model.game_running = False
                        else:
                            player_stamina -= damage

                    if mob_roll < player_roll:
                        model.entities.pop(mob_index)
                        damage = player_roll - mob_roll
                        if damage < mob_stamina:
                            mob_stamina -= damage
                            mob_entity["stamina"] = mob_stamina
                            model.entities.append(mob_entity)
                        else:
                            if (player_points < 24 <= player_points + mob_skill) \
                                    or (player_points < 48 <= player_points + mob_skill) \
                                    or (player_points < 72 <= player_points + mob_skill) \
                                    or (player_points < 96 <= player_points + mob_skill):
                                player_skill += 1
                            player_points += mob_skill
                            player_status.remove("engaged")

                    for player_i, player_obj in enumerate(model.entities):
                        if player_obj["entity_type"] == 'pc':
                            player_index = player_i

                    if "lucky" in player_status:
                        player_status.remove("lucky")
                        if model.player_dice_mod > 0:
                            model.player_dice_mod = model.player_dice_mod - 1

                    player_entity["skill"] = player_skill
                    player_entity["status"] = player_status
                    player_entity["stamina"] = player_stamina
                    player_entity["points"] = player_points
                    model.entities.pop(player_index)
                    model.entities.append(player_entity)

    @staticmethod
    def player_interact(model):

        model.menu_running = False
        model.action_menu_running = False
        model.player_dice = 0
        model.mob_dice = 0
        model.player_dice_mod_display = model.player_dice_mod

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj

        player_pos_x = player_entity["pos_x"]
        player_pos_y = player_entity["pos_y"]
        player_points = player_entity["points"]
        player_skill = player_entity["skill"]

        for i, entity_obj in enumerate(model.entities):
            entity_index = i
            if entity_obj["entity_name"] == "ring_of_yendor":
                if entity_obj["pos_x"] == player_pos_x and entity_obj["pos_y"] == player_pos_y:
                    player_points += 50
                    if (player_points < 24 <= player_points + 50) \
                            or (player_points < 48 <= player_points + 50) \
                            or (player_points < 72 <= player_points + 50) \
                            or (player_points < 96 <= player_points + 50):
                        player_skill += 1
                    player_entity["skill"] = player_skill
                    player_entity["points"] = player_points
                    model.game_victory = True
                    model.game_running = False
            if entity_obj["entity_name"] == "herb":
                if entity_obj["pos_x"] == player_pos_x and entity_obj["pos_y"] == player_pos_y:
                    player_stamina = player_entity["stamina"]
                    player_stamina += random.randint(1, 6)
                    player_entity["stamina"] = player_stamina
                    if (player_points < 24 <= player_points + 1) \
                            or (player_points < 48 <= player_points + 1) \
                            or (player_points < 72 <= player_points + 1) \
                            or (player_points < 96 <= player_points + 1):
                        player_skill += 1
                    player_points += 1
                    player_entity["skill"] = player_skill
                    player_entity["points"] = player_points
                    model.entities.pop(entity_index)
            if entity_obj["entity_name"] == "potion":
                if entity_obj["pos_x"] == player_pos_x and entity_obj["pos_y"] == player_pos_y:
                    player_luck = player_entity["luck"]
                    player_luck += random.randint(1, 6)
                    player_entity["luck"] = player_luck
                    if (player_points < 24 <= player_points + 1) \
                            or (player_points < 48 <= player_points + 1) \
                            or (player_points < 72 <= player_points + 1) \
                            or (player_points < 96 <= player_points + 1):
                        player_skill += 1
                    player_points += 1
                    player_entity["skill"] = player_skill
                    player_entity["points"] = player_points
                    model.entities.pop(entity_index)
            if entity_obj["entity_name"] == "well":
                if entity_obj["pos_x"] == player_pos_x and entity_obj["pos_y"] == player_pos_y:
                    skill_roll = random.randint(1, 6)
                    if skill_roll < 5:
                        player_skill += 1
                    elif player_skill > 1:
                        player_skill -= 1
                    if (player_points < 24 <= player_points + skill_roll) \
                            or (player_points < 48 <= player_points + skill_roll) \
                            or (player_points < 72 <= player_points + skill_roll) \
                            or (player_points < 96 <= player_points + skill_roll):
                        player_skill += 1
                    player_points += skill_roll
                    player_entity["skill"] = player_skill
                    player_entity["points"] = player_points

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'pc':
                player_index = i
                model.entities.pop(player_index)
                model.entities.append(player_entity)

    @staticmethod
    def player_luck(model):

        model.menu_running = False
        model.action_menu_running = False
        model.player_dice = 0
        model.mob_dice = 0

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj
                player_index = i
                player_status = player_entity["status"]
                player_luck = player_entity["luck"]
                if "lucky" not in player_status and player_luck > 0:
                    player_luck = player_luck - 1
                    model.player_dice_mod = model.player_dice_mod + 1
                    player_status.append("lucky")
                    player_entity["luck"] = player_luck
                    player_entity["status"] = player_status
                    model.entities.pop(player_index)
                    model.entities.append(player_entity)

        model.player_dice_mod_display = model.player_dice_mod

    @staticmethod
    def player_flee(model):

        model.menu_running = False
        model.action_menu_running = False

        for i, entity_obj in enumerate(model.entities):
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj
                player_index = i
                player_status = player_entity["status"]
                player_luck = player_entity["luck"]
                if "engaged" in player_status and player_luck > 0:
                    player_luck = player_luck - 1
                    player_status.remove("engaged")
                    player_entity["luck"] = player_luck
                    player_entity["status"] = player_status
                    model.entities.pop(player_index)
                    model.entities.append(player_entity)
                    
    @staticmethod
    def player_save(model):
        model.game_running = False

    # change game state to running (arg: A=START)
    @staticmethod
    def start(model):

        # detect input
        btn_released = False
        while not btn_released:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    model.game_running = True
                    btn_released = True

    # move player (arg: 0=TURN L,1=FORWARD,2=TURN R,3=BACK)
    def update(self, model):

        btn_released = False
        while not btn_released:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if model.menu_running:
                            self.move_cursor(model, 1)
                        else:
                            self.move_player(model, 1)
                        btn_released = True
                    if event.key == K_LEFT:
                        self.move_player(model, 0)
                        btn_released = True
                    if event.key == K_RIGHT:
                        self.move_player(model, 2)
                        btn_released = True
                    if event.key == K_DOWN:
                        if model.menu_running:
                            self.move_cursor(model, 3)
                        else:
                            self.move_player(model, 3)
                        btn_released = True
                    if event.key == K_SPACE or event.key == K_RETURN:
                        self.read_menu(model)
                        btn_released = True

                time.sleep(.05)
