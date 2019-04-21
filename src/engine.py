from ecs.container import Container


class Main:
    def __init__(self):
        self.container = Container()

    def core_game_loop(self):
        while True:
            self.container.update()


if __name__ == '__main__':
    Main().core_game_loop()
