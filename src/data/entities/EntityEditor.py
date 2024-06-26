import pygame
import json
import sys
from maison import ProjectConfig

def is_close_to_any(coord, coord_list, tolerance=5):
    for c in coord_list:
        if abs(c[0] - coord[0]) <= tolerance and abs(c[1] - coord[1]) <= tolerance:
            return [True, c]
    return [False, (0, 0)]

def import_from_json(entity_file_path):
    try:
        with open(entity_file_path, 'r') as json_file:
            json_data = json.load(json_file)
            return json_data
    except FileNotFoundError:
        print(f"Error: File not found at '{entity_file_path}'")
        sys.exit(1)
    except json.decoder.JSONDecodeError:
        print(f"Error: File at '{entity_file_path}' is not a valid JSON file")
        sys.exit(1)  

def export_to_json(entityname, entitytype, takeable, skill, stamina, luck,
                   lines):
    json_data = {
        "entity_name": entityname,
        "entity_type": entitytype,
        "entity_image_vectors": [
            [{'x': int(src[0] / 50) - 1, 'y': int(src[1] / 50) - 1},
             {'x': int(dest[0] / 50) - 1, 'y': int(dest[1] / 50) - 1}] for src, dest in lines
        ],
        "entity_id": "none",
        "takeable": takeable,
        "skill": int(skill),
        "stamina": int(stamina),
        "luck": int(luck),
        "pos_x": 0,
        "pos_y": 0,
        "direction": 2
    }
    filename = entityname + '.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)


