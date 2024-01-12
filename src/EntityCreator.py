import pygame
import json
import Config as Config


def is_close_to_any(coord, coord_list, tolerance=5):
    for c in coord_list:
        if abs(c[0] - coord[0]) <= tolerance and abs(c[1] - coord[1]) <= tolerance:
            return [True, c]
    return [False, (0, 0)]


def export_to_json(entityname, lines):
    json_data = {
        "entity_name": entityname,
        "entity_image_vectors": [
            [{'x': int(src[0] / 50) - 1, 'y': int(src[1] / 50) - 1},
             {'x': int(dest[0] / 50) - 1, 'y': int(dest[1] / 50) - 1}] for src, dest in lines
        ]
    }
    filename = entityname + '.json'
    with open(filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)


def draw_interface(window, font, entity_name_text, entity_name_input_rect, color_active, color_passive,
                   entity_type_menu_rect, entity_type_options):
    global entity_name_input_active, entity_type_menu_expanded, entity_type_selected_option
    window.fill((0, 0, 0))  # Fill screen with black
    pygame.draw.rect(window, color_active if entity_name_input_active else color_passive, entity_name_input_rect)
    text_surface = font.render(entity_name_text, True, (0, 0, 0))
    window.blit(text_surface, (entity_name_input_rect.x + 5, entity_name_input_rect.y + 5))
    entity_name_input_rect.w = max(100, text_surface.get_width() + 10)

    entity_name_text_label = font.render('Entity Name:', True, (0, 0, 255), (0, 0, 0))
    entity_name_text_label_rect = entity_name_text_label.get_rect()
    entity_name_text_label_rect.center = (600, 80)
    window.blit(entity_name_text_label, entity_name_text_label_rect)

    # Draw drop-down menu
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


def draw_buttons(window, font, button_export, button_quit, button_colour, button_border_colour):
    button_text = font.render("Export to JSON", True, button_border_colour)
    pygame.draw.rect(window, button_colour, button_export)
    window.blit(button_text, (button_export.x + 5, button_export.y + 5))

    button_text = font.render("Quit", True, button_border_colour)
    pygame.draw.rect(window, button_colour, button_quit)
    window.blit(button_text, (button_quit.x + 5, button_quit.y + 5))


def draw_matrix_and_lines(window, matrix, lines, mouse_pos):
    for node in matrix:
        pygame.draw.circle(window, Config.itempalette, node, 5)

    for line in lines:
        pygame.draw.line(window, Config.entitypalette, line[0], line[1], 5)

    if source_state:
        pygame.draw.line(window, Config.entitypalette, source, mouse_pos, 5)


def handle_mouse_events(event, mouse_pos, matrix, lines, entity_name_input_rect,
                        entity_name_text, entity_type_menu_rect,
                        entity_type_options, button_export, button_quit):
    global entity_name_input_active, entity_type_menu_expanded, entity_type_selected_option
    if event.type == pygame.MOUSEBUTTONDOWN:

        if entity_type_menu_rect.collidepoint(mouse_pos):
            entity_type_menu_expanded = not entity_type_menu_expanded
        elif entity_type_menu_expanded and not entity_type_menu_rect.collidepoint(event.pos):
            entity_type_menu_expanded = False
        elif entity_type_menu_expanded:
            # Check if an option is clicked
            for i, option in enumerate(entity_type_options):
                option_rect = pygame.Rect(entity_type_menu_rect.x,
                                          entity_type_menu_rect.y + entity_type_menu_rect.height * (i + 1),
                                          entity_type_menu_rect.width, entity_type_menu_rect.height)
                if option_rect.collidepoint(event.pos):
                    entity_type_selected_option = option
                    entity_type_menu_expanded = False

        if entity_name_input_rect.collidepoint(mouse_pos):
            entity_name_input_active = True
        else:
            entity_name_input_active = False

        if button_export.collidepoint(mouse_pos):
            export_to_json(entity_name_text, lines)
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
        handle_line_removal(mouse_pos, lines)


def handle_line_removal(mouse_pos, lines, matrix):
    global source
    source = is_close_to_any(mouse_pos, matrix)[1]
    for line in lines:
        if line[0] == source or line[1] == source:
            lines.remove(line)


def main():
    pygame.init()
    window = pygame.display.set_mode((860, 600))
    pygame.display.set_caption('Entity Creator')
    clock = pygame.time.Clock()

    # Define colors
    black = (0, 0, 0)
    button_colour = Config.entitypalette
    button_border_colour = Config.itempalette
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')

    # Define font
    font = pygame.font.Font(None, 28)

    # Initialize parameters for drawing
    global drawing_state, source_state, source, entity_name_input_active, entity_type_menu_expanded, \
        entity_type_selected_option
    lines = []
    source = (0, 0)
    drawing_state = False
    source_state = False
    matrix = [tuple([elem * 50 for elem in (x, y)]) for x in range(1, 11) for y in range(1, 11)]
    run = True

    # Initialize parameters for entity name input
    entity_name_text = ''
    entity_name_input_active = False
    entity_name_input_rect = pygame.Rect(550, 100, 140, 32)

    # Initialize parameters for entity type input
    entity_type_options = ['mob', 'item']
    entity_type_selected_option = entity_type_options[0]
    entity_type_menu_rect = pygame.Rect(550, 140, 140, 32 )
    entity_type_menu_expanded = False

    button_export = pygame.Rect(5, 5, 150, 40)
    button_quit = pygame.Rect(200, 5, 70, 40)

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        draw_interface(window, font, entity_name_text, entity_name_input_rect,
                       color_active, color_passive, entity_type_menu_rect,
                       entity_type_options)
        draw_buttons(window, font, button_export, button_quit, button_colour, button_border_colour)
        draw_matrix_and_lines(window, matrix, lines, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    entity_name_text = entity_name_text[:-1]
                else:
                    entity_name_text += event.unicode

            run = handle_mouse_events(event, mouse_pos, matrix, lines,
                                      entity_name_input_rect, entity_name_text,
                                      button_export, entity_type_options, button_export, button_quit)

        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
