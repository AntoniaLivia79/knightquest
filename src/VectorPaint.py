import pygame
import Config as Config


def main():
    def is_close_to_any(coord, coord_list, tolerance=5):
        for c in coord_list:
            if abs(c[0] - coord[0]) <= tolerance and abs(c[1] - coord[1]) <= tolerance:
                return [True, c]
        return [False, (0,0)]

    pygame.init()
    window = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    lines = []
    plot_position = (0, 0)
    source = (0, 0)
    destination = (0, 0)
    drawing_state = False
    source_state = False

    matrix = [tuple([elem * 50 for elem in (x, y)]) for x in range(1, 11) for y in range(1, 11)]
    run = True

    while run:
        # Update the pygame clock
        clock.tick(60)

        # Render the current drawing (function)
        # Fill screen with black
        window.fill((0, 0, 0))
        # Draw the node matrix
        for node in matrix:
            pygame.draw.circle(window, Config.itempalette, node, 5)
        # Draw all stored lines
        for line in lines:
            pygame.draw.line(window, Config.entitypalette, line[0], line[1], 5)

        # Detect pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if hasattr(event, 'pos'):
                plot_position = event.pos

            # Add a drawn line to the lines list (function)
            # Detect if clicked mouse, drawing line is in progress and near to a node
            if event.type == pygame.MOUSEBUTTONDOWN and is_close_to_any(plot_position, matrix)[0]:
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