def draw_interface(window, font, entity_name_text, entity_name_input_rect, color_active, color_passive,
                   entity_type_menu_rect, entity_type_options, takeable_menu_rect, takeable_options,
                   skill_input_rect, skill_text, stamina_input_rect, stamina_text,
                   luck_input_rect, luck_text):

    global entity_name_input_active, entity_type_menu_expanded, entity_type_selected_option, \
        takeable_menu_expanded, takeable_selected_option, skill_input_active, stamina_input_active, luck_input_active
    
    window.fill((0, 0, 0))  # Fill screen with black
    
    pygame.draw.rect(window, color_active if entity_name_input_active else color_passive, entity_name_input_rect)
    text_surface = font.render(entity_name_text, True, (0, 0, 0))
    window.blit(text_surface, (entity_name_input_rect.x + 5, entity_name_input_rect.y + 5))
    entity_name_input_rect.w = max(140, text_surface.get_width() + 10)

    pygame.draw.rect(window, color_active if skill_input_active else color_passive, skill_input_rect)    
    text_surface = font.render(skill_text, True, (0, 0, 0))
    window.blit(text_surface, (skill_input_rect.x + 5, skill_input_rect.y + 5))
    skill_input_rect.w = max(140, text_surface.get_width() + 10)
            
    pygame.draw.rect(window, color_active if stamina_input_active else color_passive, stamina_input_rect)
    text_surface = font.render(stamina_text, True, (0, 0, 0))
    window.blit(text_surface, (stamina_input_rect.x + 5, stamina_input_rect.y + 5))
    stamina_input_rect.w = max(140, text_surface.get_width() + 10)

    pygame.draw.rect(window, color_active if luck_input_active else color_passive, luck_input_rect)
    text_surface = font.render(luck_text, True, (0, 0, 0))
    window.blit(text_surface, (luck_input_rect.x + 5, luck_input_rect.y + 5))
    luck_input_rect.w = max(140, text_surface.get_width() + 10)

    entity_name_text_label = font.render('Entity Name:', True, (0, 0, 255), (0, 0, 0))
    entity_name_text_label_rect = entity_name_text_label.get_rect()
    entity_name_text_label_rect.x = 550
    entity_name_text_label_rect.y = 33
    window.blit(entity_name_text_label, entity_name_text_label_rect)

    entity_type_text_label = font.render('Entity Type:', True, (0, 0, 255), (0, 0, 0))
    entity_type_text_label_rect = entity_type_text_label.get_rect()
    entity_type_text_label_rect.x = 550
    entity_type_text_label_rect.y = 115
    window.blit(entity_type_text_label, entity_type_text_label_rect)

    takeable_text_label = font.render('Takeable:', True, (0, 0, 255), (0, 0, 0))
    takeable_text_label_rect = takeable_text_label.get_rect()
    takeable_text_label_rect.x = 550
    takeable_text_label_rect.y = 240
    window.blit(takeable_text_label, takeable_text_label_rect)

    skill_text_label = font.render('Skill:', True, (0, 0, 255), (0, 0, 0))
    skill_text_label_rect = skill_text_label.get_rect()
    skill_text_label_rect.x = 550
    skill_text_label_rect.y = 320
    window.blit(skill_text_label, skill_text_label_rect)

    stamina_text_label = font.render('Stamina:', True, (0, 0, 255), (0, 0, 0))
    stamina_text_label_rect = stamina_text_label.get_rect()
    stamina_text_label_rect.x = 550
    stamina_text_label_rect.y = 400
    window.blit(stamina_text_label, stamina_text_label_rect)

    Luck_text_label = font.render('Luck:', True, (0, 0, 255), (0, 0, 0))
    Luck_text_label_rect = Luck_text_label.get_rect()
    Luck_text_label_rect.x = 550
    Luck_text_label_rect.y = 480
    window.blit(Luck_text_label, Luck_text_label_rect)

    # Draw entity type drop-down menu
    pygame.draw.rect(window, color_active if entity_type_menu_expanded else color_passive, entity_type_menu_rect)
    pygame.draw.rect(window, (0, 255, 0), entity_type_menu_rect, 2)
    menu_text = font.render(entity_type_selected_option, True, (0, 0, 255))
    window.blit(menu_text, (entity_type_menu_rect.x + 10, entity_type_menu_rect.y + 10))

    if entity_type_menu_expanded:
        for i, option in enumerate(entity_type_options):
            option_rect = pygame.Rect(entity_type_menu_rect.x,
                                      entity_type_menu_rect.y + entity_type_menu_rect.height * (i + 1),
                                      entity_type_menu_rect.width, entity_type_menu_rect.height)
            pygame.draw.rect(window, (0, 0, 0), option_rect)
            pygame.draw.rect(window, (0, 255, 0), option_rect, 2)
            option_text = font.render(option, True, (0, 0, 255))
            window.blit(option_text, (option_rect.x + 10, option_rect.y + 10))

    # Draw takeable drop-down menu
    pygame.draw.rect(window, color_active if takeable_menu_expanded else color_passive, takeable_menu_rect)
    pygame.draw.rect(window, (0, 255, 0), takeable_menu_rect, 2)
    menu_text = font.render(takeable_selected_option, True, (0, 0, 255))
    window.blit(menu_text, (takeable_menu_rect.x + 10, takeable_menu_rect.y + 10))

    if takeable_menu_expanded:
        for i, option in enumerate(takeable_options):
            option_rect = pygame.Rect(takeable_menu_rect.x,
                                      takeable_menu_rect.y + takeable_menu_rect.height * (i + 1),
                                      takeable_menu_rect.width, takeable_menu_rect.height)
            pygame.draw.rect(window, (0, 0, 0), option_rect)
            pygame.draw.rect(window, (0, 255, 0), option_rect, 2)
            option_text = font.render(option, True, (0, 0, 255))
            window.blit(option_text, (option_rect.x + 10, option_rect.y + 10))                

def draw_buttons(window, font, button_export, button_quit, button_colour, button_border_colour):
    button_text = font.render("Export to JSON", True, button_border_colour)
    pygame.draw.rect(window, button_colour, button_export)
    window.blit(button_text, (button_export.x + 5, button_export.y + 5))

    button_text = font.render("Quit", True, button_border_colour)
    pygame.draw.rect(window, button_colour, button_quit)
    window.blit(button_text, (button_quit.x + 5, button_quit.y + 5))


def draw_matrix_and_lines(window, matrix, lines, mouse_pos, config):
    for node in matrix:
        pygame.draw.circle(window, tuple(config.get_option("itempalette")), node, 5)

    for line in lines:
        pygame.draw.line(window, tuple(config.get_option("entitypalette")), line[0], line[1], 5)

    if source_state:
        pygame.draw.line(window, tuple(config.get_option("entitypalette")), source, mouse_pos, 5)


