import pygame
import sys
def main_menu(screen, settings):
    pygame.font.init()
    menu_font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)

    title_text = menu_font.render("Главное меню", True,(255,255,255))
    start_text = button_font.render("Начать игру", True,(0,255,0))
    setting_text = button_font.render("Настройки", True,(255,255,0))
    quit_text = button_font.render("Выход", True,(255, 0, 0))


    start_rect = start_text.get_rect(center = (settings.screen_width // 2, settings.screen_height // 2 - 50))
    settings_rect = setting_text.get_rect(center = (settings.screen_width // 2, settings.screen_height // 2))
    quit_rect = quit_text.get_rect(center = (settings.screen_width // 2, settings.screen_height // 2 + 50))

    while True:
        screen.fill((0,0,0))
        screen.blit(title_text,(settings.screen_width // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, start_rect)
        screen.blit(setting_text,settings_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    return "start"
                if settings_rect.collidepoint(event.pos):
                    return "settings"
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


def settings_menu(screen, settings):
    pygame.font.init()
    menu_font = pygame.font.Font(None, 74) 
    button_font = pygame.font.Font(None, 50) 

    resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
 
    while True:

        if not isinstance(screen, pygame.Surface):
            raise ValueError("screen must be a pygame.Surface object.")
        screen.fill((0, 0, 0))
 
        title_text = menu_font.render("Настройки", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(settings.screen_width // 2, 50))
        screen.blit(title_text, title_rect)
 
        resolution_rects = []
        for i, res in enumerate(resolutions):
            res_text = button_font.render(f"{res[0]}x{res[1]}", True, (255, 255, 255))
            res_rect = res_text.get_rect(center=(settings.screen_width // 2, 200 + i * 50))
            resolution_rects.append((res_text, res_rect))
            screen.blit(res_text, res_rect)
 
        back_text = button_font.render("Назад", True, (255, 0, 0))
        back_rect = back_text.get_rect(center=(settings.screen_width // 2, settings.screen_height - 100))
        screen.blit(back_text, back_rect)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                for i, (_, res_rect) in enumerate(resolution_rects):
                    if res_rect.collidepoint(event.pos):
                        new_resolution = resolutions[i]
                        settings.screen_width, settings.screen_height = new_resolution
                        screen = pygame.display.set_mode(new_resolution)  
                        print(f"Resolution changed to: {new_resolution}")
 

                if back_rect.collidepoint(event.pos):
                    return  
 
        pygame.display.update()