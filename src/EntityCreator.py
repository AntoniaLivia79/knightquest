import pygame
import json
import Config as Config


def main():
    def is_close_to_any(coord, coord_list, tolerance=5):
        for c in coord_list:
            if abs(c[0] - coord[0]) <= tolerance and abs(c[1] - coord[1]) <= tolerance:
                return [True, c]
        return [False, (0, 0)]

    def export_to_json(entityname='default'):
        json_data = {"entity_name": entityname,
                     "entity_image_vectors": [[{'x': int(src[0] / 50) - 1, 'y': int(src[1] / 50) - 1},
                                               {'x': int(dest[0] / 50) - 1, 'y': int(dest[1] / 50) - 1}] for src, dest
                                              in lines]}
        filename = entityname + '.json'
        with open(filename, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)

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

    # Initialise parameters for drawing
    lines = []
    source = (0, 0)
    drawing_state = False
    source_state = False
    matrix = [tuple([elem * 50 for elem in (x, y)]) for x in range(1, 11) for y in range(1, 11)]
    run = True

    # Initialise parameters for entity name input
    entity_name_text = ''
    entity_name_input_active = False
    entity_name_text_label = font.render('Entity Name:', True, (0, 0, 255), (0, 0, 0))
    entity_name_input_rect = pygame.Rect(550, 100, 140, 32)
    entity_name_text_label_rect = entity_name_text_label.get_rect()
    entity_name_text_label_rect.center = (600, 80)

    while run:
        # Update the pygame clock
        clock.tick(60)

        # Render the current drawing (function)
        # Fill screen with black
        window.fill(black)
        # Draw export button
        button_text = font.render("Export to JSON", True, button_border_colour)
        button_export = pygame.Rect(5, 5, button_text.get_width() + 10, button_text.get_height() + 10)
        pygame.draw.rect(window, button_colour, button_export)
        window.blit(button_text, (button_export.x + 5, button_export.y + 5))
        # Draw quit button
        button_text = font.render("Quit", True, button_border_colour)
        button_quit = pygame.Rect(200, 5, button_text.get_width() + 10, button_text.get_height() + 10)
        pygame.draw.rect(window, button_colour, button_quit)
        window.blit(button_text, (button_quit.x + 5, button_quit.y + 5))

        window.blit(entity_name_text_label, entity_name_text_label_rect)

        # Draw the node matrix
        for node in matrix:
            pygame.draw.circle(window, Config.itempalette, node, 5)
        # Draw all stored lines
        for line in lines:
            pygame.draw.line(window, Config.entitypalette, line[0], line[1], 5)

        mouse_pos = pygame.mouse.get_pos()
        # Draw a line if source exists but not drawing is not yet stored in lines list (function)
        if source_state:
            pygame.draw.line(window, Config.entitypalette, source, mouse_pos, 5)

        # Detect pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # mouse_pos = pygame.mouse.get_pos()
            # Add a drawn line to the lines list (function)
            # Detect if clicked mouse, drawing line is in progress and near to a node
            if event.type == pygame.MOUSEBUTTONDOWN:
                if entity_name_input_rect.collidepoint(mouse_pos):
                    entity_name_input_active = True
                else:
                    entity_name_input_active = False

                if button_export.collidepoint(mouse_pos):
                    export_to_json(entity_name_text)
                else:
                    if button_quit.collidepoint(mouse_pos):
                        run = False
                    else:
                        if is_close_to_any(mouse_pos, matrix)[0]:
                            # On left mouse button click, begin drawing line or complete drawing line
                            if event.button == 1:
                                if not drawing_state and not source_state:
                                    # A new line is now being drawn, change the drawing state
                                    drawing_state = True
                                    # Store the source coordinate which has just been plotted
                                    # and change the source state
                                    source = is_close_to_any(mouse_pos, matrix)[1]
                                    source_state = True
                                else:
                                    # Drawing a line is now complete, reset the drawing state
                                    drawing_state = False
                                    # Find the node closest to the mouse coordinate
                                    destination = is_close_to_any(mouse_pos, matrix)[1]
                                    # Store the source and destination coordinates of the drawn line
                                    lines.append([source, destination])
                                    # Reset the source and destination states
                                    source_state = False
                            # On right mouse button click, clear any lines from the lines list
                            # containing the clicked node
                            if event.button == 3:
                                source = is_close_to_any(mouse_pos, matrix)[1]
                                for line in lines:
                                    if line[0] == source or line[1] == source:
                                        lines.remove(line)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    entity_name_text = entity_name_text[:-1]
                else:
                    entity_name_text += event.unicode

        if entity_name_input_active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(window, color, entity_name_input_rect)
        text_surface = font.render(entity_name_text, True, (0, 0, 0))

        window.blit(text_surface, (entity_name_input_rect.x + 5, entity_name_input_rect.y + 5))
        entity_name_input_rect.w = max(100, text_surface.get_width() + 10)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