def handle_mouse_events(event, mouse_pos, matrix, lines, entity_name_input_rect,
                        entity_name_text, entity_type_menu_rect,
                        entity_type_options, button_export, button_quit, skill_input_rect,
                        stamina_input_rect, luck_input_rect, takeable_menu_rect, takeable_options, skill_text, stamina_text, luck_text):
    
    global entity_name_input_active, entity_type_menu_expanded, entity_type_selected_option, \
        takeable_menu_expanded, takeable_selected_option, skill_input_active, stamina_input_active, luck_input_active

    if event.type == pygame.MOUSEBUTTONDOWN:
        if entity_type_menu_rect.collidepoint(mouse_pos):
            entity_type_menu_expanded = not entity_type_menu_expanded
        elif entity_type_menu_expanded:
            for i, option in enumerate(entity_type_options):
                option_rect = pygame.Rect(entity_type_menu_rect.x,
                                          entity_type_menu_rect.y + entity_type_menu_rect.height * (i + 1),
                                          entity_type_menu_rect.width, entity_type_menu_rect.height)
                if option_rect.collidepoint(mouse_pos):
                    entity_type_selected_option = option
                    entity_type_menu_expanded = False

        if takeable_menu_rect.collidepoint(mouse_pos):
            takeable_menu_expanded = not takeable_menu_expanded
        elif takeable_menu_expanded:
            for i, option in enumerate(takeable_options):
                option_rect = pygame.Rect(takeable_menu_rect.x,
                                          takeable_menu_rect.y + takeable_menu_rect.height * (i + 1),
                                          takeable_menu_rect.width, takeable_menu_rect.height)
                if option_rect.collidepoint(mouse_pos):
                    takeable_selected_option = option
                    takeable_menu_expanded = False

        if entity_name_input_rect.collidepoint(mouse_pos):
            entity_name_input_active = True
        else:
            entity_name_input_active = False

        if skill_input_rect.collidepoint(mouse_pos):
            skill_input_active = True
        else:
            skill_input_active = False

        if stamina_input_rect.collidepoint(mouse_pos):
            stamina_input_active = True
        else:
            stamina_input_active = False

        if luck_input_rect.collidepoint(mouse_pos):
            luck_input_active = True
        else:
            luck_input_active = False

        if button_export.collidepoint(mouse_pos):
            export_to_json(entity_name_text, entity_type_selected_option, takeable_selected_option, skill_text, stamina_text, luck_text,
                           lines)
        elif button_quit.collidepoint(mouse_pos):
            return False
        else:
            if is_close_to_any(mouse_pos, matrix)[0]:
                handle_line_drawing(event, mouse_pos, matrix, lines)

    return True


def handle_line_drawing(event, mouse_pos, matrix, lines):
    global drawing_state, source_state, source
    if event.button == 1:
        if not drawing_state and not source_state:
            drawing_state = True
            source = is_close_to_any(mouse_pos, matrix)[1]
            source_state = True
        else:
            drawing_state = False
            destination = is_close_to_any(mouse_pos, matrix)[1]
            lines.append([source, destination])
            source_state = False
    elif event.button == 3:
        handle_line_removal(mouse_pos, lines, matrix)
    elif event.button == 2:
        handle_line_removal(mouse_pos, lines, matrix)
        drawing_state = False
        source_state = False
        source = (0, 0)


def handle_line_removal(mouse_pos, lines, matrix):
    global source
    source = is_close_to_any(mouse_pos, matrix)[1]
    for line in lines:
        if line[0] == source or line[1] == source:
            lines.remove(line)


