#!/usr/bin/env python

from Model import Model
from Control import Controller as Controller
from View import View as View


def main():

    view.draw_intro()
    controller.start(model)
    view.draw_view(model)

    while model.game_running:

        controller.update(model)

        if not model.menu_running:
            view.draw_view(model)
        else:
            if not model.status_screen_running:
                view.draw_menu(model)
            else:
                view.draw_status(model)

    if model.game_victory:

        view.draw_end(model)
        controller.start(model)

    if model.game_demise:

        view.draw_demise(model)
        controller.start(model)


if __name__ == "__main__":

    model = Model()
    view = View()
    controller = Controller()

    main()
