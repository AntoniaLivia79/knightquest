#!/usr/bin/env python

import pygame
import pygame.surfarray as surfarray
import numpy as np
import os
import json
import Config as Config

# The view displays the game interface on the screen. It does not alter the dungeon_map; it just
# reads the data from the dungeon_map and decides what to display based upon the state of the
# dungeon_map.


class View:

    # The __init__ method is a special method called a constructor. The first parameter
    # 'self' is required by Python and refers to the object being created.
    def __init__(self):

        # configure font
        self.font_size = Config.font_size * Config.hud_scale
        # configure text
        self.text_indent = Config.text_indent * Config.hud_scale
        self.text_intro_header_indent = Config.text_intro_header_indent * Config.hud_scale
        self.text_intro_footer_indent = Config.text_intro_footer_indent * Config.hud_scale
        self.text_end_header_indent = Config.text_end_header_indent * Config.hud_scale
        self.text_end_footer_indent = Config.text_end_footer_indent * Config.hud_scale
        self.text_stats_header_indent = Config.text_stats_header_indent * Config.hud_scale
        self.text_entity_footer_indent = Config.text_entity_footer_indent * Config.hud_scale
        self.text_option_indent = Config.text_option_indent * Config.hud_scale
        # configure menu
        self.cursor_width = Config.cursor_width * Config.hud_scale
        self.cursor_height = Config.cursor_height * Config.hud_scale
        self.cursor_radius = Config.cursor_radius * Config.hud_scale
        # configure display
        self.display_width = Config.display_width * Config.hud_scale
        self.display_height = Config.display_height * Config.hud_scale
        # configure palette
        self.gamepalette = Config.gamepalette
        self.uipalette = Config.uipalette
        self.entitypalette = Config.entitypalette
        self.mobpalette = Config.mobpalette
        self.itempalette = Config.itempalette
        # configure hud
        self.front_entity_width = Config.front_entity_width * Config.hud_scale
        self.front_entity_height = Config.front_entity_height * Config.hud_scale
        self.left_entity_width = Config.left_entity_width * Config.hud_scale
        self.left_entity_height = Config.left_entity_height * Config.hud_scale
        self.right_entity_width = Config.right_entity_width * Config.hud_scale
        self.right_entity_height = Config.right_entity_height * Config.hud_scale
        self.text_header_height = Config.text_header_height * Config.hud_scale
        self.text_footer_height = Config.text_footer_height * Config.hud_scale
        self.text_option_height = Config.text_option_height * Config.hud_scale
        self.cursor_width = Config.cursor_width * Config.hud_scale
        self.cursor_radius = Config.cursor_radius * Config.hud_scale
        self.vector_scale = Config.vector_scale * Config.hud_scale
        self.map_width = Config.map_width * Config.hud_scale
        self.map_height = Config.map_height * Config.hud_scale
        self.compass_width = Config.compass_width * Config.hud_scale
        self.compass_height = Config.compass_height * Config.hud_scale
        self.compass_bearing_list = Config.compass_bearing_list * Config.hud_scale
        self.left_dice_width = Config.left_dice_width * Config.hud_scale
        self.right_dice_width = Config.right_dice_width * Config.hud_scale
        self.player_dice_height = Config.player_dice_height * Config.hud_scale
        self.mob_dice_height = Config.mob_dice_height * Config.hud_scale
        # initialise pygame instance
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('KNIGHTQUEST')
        # define path to data
        root_path = os.path.dirname(os.path.realpath(__file__))
        self.entity_path = root_path + "/data/entities/"
        # initialise pygame font
        pygame.font.init()
        self.gamefont = pygame.font.Font(root_path + "/assets/font/BlackPearl.ttf", self.font_size)
        # initialise data structures
        self.vector_pnt_tuple = ()
        self.vector_pnt_tuple_list = []
        self.dictionary_list = []
        # initialise pygame display
        self.gamescreen = None
        self.gamescreen = pygame.display.set_mode((self.display_width, self.display_height))
        # initialise menu cursor
        self.cursor_height = self.font_size - (self.cursor_radius * 2)

        pass

    # extract dict list from a json in a path which match a key
    def load_dictionary_list(self, document_path, document, document_key):

        # load the json into a dictionary object
        dictionary = json.load(open(document_path + document, 'r'))
        # load the list of dictionaries from the json dictionary object
        self.dictionary_list = dictionary[document_key]

    # convert list of vector point dicts into tuple of coordinates
    def vector_entity_tuples(self,
                             entity_image_vector_list,
                             elevation):

        # load the initial point A dict        ionary with x and y attributes
        entity_image_vector_pnt_a = entity_image_vector_list[0]
        # load the terminal point B dictionary with x and y attributes
        entity_image_vector_pnt_b = entity_image_vector_list[1]
        # load the x and y attributes for initial point A and terminal point B, offset according to elevation
        if elevation == 'left':
            init_pnt_a_x = (entity_image_vector_pnt_a["x"] * self.vector_scale) + self.left_entity_width
            init_pnt_a_y = (entity_image_vector_pnt_a["y"] * self.vector_scale) + self.left_entity_height
            term_pnt_b_x = (entity_image_vector_pnt_b["x"] * self.vector_scale) + self.left_entity_width
            term_pnt_b_y = (entity_image_vector_pnt_b["y"] * self.vector_scale) + self.left_entity_height
        else:
            if elevation == 'right':
                init_pnt_a_x = (entity_image_vector_pnt_a["x"] * self.vector_scale) + self.right_entity_width
                init_pnt_a_y = (entity_image_vector_pnt_a["y"] * self.vector_scale) + self.right_entity_height
                term_pnt_b_x = (entity_image_vector_pnt_b["x"] * self.vector_scale) + self.right_entity_width
                term_pnt_b_y = (entity_image_vector_pnt_b["y"] * self.vector_scale) + self.right_entity_height
            else:
                init_pnt_a_x = (entity_image_vector_pnt_a["x"] * self.vector_scale) + self.front_entity_width
                init_pnt_a_y = (entity_image_vector_pnt_a["y"] * self.vector_scale) + self.front_entity_height
                term_pnt_b_x = (entity_image_vector_pnt_b["x"] * self.vector_scale) + self.front_entity_width
                term_pnt_b_y = (entity_image_vector_pnt_b["y"] * self.vector_scale) + self.front_entity_height
        # populate a list of vector points
        self.vector_pnt_tuple = (init_pnt_a_x, init_pnt_a_y, term_pnt_b_x, term_pnt_b_y)

    # display player stats in the header of the game screen
    def draw_player_stats(self, skill, stamina, luck):

        self.draw_text('SKL ' + str(skill) + ' STM ' + str(stamina) + ' LCK ' + str(luck),
                       'header',
                       self.text_stats_header_indent + self.text_indent)

    # draw player dice in bottom right of display
    def draw_player_dice(self, left_dice, right_dice):

        self.draw_text(str(left_dice) + ' + ', 'player_dice', self.left_dice_width)
        self.draw_text(str(right_dice), 'player_dice_mod', self.right_dice_width)

    # draw mob dice in top right of display
    def draw_mob_dice(self, left_dice, right_dice):
        self.draw_text(str(left_dice) + ' + ', 'mob_dice', self.left_dice_width)
        self.draw_text(str(right_dice), 'mob_dice_mod', self.right_dice_width)

    # draw entities in same coordinate as player
    def draw_entities(self, entities, left_dice, right_dice, pos_x, pos_y):

        for entity in entities:
            if entity["entity_type"] == 'item' or entity["entity_type"] == 'mob':
                if entity["pos_x"] == pos_x and entity["pos_y"] == pos_y:
                    self.draw_entity(entity["entity_name"], entity["entity_type"], 'front', self.gamescreen)
                    entity_name = str(entity["entity_name"])
                    entity_name = entity_name.replace("_", " ")
                    entity_name = entity_name.title()
                    if entity["entity_type"] == 'item':
                        self.draw_text(entity_name, 'footer', self.text_entity_footer_indent + self.text_indent)
                    else:
                        self.draw_text(entity_name + ' SKL ' + str(entity["skill"]) + ' STM ' + str(entity["stamina"]),
                                       'footer',
                                       self.text_entity_footer_indent + self.text_indent)
                        self.draw_mob_dice(left_dice, right_dice)

    # function to draw walls to front, left and right of player
    def draw_walls(self, dungeon_map, pos_x, pos_y, direction, entities):

        compass = [[3, 0, 1], [0, 1, 2], [1, 2, 3], [2, 3, 0]]
        player_view = compass[direction]
        blocked = False
        # draw walls based on player facing direction and coordinates
        
        if dungeon_map[pos_y, pos_x, player_view[0]] == 1:
            self.draw_entity('wall_left_open', 'wall', 'left', self.gamescreen)
        else:
            self.draw_entity('wall_left_closed', 'wall', 'left', self.gamescreen)
        if dungeon_map[pos_y, pos_x, player_view[1]] == 1:
            for entity in entities:
                if entity["entity_type"] == 'mob' and entity["pos_x"] == pos_x and entity["pos_y"] == pos_y:
                    blocked = True
            if not blocked:
                self.draw_entity('wall_front_open', 'wall', 'front', self.gamescreen)
        else:
            for entity in entities:
                if entity["entity_type"] == 'mob' and entity["pos_x"] == pos_x and entity["pos_y"] == pos_y:
                    blocked = True
            if not blocked:
                self.draw_entity('wall_front_closed', 'wall', 'front', self.gamescreen)
        if dungeon_map[pos_y, pos_x, player_view[2]] == 1:
            self.draw_entity('wall_right_open', 'wall', 'right', self.gamescreen)
        else:
            self.draw_entity('wall_right_closed', 'wall', 'right', self.gamescreen)

    def post_process_view(self):

        # apply post processing to gamescreen canvas
        rgbarray = surfarray.array3d(self.gamescreen)
        factor = np.array((8,), np.int32)
        soften = np.array(rgbarray, np.int32)
        soften[1:, :] += rgbarray[:-1, :] * factor
        soften[:-1, :] += rgbarray[1:, :] * factor
        soften[:, 1:] += rgbarray[:, :-1] * factor
        soften[:, :-1] += rgbarray[:, 1:] * factor
        soften //= 36
        screen = pygame.display.set_mode(soften.
                                         shape[:2], 0, 32)
        surfarray.blit_array(screen, soften)

    def draw_entity(self, entity_name, entity_type, elevation, surface):
        # initialise entity vector point list
        self.vector_pnt_tuple_list = []
        # iterate through each file in the entities path
        for entity_filename in os.listdir(self.entity_path):
            # execute conditional block if a json file exists in the entities path and it matches the argument name
            if entity_filename.endswith(".json") and entity_name in entity_filename:
                # load the image vectors from the entity dictionary object into a list of vectors
                self.load_dictionary_list(self.entity_path, entity_filename, "entity_image_vectors")
                # iterate through the list of vectors
                for entity_image_vector in self.dictionary_list:
                    # draw a line between the initial point A vector tuple and the terminal point B vector tuple
                    self.vector_entity_tuples(entity_image_vector, elevation)
                    self.vector_pnt_tuple_list.append(self.vector_pnt_tuple)

        if entity_type == 'item':
            draw_palette = self.itempalette
        elif entity_type == 'mob':
            draw_palette = self.mobpalette
        else:
            draw_palette = self.entitypalette

        for vector_pnt in self.vector_pnt_tuple_list:
            pygame.draw.line(surface,
                             draw_palette,
                             (vector_pnt[0],
                              vector_pnt[1]),
                             (vector_pnt[2],
                              vector_pnt[3]),
                             4)

    # clear the wall view
    def clear_walls(self):

        # Draw a black filled box to clear the image.
        self.gamescreen.fill((0, 0, 0))
        pygame.display.flip()

    # push text to display (text, header/ footer, indent)
    def draw_text(self, text_string, caption_position, text_indent):

        text_surface = self.gamefont.render(text_string, False, self.gamepalette)
        if caption_position == 'header':
            self.gamescreen.blit(text_surface, (text_indent, self.text_header_height))
        elif caption_position == 'footer':
            self.gamescreen.blit(text_surface, (text_indent, self.text_footer_height))
        elif caption_position == 'player_dice':
            self.gamescreen.blit(text_surface, (text_indent, self.player_dice_height))
        elif caption_position == 'player_dice_mod':
            self.gamescreen.blit(text_surface, (text_indent, self.player_dice_height))
        elif caption_position == 'mob_dice':
            self.gamescreen.blit(text_surface, (text_indent, self.mob_dice_height))
        elif caption_position == 'mob_dice_mod':
            self.gamescreen.blit(text_surface, (text_indent, self.mob_dice_height))
        elif caption_position.isdigit():
            self.gamescreen.blit(text_surface, (text_indent, self.text_option_height
                                                + ((int(caption_position) - 1) * self.font_size)))

    # draw map on left of game screen of player
    def draw_map(self, pos_x, pos_y, dungeon_map, model):
        player_pos_x = (pos_x * (Config.hud_scale * 8)) + self.map_width
        player_pos_y = (pos_y * (Config.hud_scale * 8)) + self.map_height
        # draw all visited dungeon cells
        for pos_x in range(0, model.max_x):
            for pos_y in range(0, model.max_y):
                map_pos_x = (pos_x * (Config.hud_scale * 8)) + self.map_width
                map_pos_y = (pos_y * (Config.hud_scale * 8)) + self.map_height
                if dungeon_map[pos_y, pos_x, 4] == 1:
                    pygame.draw.rect(self.gamescreen, self.uipalette,
                                     (map_pos_x + 1, map_pos_y + 1, (Config.hud_scale * 4), (Config.hud_scale * 4)))
        # draw player
        pygame.draw.rect(self.gamescreen, self.gamepalette,
                                     (player_pos_x + 1, player_pos_y + 1, (Config.hud_scale * 4), (Config.hud_scale * 4)))

    # draw cursor on menu_screen
    def draw_cursor(self, option_height):

        pygame.draw.circle(self.gamescreen,
                           self.uipalette,
                           (self.cursor_width, self.cursor_height
                            + (int(option_height - 1) * (self.font_size + Config.hud_scale)) + (self.font_size / 2) + self.cursor_radius),
                           self.cursor_radius,
                           0)

    # draw compass on right of game screen of player
    def draw_compass(self, direction):

        compass_arrow = self.gamefont.render("^", True, self.uipalette)
        compass_bearing = self.compass_bearing_list[direction]
        compass_text = pygame.transform.rotate(compass_arrow, compass_bearing['angle'])
        self.gamescreen.blit(compass_text, [self.compass_width + compass_bearing['width_offset'],
                                            self.compass_height + compass_bearing['height_offset']])

    # draw the game introduction
    def draw_intro(self):

        self.draw_text('KNIGHTQUEST', 'header', self.text_intro_header_indent + self.text_indent)
        self.draw_text('Find Ring Of Yendor', 'footer', self.text_intro_footer_indent + self.text_indent)
        self.draw_entity('kobold', 'mob', 'front', self.gamescreen)
        self.draw_entity('wall_left_closed', 'wall', 'left', self.gamescreen)
        self.draw_entity('wall_right_closed', 'wall', 'right', self.gamescreen)

        # render screen
        pygame.display.flip()

    # draw the game finale
    def draw_end(self, model):

        self.clear_walls()
        for entity_obj in model.entities:
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj
        self.draw_text('  YOU HAVE WON !', 'header', self.text_end_header_indent + self.text_indent)
        self.draw_text('Score: ' + str(player_entity["points"]), 'footer', self.text_end_footer_indent
                       + self.text_indent)
        self.draw_entity('ring_of_yendor', 'item', 'front', self.gamescreen)
        self.draw_entity('wall_left_closed', 'wall', 'left', self.gamescreen)
        self.draw_entity('wall_right_closed', 'wall', 'right', self.gamescreen)

        # render screen
        pygame.display.flip()

    # draw the game demise
    def draw_demise(self, model):

        self.clear_walls()

        for entity_obj in model.entities:
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj
        self.draw_text('  YOU HAVE DIED !', 'header', self.text_end_header_indent + self.text_indent)
        self.draw_text('Score: ' + str(player_entity["points"]), 'footer', self.text_end_footer_indent + self.text_indent)
        self.draw_entity('wall_left_closed', 'wall', 'left', self.gamescreen)
        self.draw_entity('wall_right_closed', 'wall', 'right', self.gamescreen)

        # render screen
        pygame.display.flip()

    # display player status
    def draw_status(self, model):

        for entity_obj in model.entities:
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj

        self.clear_walls()

        def filter_status(status):
            if "standing" in status:
                return False
            else:
                return True

        status_list = filter(filter_status, player_entity["status"])

        self.draw_text(', '.join(status_list), '1', self.text_indent + self.text_option_indent)

        # render screen
        pygame.display.flip()

    # display_game_menu
    def draw_menu(self, model):

        self.clear_walls()

        if not model.action_menu_running:
            self.draw_text('Action', '1', self.text_indent + self.text_option_indent)
            self.draw_text('Status', '2', self.text_indent + self.text_option_indent)
            self.draw_text('Exit', '3', self.text_indent + self.text_option_indent)
            self.draw_text('Back', '4', self.text_indent + self.text_option_indent)
        else:
            self.clear_walls()
            self.draw_text('Fight', '1', self.text_indent + self.text_option_indent)
            self.draw_text('Flee', '2', self.text_indent + self.text_option_indent)
            self.draw_text('Interact', '3', self.text_indent + self.text_option_indent)
            self.draw_text('Try Luck', '4', self.text_indent + self.text_option_indent)
            self.draw_text('Back', '5', self.text_indent + self.text_option_indent)

        self.draw_cursor(model.menu_option)
        # render screen
        pygame.display.flip()

    # draw all features on display canvas
    def draw_view(self, model):

        for entity_obj in model.entities:
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj

        self.clear_walls()

        for entity_obj in model.entities:
            if entity_obj["entity_type"] == 'pc':
                player_entity = entity_obj

        # draw walls based on player facing direction and coordinates
        self.draw_walls(model.dungeon_map,
                        player_entity["pos_x"],
                        player_entity["pos_y"],
                        player_entity["direction"],
                        model.entities)
        # draw entities
        self.draw_entities(model.entities,
                           model.mob_dice,
                           model.mob_dice_mod,
                           player_entity["pos_x"],
                           player_entity["pos_y"])
        # draw player stats
        self.draw_player_stats(player_entity["skill"],
                               player_entity["stamina"],
                               player_entity["luck"])
        # draw dice values
        self.draw_player_dice(model.player_dice, model.player_dice_mod_display)
        # draw map based on player coordinates
        self.draw_map(player_entity["pos_x"],
                      player_entity["pos_y"],
                      model.dungeon_map,
                      model)
        # draw compass based on player facing direction
        self.draw_compass(player_entity["direction"])

        # render screen
        pygame.display.flip()

        self.clock.tick(60)