def main():
    pygame.init()
    window = pygame.display.set_mode((705, 550))
    pygame.display.set_caption('Entity Creator')
    clock = pygame.time.Clock()

    config = ProjectConfig(project_name="knightquest")

    # Define colors
    black = (0, 0, 0)
    button_colour = tuple(config.get_option("entitypalette"))
    button_border_colour = tuple(config.get_option("itempalette"))
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')

    # Define font
    font = pygame.font.Font(None, 28)

    # Initialize parameters for drawing
    global drawing_state, source_state, source, entity_name_input_active, entity_type_menu_expanded, \
        entity_type_selected_option, takeable_menu_expanded, takeable_selected_option, \
        skill_input_active, stamina_input_active, luck_input_active

    lines = []
    source = (0, 0)
    drawing_state = False
    source_state = False
    matrix = [tuple([elem * 50 for elem in (x, y)]) for x in range(1, 11) for y in range(1, 11)]
    run = True

    # Initialize parameters for entity name input
    entity_name_text = ''
    entity_name_input_active = False
    entity_name_input_rect = pygame.Rect(550, 57, 220, 32)

    # Initialize parameters for entity type input
    entity_type_options = ['mob', 'item']
    entity_type_selected_option = entity_type_options[0]
    entity_type_menu_rect = pygame.Rect(550, 139, 140, 32)
    entity_type_menu_expanded = False

    # Initialize parameters for takeable input
    takeable_options = ['true', 'false']
    takeable_selected_option = takeable_options[0]
    takeable_menu_rect = pygame.Rect(550, 264, 140, 32)
    takeable_menu_expanded = False

    # Initialize parameters for skill input
    skill_text = ''
    skill_input_active = False
    skill_input_rect = pygame.Rect(550, 344, 140, 32)

    # Initialize parameters for stamina input
    stamina_text = ''
    stamina_input_active = False
    stamina_input_rect = pygame.Rect(550, 424, 140, 32)

    # Initialize parameters for luck input
    luck_text = ''
    luck_input_active = False
    luck_input_rect = pygame.Rect(550, 504, 140, 32)
    
    # Initialize parameters for buttons
    button_export = pygame.Rect(40, 5, 155, 28)
    button_quit = pygame.Rect(640, 5, 50, 28)

    # Check if a Entity JSON file name was passed as an argument
    if len(sys.argv) == 2:
        entity_file_path = sys.argv[1]
        entity_json_data = import_from_json(entity_file_path)
        entity_name_text = entity_json_data['entity_name']
        entity_type_selected_option = entity_json_data['entity_type']
        takeable_selected_option = entity_json_data['takeable']
        skill_text = str(entity_json_data['skill'])
        stamina_text = str(entity_json_data['stamina'])
        luck_text = str(entity_json_data['luck'])
        lines = [[tuple([elem * 50 for elem in (x['x'] + 1, x['y'] + 1)]),
                  tuple([elem * 50 for elem in (y['x'] + 1, y['y'] + 1)])] for x, y in entity_json_data['entity_image_vectors']]

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        draw_interface(window, font, entity_name_text, entity_name_input_rect,
                       color_active, color_passive, entity_type_menu_rect,
                       entity_type_options, takeable_menu_rect, takeable_options,
                       skill_input_rect, skill_text, stamina_input_rect, stamina_text,
                       luck_input_rect, luck_text)
        draw_buttons(window, font, button_export, button_quit, button_colour, button_border_colour)
        draw_matrix_and_lines(window, matrix, lines, mouse_pos, config)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # Handle entity name input
                if entity_name_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        entity_name_text = entity_name_text[:-1]
                    else:
                        entity_name_text += event.unicode

                # Handle skill input
                if skill_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        skill_text = skill_text[:-1]
                    else:
                        skill_text += event.unicode

                # Handle stamina input
                if stamina_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        stamina_text = stamina_text[:-1]
                    else:
                        stamina_text += event.unicode

                # Handle luck input
                if luck_input_active:
                    if event.key == pygame.K_BACKSPACE:
                        luck_text = luck_text[:-1]
                    else:
                        luck_text += event.unicode

            run = handle_mouse_events(event, mouse_pos, matrix, lines,
                                      entity_name_input_rect, entity_name_text,
                                      entity_type_menu_rect, entity_type_options,
                                      button_export, button_quit, skill_input_rect,
                                      stamina_input_rect, luck_input_rect, takeable_menu_rect, takeable_options, skill_text, stamina_text, luck_text)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
