import pygame
import json
import Config as Config


def main():
    def is_close_to_any(coord, coord_list, tolerance=5):
        for c in coord_list:
            if abs(c[0] - coord[0]) <= tolerance and abs(c[1] - coord[1]) <= tolerance:
                return [True, c]
        return [False, (0,0)]

    def export_to_json():
        json_data = {"entity_image_vectors": [[{'x': int(src[0]/50) - 1, 'y': int(src[1]/50) - 1},
                      {'x': int(dest[0]/50) - 1, 'y': int(dest[1]/50) - 1}] for src, dest in lines]}

        with open('exported_lines.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=2)
        print('Lines exported to exported_lines.json')

    pygame.init()
    window = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    # Define colors
    black = (0, 0, 0)
    button_colour = Config.entitypalette
    button_border_colour = Config.itempalette

    # Define font
    font = pygame.font.Font(None, 14)

    lines = []
    plot_position = (0, 0)
    source = (0, 0)
    drawing_state = False
    source_state = False

    matrix = [tuple([elem * 50 for elem in (x, y)]) for x in range(1, 11) for y in range(1, 11)]
    run = True

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
        # Draw the node matrix
        for node in matrix:
            pygame.draw.circle(window, Config.itempalette, node, 5)
        # Draw all stored lines
        for line in lines:
            pygame.draw.line(window, Config.entitypalette, line[0], line[1], 5)

        # Draw a line if source exists but not drawing is not yet stored in lines list (function)
        if source_state:
            pygame.draw.line(window, Config.entitypalette, source, plot_position, 5)

        # Detect pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if hasattr(event, 'pos'):
                plot_position = event.pos

            # Add a drawn line to the lines list (function)
            # Detect if clicked mouse, drawing line is in progress and near to a node
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_export.collidepoint(mouse_pos):
                    export_to_json()
                else:
                    if button_quit.collidepoint(mouse_pos):
                        run = False
                    else:
                        if is_close_to_any(plot_position, matrix)[0]:
                            # On left mouse button click, begin drawing line or complete drawing line
                            if event.button == 1:
                                if not drawing_state and not source_state:
                                    # A new line is now being drawn, change the drawing state
                                    drawing_state = True
                                    # Store the source coordinate which has just been plotted and change the source state
                                    source = is_close_to_any(plot_position, matrix)[1]
                                    source_state = True
                                else:
                                    # Drawing a line is now complete, reset the drawing state
                                    drawing_state = False
                                    # Find the node closest to the mouse coordinate
                                    destination = is_close_to_any(plot_position, matrix)[1]
                                    # Store the source and destination coordinates of the drawn line
                                    lines.append([source, destination])
                                    # Reset the source and destination states
                                    source_state = False
                            # On right mouse button click, clear any lines from the lines list containing the clicked node
                            if event.button == 3:
                                source = is_close_to_any(plot_position, matrix)[1]
                                for line in lines:
                                    if line[0] == source or line[1] == source:
                                        lines.remove(line)

            # Draw a line if source exists but not drawing is not yet stored in lines list (function)
            if source_state:
                pygame.draw.line(window, Config.entitypalette, source, plot_position, 5)

        # Update the display
        pygame.display.flip()

        # Print the list of coordinates
        print(lines)

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
