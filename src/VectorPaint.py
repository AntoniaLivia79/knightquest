import pygame
import src.Config as Config


def main():
    def is_close_to_any(coord, coord_list, tolerance=5):
        for c in coord_list:
            if abs(c[0] - coord[0]) <= tolerance and abs(c[1] - coord[1]) <= tolerance:
                return [True, c]
        return [False, (0,0)]

    pygame.init()
    window = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()

    lines = [(0, 0)]
    draw = False
    plot = False

    matrix = [tuple([elem * 50 for elem in (x, y)]) for x in range(1, 11) for y in range(1, 11)]
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:
                plot_pos = event.pos
                draw = True
            if event.type == pygame.MOUSEBUTTONDOWN and not plot and is_close_to_any(event.pos, matrix)[0]:
                new_pos = is_close_to_any(event.pos, matrix)[1]

                plot = True
                lines.append(new_pos)
            else:
                if event.type == pygame.MOUSEBUTTONUP and plot:
                    plot = False

        window.fill((0, 0, 0))
        old_points = (0, 0)

        for node in matrix:
            pygame.draw.circle(window, Config.itempalette, node, 5)

        for points in lines:
            if points != old_points and points[0] != 0:
                pygame.draw.line(window, Config.entitypalette, old_points, points, 5)
                old_points = points

        if draw and len(lines) > 1:
            pygame.draw.line(window, Config.entitypalette, points, plot_pos, 5)
            draw = False

        pygame.display.flip()

        # Print the list of coordinates
        print(lines)

    pygame.quit()
    exit()


if __name__ == "__main__":
    main()
