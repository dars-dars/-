class Settings:
    screen_width = 800
    screen_height = 500
    need_gravity = True

    def apply(self, screen):
        return pygame.set_mode((self.screen_width, self.screen_height))