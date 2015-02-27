from input_map import *
from minigames import minigame
from minigames.mirrors.entities.blaster import Blaster
from minigames.mirrors.entities.blaster_base import BlasterBase
from minigames.mirrors.entities.mirror import Mirror


class MirrorsMinigame(minigame.Minigame):
    name = "Break The Mirrors!"
    game_type = minigame.MULTIPLAYER
    max_duration = 7000

    MIRROR_BASE_COUNT = 3
    MIRROR_BASE_COOLDOWN = 200
    MIRROR_SHOW_DURATION = 1000

    def __init__(self, game):
        minigame.Minigame.__init__(self, game)
        self.backdrop = pygame.image.load("minigames/mirrors/images/backdrop.png").convert()
        self.backdrop = pygame.transform.scale(self.backdrop, (int(self.backdrop.get_width() * 3.5), int(self.backdrop.get_height() * 3.5)))

    def init(self):
        self._first_tick = True

        self.base = BlasterBase(2)
        self.mirrors = []
        self.mirror_count = MirrorsMinigame.MIRROR_BASE_COUNT + 2 * self.difficulty
        self.mirror_cooldown = 0
        self.score = [0, 0]
        self.results = [False, False]

    def tick(self):
        self.screen.blit(self.backdrop, (0, -50))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                for i in range(len(self.base.blasters)):
                    if event.key == PLAYERS_MAPPING[i][UP] or event.key == PLAYERS_MAPPING[i][LEFT]:
                        self.base.blasters[i].set_motion(Blaster.ACCELERATING)
                        self.base.blasters[i].set_direction(Blaster.RIGHT)
                    elif event.key == PLAYERS_MAPPING[i][DOWN] or event.key == PLAYERS_MAPPING[i][RIGHT]:
                        self.base.blasters[i].set_motion(Blaster.ACCELERATING)
                        self.base.blasters[i].set_direction(Blaster.LEFT)
                    elif event.key == PLAYERS_MAPPING[i][ACTION]:
                        self.base.blasters[i].set_action(Blaster.CHARGING)
            elif event.type == KEYUP:
                for i in range(len(self.base.blasters)):
                    if event.key == PLAYERS_MAPPING[i][UP] or event.key == PLAYERS_MAPPING[i][LEFT]:
                        self.base.blasters[i].set_motion(Blaster.DECELERATING)
                        self.base.blasters[i].set_direction(Blaster.RIGHT)
                    elif event.key == PLAYERS_MAPPING[i][DOWN] or event.key == PLAYERS_MAPPING[i][RIGHT]:
                        self.base.blasters[i].set_motion(Blaster.DECELERATING)
                        self.base.blasters[i].set_direction(Blaster.LEFT)
                    elif event.key == PLAYERS_MAPPING[i][ACTION]:
                        self.base.blasters[i].set_action(Blaster.SHOOTING)

        if self.mirror_cooldown == 0 and len(self.mirrors) < self.mirror_count:
            self.mirror_cooldown = max(MirrorsMinigame.MIRROR_BASE_COOLDOWN - self.difficulty * 35, 50)

            self.mirrors.append(Mirror((self.screen.get_width(), self.screen.get_height()), max(MirrorsMinigame.MIRROR_SHOW_DURATION - self.difficulty * 150, 200), self.mirrors))
        else:
            self.mirror_cooldown -= 1

        for player in self.base.get_points(self.mirrors):
            self.score[player] += 1

            self.results[0] = self.score[0] >= self.score[1]
            self.results[1] = self.score[1] >= self.score[0]

        self.gfx.print_msg(str(self.score[0]), (self.screen.get_width() / 2 - 200, self.screen.get_height() / 2), color=(255, 0, 0))
        self.gfx.print_msg(str(self.score[1]), (self.screen.get_width() / 2 + 200, self.screen.get_height() / 2), color=(0, 0, 255))
        self.base.display(self.screen)

        for i, m in enumerate(self.mirrors):
            if not m.is_visible():
                del self.mirrors[i]
            else:
                m.display(self.screen)

    def get_results(self):
        return self.results
