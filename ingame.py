import pygame
import pygame_gui
import button
from pygame import mixer
import math
import sys
import os
from tkinter import messagebox

class InGame:
    def __init__(self, ancho, alto, rol, user):
        pygame.init()
        mixer.init()
        self.rol = rol
        self.user = user
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Seleccione Musica")
        self.background = pygame.image.load("assets/ingame_bg.png")
        self.gui_manager = pygame_gui.UIManager((ancho, alto))
        self.cmusica = "Musica"
        self.canciones = [archivo for archivo in os.listdir(self.cmusica) if archivo.endswith('.mp3')]#os.listdir(self.cmusica)
        self.options = ["Option 1", "Option 2"]
        self.list_box = pygame_gui.elements.UIDropDownMenu(relative_rect=pygame.Rect(50, 50, 200, 30),
                                                      starting_option=self.canciones[0], options_list=self.canciones,
                                                      manager=self.gui_manager)

        self.start = False
        self.TILE_TYPES = 3
        self.ROWS = 15
        self.COLS = 23
        self.TILE_SIZE = 768 // self.ROWS
        self.current_tile = 0
        self.img_list = []
        for x in range(self.TILE_TYPES):
            img = pygame.image.load(f'assets/blocks/full/{x}.png')
            img2 = pygame.transform.scale(img, (self.TILE_SIZE, self.TILE_SIZE))
            self.img_list.append(img2)
        self.button_list = []
        self.button_col = 0
        self.button_row = 0
        for i in range(len(self.img_list)):
            tile_button = button.Button(1168 + (75 * self.button_col) + 50, 75 * self.button_row + 50, self.img_list[i], 1)
            self.button_list.append(tile_button)
            self.button_row += 1
            if self.button_row == 1:
                self.button_row += 0
                self.button_col += 0


        self.world_data = []
        for row in range(self.ROWS):
            r = [-1] * self.COLS
            self.world_data.append(r)

        self.tank = Tank(375,300)
        self.gun = Gun(self.tank)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.tank,self.gun)
        self.bullet_sprites = pygame.sprite.Group()
        self.balas_perdidas = 0
        self.max_disparosf = 0
        self.max_disparosw = 0
        self.max_disparosb = 0
        self.fuente = pygame.font.Font(None, 25)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.wood_blocks = 10
        self.steel_blocks = 10
        self.concrete_blocks = 10

        self.button_start = pygame.Rect(1220, 280, 130, 70)
        self.button_start_label = pygame_gui.elements.UIButton(relative_rect=self.button_start, text="Empezar", manager=self.gui_manager)


    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.screen.blit(self.img_list[tile], (x * self.TILE_SIZE, y * self.TILE_SIZE))
    def draw_grid(self):
        for c in range(self.COLS+1):
            pygame.draw.line(self.screen, self.white, (c * self.TILE_SIZE, 0), (c * self.TILE_SIZE, 766))
        for c in range(self.ROWS+1):
            pygame.draw.line(self.screen, self.white, (0, c * self.TILE_SIZE), (1173, c * self.TILE_SIZE))

    def begin(self):
        self.button_start_label.disable()

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
                self.texto = f"Balas perdidas:{self.balas_perdidas}"
                self.counter_0 = f"= {self.wood_blocks}"
                self.counter_1 = f"= {self.steel_blocks}"
                self.counter_2 = f"= {self.concrete_blocks}"

                self.texto_renderizado = self.fuente.render(self.texto, True, self.black)
                self.c_0_render = self.fuente.render(self.counter_0, True, self.white)
                self.c_1_render = self.fuente.render(self.counter_1, True, self.white)
                self.c_2_render = self.fuente.render(self.counter_2, True, self.white)

                self.gui_manager.update(time_delta)



                if self.gun.can_shoot:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE] and self.max_disparosf < 5:
                        bullet_angle = self.gun.angle
                        bullet_x = self.gun.rect.centerx + (self.gun.gun_length + self.gun.tip_offset) * math.cos(
                            math.radians(bullet_angle))
                        bullet_y = self.gun.rect.centery - (self.gun.gun_length + self.gun.tip_offset) * math.sin(
                            math.radians(bullet_angle))
                        bullet = Bullet(bullet_x, bullet_y, bullet_angle)
                        self.all_sprites.add(bullet)
                        self.bullet_sprites.add(bullet)
                        self.gun.can_shoot = False
                        self.gun.shoot_cooldown = self.gun.cooldown_duration
                        self.balas_perdidas += 1
                        self.max_disparosf += 1
                        print(self.balas_perdidas)
                self.bullet_sprites.update()

                if self.gun.can_shoot:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_c] and self.max_disparosw < 5:
                        bullet_angle = self.gun.angle
                        bullet_x = self.gun.rect.centerx + (self.gun.gun_length + self.gun.tip_offset) * math.cos(
                            math.radians(bullet_angle))
                        bullet_y = self.gun.rect.centery - (self.gun.gun_length + self.gun.tip_offset) * math.sin(
                            math.radians(bullet_angle))
                        self.waterbullet = WB(bullet_x, bullet_y, bullet_angle)
                        self.all_sprites.add(self.waterbullet)
                        self.bullet_sprites.add(self.waterbullet)
                        self.gun.can_shoot = False
                        self.gun.shoot_cooldown = self.gun.cooldown_duration
                        self.balas_perdidas += 1
                        self.max_disparosw += 1
                        print(self.balas_perdidas)
                self.bullet_sprites.update()

                if self.gun.can_shoot:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_v] and self.max_disparosb < 5:
                        bullet_angle = self.gun.angle
                        bullet_x = self.gun.rect.centerx + (self.gun.gun_length + self.gun.tip_offset) * math.cos(
                            math.radians(bullet_angle))
                        bullet_y = self.gun.rect.centery - (self.gun.gun_length + self.gun.tip_offset) * math.sin(
                            math.radians(bullet_angle))
                        bombbullet = BB(bullet_x, bullet_y, bullet_angle)
                        self.all_sprites.add(bombbullet)
                        self.bullet_sprites.add(bombbullet)
                        self.gun.can_shoot = False
                        self.gun.shoot_cooldown = self.gun.cooldown_duration
                        self.balas_perdidas += 1
                        self.max_disparosb += 1
                        print(self.balas_perdidas)
                self.bullet_sprites.update()

                self.screen.blit(self.background, (0, 0))
                self.draw_grid()
                self.draw_world()
                self.screen.blit(self.texto_renderizado, (10, 10))
                self.screen.blit(self.c_0_render, (1280, 65))
                self.screen.blit(self.c_1_render, (1280, 140))
                self.screen.blit(self.c_2_render, (1280, 215))

                # Dibuja los elementos de la interfaz de usuario de pygame_gui
                self.gui_manager.draw_ui(self.screen)
                self.bullet_sprites.draw(self.screen)

                button_count = 0
                for button_count, i in enumerate(self.button_list):
                    if i.draw(self.screen):
                        self.current_tile = button_count

                pygame.draw.rect(self.screen, (196, 12, 12), self.button_list[self.current_tile].rect, 3)
                pos = pygame.mouse.get_pos()
                x = (pos[0]) // self.TILE_SIZE
                y = pos[1] // self.TILE_SIZE

                #revisar que el mouse se encuentre dentro de la matriz
                if pos[0] < 1173 and pos[1] < 766:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if self.world_data[y][x] != self.current_tile:
                            # si el bloque aun no ha llegado a 0
                            if (self.current_tile == 0 and self.wood_blocks != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.wood_blocks -= 1
                            elif (self.current_tile == 1 and self.steel_blocks != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.steel_blocks -= 1
                            elif (self.current_tile == 2 and self.concrete_blocks != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.concrete_blocks -= 1

                    if pygame.mouse.get_pressed()[2] == 1:
                        if self.world_data[y][x] == 0:
                            self.wood_blocks += 1
                        if self.world_data[y][x] == 1:
                            self.steel_blocks += 1
                        if self.world_data[y][x] == 2:
                            self.concrete_blocks += 1
                        self.button_start_label.disable()
                        self.world_data[y][x] = -1

                if (self.wood_blocks == 0 and self.steel_blocks == 0 and self.concrete_blocks == 0):
                    self.button_start_label.enable()

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
        self.rect = self.gun_image.get_rect(center = tank.rect.center)
        self.angle = 0
        self.rotation_speed = 0
        self.tank = tank
        self.gun_length = 40
        self.gun_rotation_direction = 0
        self.tip_offset = 30
        self.original_gun_length = 0
        self.gun_back_start_time = 0
        self.gun_back_duration = 200
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.cooldown_duration = 500  #modifica el tiempo entre disparos del tanque
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

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x , y , angle):
        super().__init__()
        self.original_bullet_image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.original_bullet_image, (20,20))
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 4
        self.tank = Tank(375, 300)
        self.gun = Gun(self.tank)

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length+ self.gun.tip_offset - 32) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 32) * math.sin(angle_rad)


        self.rect = self.bullet_image.get_rect(center=(x+dx, y+dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        angle_rad = math.radians(self.angle)
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)
        self.rect.x += dx
        self.rect.y += dy

class WB(pygame.sprite.Sprite):
    def __init__(self, x , y , angle):
        super().__init__()
        self.original_bullet_image = pygame.image.load("assets/WB.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.original_bullet_image, (20,20))
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 4
        self.tank = Tank(375, 300)
        self.gun = Gun(self.tank)


        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length + self.gun.tip_offset - 32) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 32) * math.sin(angle_rad)


        self.rect = self.bullet_image.get_rect(center=(x+dx, y+dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        angle_rad = math.radians(self.angle)
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)
        self.rect.x += dx
        self.rect.y += dy

class BB(pygame.sprite.Sprite):
    def __init__(self, x , y , angle):
        super().__init__()
        self.original_bullet_image = pygame.image.load("assets/BB.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.original_bullet_image, (20,20))
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 4
        self.tank = Tank(375, 300)
        self.gun = Gun(self.tank)

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length+ self.gun.tip_offset - 32) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 32) * math.sin(angle_rad)


        self.rect = self.bullet_image.get_rect(center=(x+dx, y+dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        angle_rad = math.radians(self.angle)
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)
        self.rect.x += dx
        self.rect.y += dy

