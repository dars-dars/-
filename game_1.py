import pygame
from menu import main_menu, settings_menu
from game_settings import Settings
from actor_script import Actor
from item_script import Weapon, weapon_body_list

pygame.init()
pygame.font.init()
main_screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
pygame.display.set_caption("Моя игра")

actor_1 = Actor(color=(0, 255, 0), x=150, y=400, speed=10, role = "player")

actor_enemy_1 = Actor(x=600, y=350, speed=10, role = "enemy")

weapon_1 = Weapon(x=200, y=480)
weapon_2 = Weapon(x = 500, y = 480)

button_skill_1 = pygame.Rect(100, 400, 50, 50)

block_1 = pygame.Rect(600, 450, 100, 25)
block_2 = pygame.Rect(0, 450, 100, 25)

direction = 0

while True:
    action = main_menu(main_screen, Settings)
    if action == "start":
        while True:
            main_screen.fill((0, 0, 255))

            weapon_1.rendering(rendering_surf=main_screen)
            weapon_2.rendering(rendering_surf = main_screen)
            if not actor_1.dead:
                actor_1.rendering(rendering_surf=main_screen)
            if not actor_enemy_1.dead:
                actor_enemy_1.rendering(rendering_surf=main_screen)


            pygame.draw.rect(main_screen, color=(255, 255, 255), rect=block_1)
            pygame.draw.rect(main_screen, color=(255, 255, 255), rect=block_2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        direction = 1
                    elif event.key == pygame.K_LEFT:
                       direction = -1

                    elif event.key == pygame.K_SPACE:
                        actor_1.jump()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        direction = 0
                    elif event.key == pygame.K_LEFT:
                        direction = 0

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if len(actor_1.backpack) > 0:
                        actor_1.backpack[0].fire()

                if len(actor_1.backpack) > 0:
                    actor_1.backpack[0].projectile.check_hit()

            pygame.time.delay(60)

            actor_1.take_item(item_list=weapon_body_list)
            actor_1.moving(direction, [block_1, block_2])
            if not actor_enemy_1.dead:
                if len(actor_enemy_1.backpack) > 0:
                    actor_enemy_1.backpack[0].rendering(rendering_surf = main_screen)
                    actor_enemy_1.backpack[0].projectile.check_hit()    
                if len(actor_enemy_1.backpack) == 0:
                    actor_enemy_1.move_towards(weapon_2.weapon_body)
                    actor_enemy_1.take_item(item_list = weapon_body_list)
                else:
                    actor_enemy_1.fire_at_target(actor_1.actor_body)
                    actor_enemy_1.move_towards_to_player(actor_1, min_distance = 100)

            if actor_enemy_1.dead:
                font = pygame.font.Font(None, 74)
                victory_text = font.render("victory!", True, (0,255,0))
                main_screen.blit(victory_text, (Settings.screen_width // 2 - victory_text.get_width() // 2,
                                                 Settings.screen_height // 2 - victory_text.get_height()// 2 ))

            pygame.display.update()
    elif action == "settings":
        settings_menu(main_screen, Settings)
        action = main_menu(main_screen, Settings)
