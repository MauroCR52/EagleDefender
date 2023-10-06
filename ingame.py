import pygame
import pygame_gui
import button
from pygame import mixer
import math
import sys
import os

class InGame:
    def __init__(self, ancho, alto):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Seleccione Musica")
        self.background = pygame.image.load("Multimedia/Fondo desertico.jpg")
        self.gui_manager = pygame_gui.UIManager((ancho, alto))
        self.cmusica = "Musica"
        self.canciones = [archivo for archivo in os.listdir(self.cmusica) if archivo.endswith('.mp3')]#os.listdir(self.cmusica)
        self.options = ["Option 1", "Option 2"]
        self.list_box = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(50, 50, 200, 30),
                                                      starting_option=self.canciones[0], options_list=self.canciones,
                                                      manager=self.gui_manager)
        self.tank = Tank(375,300)
        self.gun = Gun(self.tank)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tank,self.gun)

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas
        while True:
                time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

                # salir del juego con la ventana
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        self.seleccion = self.list_box.selected_option
                        self.audioplay = os.path.join(self.cmusica, self.seleccion)
                        pygame.mixer.music.load(self.audioplay)
                        pygame.mixer.music.play()


                    # Pasar eventos de pygame a pygame_gui
                    self.gui_manager.process_events(event)  # Actualiza el administrador de interfaz de usuario de pygame_gui

                self.all_sprites.update()

                self.gui_manager.update(time_delta)

                self.screen.blit(self.background, (0, 0))

                # Dibuja los elementos de la interfaz de usuario de pygame_gui
                self.gui_manager.draw_ui(self.screen)
                self.all_sprites.draw(self.screen)
                pygame.display.update()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_tank_image = pygame.image.load("assets/tr2.png").convert_alpha()
        self.tank_image = pygame.transform.scale(self.original_tank_image, (50, 30))
        self.image = self.tank_image
        self.rect = self.tank_image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0


    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.speed = 3
            #move_forward_sound.play()
        elif keys[pygame.K_DOWN]:
            self.speed = -2
            #move_forward_sound.play()
        else:
            self.speed = 0
            #move_forward_sound.stop()

        if keys[pygame.K_LEFT]:
            self.rotation_speed = 2
            #move_forward_sound.play()
        elif keys[pygame.K_RIGHT]:
            self.rotation_speed = -2
            #move_forward_sound.play()

        else:
            self.rotation_speed = 0

        self.angle += self.rotation_speed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.original_tank_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad) * self.speed
        dy = math.sin(angle_rad) * self.speed

        self.rect.x += dx
        self.rect.y -= dy

class Gun(pygame.sprite.Sprite):
    def __init__(self, tank):
        super().__init__()
        self.original_gun_image = pygame.image.load("assets/gr3.png").convert_alpha()
        self.gun_image = pygame.transform.scale(self.original_gun_image, (20, 40))
        self.image = self.gun_image
        self.rect = self.gun_image.get_rect(center=tank.rect.center)
        self.angle = 0
        self.rotation_speed = 0
        self.tank = tank
        self.gun_length = 40

        self.original_gun_length = self.gun_length
        self.gun_back_start_time = 0
        self.gun_back_duration = 200
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.cooldown_duration = 3000
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.rotation_speed = 2
        elif keys[pygame.K_x]:
            self.rotation_speed = -2
        else:
            self.rotation_speed = 0

        self.angle += self.rotation_speed
        self.angle %= 360

        self.image = pygame.transform.rotate(self.original_gun_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        angle_rad = math.radians(self.angle)
        dx = math.cos(angle_rad) * self.gun_length
        dy = -math.sin(angle_rad) * self.gun_length

        self.rect.x = self.tank.rect.centerx - self.rect.width // 2 + dx
        self.rect.y = self.tank.rect.centery - self.rect.height // 2 + dy

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= pygame.time.get_ticks() - self.last_update_time
        else:
            self.can_shoot = True

        self.last_update_time = pygame.time.get_ticks()
