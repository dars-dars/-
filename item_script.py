import pygame
import math
import actor_script

weapon_body_list = []
weapon_list = []

class Projectile:
    def __init__(self, size: tuple = (10, 10), color: tuple = (255, 0, 0),
                 x: float = 0, y: float = 0):
        self.size = size
        self.color = color
        self.surf = pygame.surface.Surface(size=self.size)
        self.body = self.surf.get_rect(x=x, y=y)
        self.direction =[0,0 ]
        self.ricochet_count = 0
        
    def set_direction(self,target_x, target_y):
        dx = target_x - self.body.centerx
        dy = target_y - self.body.centery
        magnitude = math.sqrt(dx**2 + dy**2)
        if magnitude != 0:
            self.direction = [dx / magnitude * 50, dy / magnitude * 50]
        
    def move(self):
        self.body.x += self.direction[0]
        self.body.y += self.direction[1]
        
        if self.body.left <= 0 or self.body.right >= 800:
          self.direction[0] = -self.direction[0]
          self.ricochet_count +=1
        if self.body.top <= 0 or self.body.bottom >= 500:
          self.direction[1] = -self.direction[1]
          self.ricochet_count +=1
        if self.ricochet_count >= 3:
          self.ricochet_count = 0
          return False
        return True

    def check_hit(self):
        target_list = actor_script.actor_body_list
        if len(actor_script.actor_body_list) > 0:
            if self.body.collidelist(target_list) != -1:
                current_target = actor_script.actor_list[self.body.collidelist(target_list)]
                current_target.get_hit()
                if current_target.dead:
                    actor_script.actor_list.pop(self.body.collidelist(target_list))
                    actor_script.actor_body_list.pop(self.body.collidelist(target_list))



class Weapon:
    def __init__(self, size: tuple = (40, 20), color: tuple = (200, 180, 120),
                 x: float = 0, y: float = 0):
        self.weapon_size = size
        self.weapon_color = color
        self.weapon_surf = pygame.surface.Surface(size = self.weapon_size)
        self.weapon_body = self.weapon_surf.get_rect(x=x, y=y)
        self.rendering_surf = None
        self.projectile = Projectile()
        self.projectile_tau = 0
        self.fire_flag = False
        weapon_list.append(self)
        weapon_body_list.append(self.weapon_body)

 
    def rendering(self, rendering_surf: pygame.surface.Surface=None, color:
                   tuple=None):
        if rendering_surf is not None:
            self.rendering_surf = rendering_surf
        rendering_surf = self.rendering_surf
        if color is None:
            color = self.weapon_color
        self.weapon_surf.fill(color)
        rendering_surf.blit(self.weapon_surf, self.weapon_body)

        if not self.fire_flag:
            self.projectile.body.x = self.weapon_body.midright[0]
            self.projectile.body.y = self.weapon_body.midright[1]
        else:
            pygame.draw.rect(rendering_surf, color=(255, 100, 50), rect=self.projectile.body)
            if not self.projectile.move():
                self.fire_flag = False

    def fire(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.projectile.set_direction(mouse_x, mouse_y)
        self.fire_flag = True
    def fire_to_player(self, target_x, target_y):
        if not self.fire_flag or not self.projectile.move():
            self.projectile = Projectile(x = self.weapon_body.centerx, y = self.weapon_body.centery)
            self.projectile.set_direction(target_x, target_y)
            self.fire_flag = True
