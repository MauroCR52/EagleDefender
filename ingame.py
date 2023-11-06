import pygame
import pygame_gui
import button
from pygame import mixer
import math
import sys
import os
import json

from mutagen.mp3 import MP3
import time
import threading

from tkinter import messagebox
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UISelectionList




Bullet_type = ""
class InGame:
    def __init__(self, ancho, alto, rol, user1, user2):
        pygame.init()
        mixer.init()
        self.rol = rol
        self.user1 = user1
        self.user2 = user2
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Juego")
        self.background = pygame.image.load("assets/ingame_bg.png")
        self.gui_manager = pygame_gui.UIManager((ancho, alto), 'config/theme_ingame.json')
        self.cmusica = "Musica"
        self.canciones = []
        with open('config/users.json','r') as file:
            data = json.load(file)
            users = data['users']
            for user in users:
                if user['username'] == self.user1:
                    self.canciones = user['songs']

    #   self.canciones = [archivo for archivo in os.listdir(self.cmusica) if archivo.endswith('.mp3')]#os.listdir(self.cmusica)
        self.start = False
        self.TILE_TYPES = 7
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
        for i in range(len(self.img_list) - 4):
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

        self.tank = None
        self.gun = None
        self.all_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.balas_perdidas = 0
        self.max_disparosf = 0
        self.max_disparosw = 0
        self.max_disparosb = 0

        self.water_bullets_rest = 5
        self.bomb_bullets_rest = 5
        self.fire_bullets_rest = 5

        self.fuente = pygame.font.Font(None, 25)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.wood_blocks = 10
        self.steel_blocks = 10
        self.concrete_blocks = 10

        self.destroyed_wood_blocks = 0
        self.destroyed_steel_blocks = 0
        self.destroyed_concrete_blocks = 0

        self.destroyed_blocks = 0
        self.score = 0


        self.button_start = pygame.Rect(1220, 670, 130, 70)
        self.button_start_label = pygame_gui.elements.UIButton(relative_rect=self.button_start, text="Empezar", manager=self.gui_manager)

        self.eagle_img = pygame.image.load("assets/eagle.png")
        self.eagle_img = pygame.transform.scale(self.eagle_img,(self.TILE_SIZE - 1 , self.TILE_SIZE - 1))
        self.eagle_rect = self.eagle_img.get_rect()
        self.eagle_rect.center = (1150, 332)

        self.fire_img = pygame.image.load("assets/bullet.png")
        self.fire_img = pygame.transform.scale(self.fire_img,(self.TILE_SIZE - 1 , self.TILE_SIZE - 1))
        self.fire_rect = self.fire_img.get_rect()
        self.fire_rect.center = (1245, 460)

        self.water_img = pygame.image.load("assets/WB.png")
        self.water_img = pygame.transform.scale(self.water_img,(self.TILE_SIZE - 1 , self.TILE_SIZE - 1))
        self.water_rect = self.water_img.get_rect()
        self.water_rect.center = (1245, 530)

        self.bomb_img = pygame.image.load("assets/BB.png")
        self.bomb_img = pygame.transform.scale(self.bomb_img,(self.TILE_SIZE - 1 , self.TILE_SIZE - 1))
        self.bomb_rect = self.bomb_img.get_rect()
        self.bomb_rect.center = (1245, 600)


        self.song_window = None
        self.button_song = None
        self.song_selection = None

        self.inicio= time.time()

        self.texto_cronometro = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((500, 10), (200, 50)),
                                                            text="Tiempo: 00:00",
                                                            manager=self.gui_manager)

        self.attacker = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((80, 10), (200, 50)),
                                                            text="Atacante: ",
                                                            manager=self.gui_manager)

        self.defender = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((900, 10), (200, 50)),
                                                            text="Defensor: ",
                                                            manager=self.gui_manager)

        self.crono = pygame.time.Clock()
        self.inicio = None
        self.seleccion_actual = self.canciones[0]

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

    def open_song_list(self):
        self.current_tile = -1
        self.song_window = UIWindow(pygame.Rect((500, 150), (380, 360)), resizable= False,
                                    window_display_title= "Select Song", manager=self.gui_manager,
                                    draggable=False)

        self.button_song = UIButton(pygame.Rect(80, 20, 174, 30), 'Aceptar',
                          manager=self.gui_manager,
                          container=self.song_window)

        self.song_selection = UISelectionList(pygame.Rect(20, 70, 300, 200),
                                         item_list=self.canciones,
                                         manager=self.gui_manager,
                                         container=self.song_window,
                                         allow_multi_select=False)

        self.button_start_label.disable()

    def actualizar_cronometro(self, seleccion):
        while True:
            pygame.time.wait(100)
            if self.inicio is not None and seleccion == self.seleccion_actual:
                tiempo_transcurrido = (pygame.time.get_ticks() / 1000) - self.inicio

                # Calcula los minutos y segundos
                minutos = int(tiempo_transcurrido // 60)
                segundos = int(tiempo_transcurrido % 60)

                # Formatea el tiempo en minutos y segundos
                tiempo_formateado = f"Tiempo: {minutos:02d}:{segundos:02d}"

                self.texto_cronometro.set_text(tiempo_formateado)

                if tiempo_transcurrido >= self.duraA:
                    pygame.mixer.music.stop()
                    self.texto_cronometro.set_text(f"{tiempo_formateado}")
                    self.inicio = None
                    if self.rol == "defender":
                        messagebox.showinfo("Perdistes", "El defensor " + self.user1 + " gana")
                    else:
                        messagebox.showinfo("Perdistes", "El defensor " + self.user2 + " gana")


    def initGame(self):
        self.song_window.kill()
        self.song_window = None
        self.button_song = None
        self.song_selection = None

        self.audioplay = os.path.join(self.cmusica, self.seleccion)
        pygame.mixer.music.load(self.audioplay)
        pygame.mixer.music.play()
        self.audioD = MP3(self.audioplay)
        self.duraA = self.audioD.info.length
        self.inicio = pygame.time.get_ticks() / 1000
        self.tank = Tank(80,330)
        self.gun = Gun(self.tank)
        self.all_sprites.add(self.tank,self.gun)
        self.start = True


    def begin(self):

        if self.rol == "attacker":
            self.attacker.set_text("Atacante: "+ self.user1)
            self.defender.set_text("Defensor: "+ self.user2)
        else:
            self.attacker.set_text("Atacante: "+ self.user2)
            self.defender.set_text("Defensor: "+ self.user1)

        self.world_data[6][22] = -5
        cronometro_thread = threading.Thread(target=self.actualizar_cronometro, args=(self.seleccion_actual,))
        cronometro_thread.daemon = True
        cronometro_thread.start()
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas


        global Bullet_type
        while True:
                time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

                # salir del juego con la ventana
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if (event.type == pygame_gui.UI_WINDOW_CLOSE
                            and event.ui_element == self.song_window):
                        self.button_start_label.enable()
                        self.song_window = None
                        self.button_song = None
                        self.song_selection = None

                    if (event.type == pygame_gui.UI_BUTTON_PRESSED
                        and event.ui_element == self.button_song):
                        self.seleccion = self.song_selection.get_single_selection()
                        if self.seleccion == None:
                            messagebox.showinfo("Error", "Debes elegir una cancion")
                        else:
                            self.initGame()

                    if (event.type == pygame_gui.UI_BUTTON_PRESSED
                            and event.ui_element == self.button_start):
                            self.open_song_list()
                    # Pasar eventos de pygame a pygame_gui
                    self.gui_manager.process_events(event)  # Actualiza el administrador de interfaz de usuario de pygame_gui

                self.all_sprites.update()
                self.bullet_sprites.update()

                for y, row in enumerate(self.world_data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE,
                                                    self.TILE_SIZE)

                            if self.gun != None:


                                if tile_rect.colliderect(self.gun.rect) and self.world_data[y][x] >= 0:
                                    self.tank.choque = True


                                else:
                                    self.tank.choque = False







                for bullet in self.bullet_sprites:
                    if bullet.rect.x < 0 or bullet.rect.x > 1150:
                        bullet.kill()
                    if bullet.rect.y < 0 or bullet.rect.y > 740:
                        bullet.kill()
                    distance = math.sqrt((bullet.rect.centerx - bullet.start_x) ** 2 + (bullet.rect.centery - bullet.start_y) ** 2)
                    if distance > 8 * 51.2:
                        bullet.kill()

                    if self.eagle_rect.colliderect(bullet.rect):
                        if self.rol == "attacker":
                            messagebox.showinfo("Felicidades", "El atacante "+self.user1 + " gana")
                        else:
                            messagebox.showinfo("Felicidades", "El atacante "+self.user2 + " gana")
                        bullet.kill()

                    for y, row in enumerate(self.world_data):
                        for x, tile in enumerate(row):
                            if tile >= 0:
                                tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE,
                                                        self.TILE_SIZE)

                                if bullet.rect.colliderect(tile_rect):

                                    if self.world_data[y][x] == 0:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_wood_blocks += 1
                                        self.score += 5

                                    elif Bullet_type == "water" and self.world_data[y][x] == 1:
                                        self.world_data[y][x] = 5

                                    elif Bullet_type == "water" and self.world_data[y][x] == 5:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_steel_blocks += 1
                                        self.score += 10

                                    elif Bullet_type == "water" and self.world_data[y][x] == 2:
                                        self.world_data[y][x] = 4

                                    elif Bullet_type == "water" and self.world_data[y][x] == 4:
                                        self.world_data[y][x] = 6

                                    elif Bullet_type == "water" and self.world_data[y][x] == 6:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_concrete_blocks += 1
                                        self.score += 15

                                    elif Bullet_type == "fire" and self.world_data[y][x] == 1:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_steel_blocks += 1
                                        self.score += 10

                                    elif Bullet_type == "fire" and self.world_data[y][x] == 5:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_concrete_blocks += 1
                                        self.score += 15

                                    elif Bullet_type == "fire" and self.world_data[y][x] == 2:
                                        self.world_data[y][x] = 6

                                    elif Bullet_type == "fire" and self.world_data[y][x] == 4:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_steel_blocks += 1
                                        self.score += 10

                                    elif Bullet_type == "fire" and self.world_data[y][x] == 6:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_concrete_blocks += 1
                                        self.score += 15

                                    elif Bullet_type == "bomb" and self.world_data[y][x] == 1:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_steel_blocks += 1
                                        self.score += 10

                                    elif Bullet_type == "bomb" and self.world_data[y][x] == 2:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_concrete_blocks += 1
                                        self.score += 15

                                    elif Bullet_type == "bomb" and self.world_data[y][x] == 4:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_steel_blocks += 1
                                        self.score += 10

                                    elif Bullet_type == "bomb" and self.world_data[y][x] == 5:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_concrete_blocks += 1
                                        self.score += 15

                                    elif Bullet_type == "bomb" and self.world_data[y][x] == 6:
                                        self.world_data[y][x] = -1
                                        self.destroyed_blocks += 1
                                        self.destroyed_concrete_blocks += 1
                                        self.score += 15

                                    bullet.kill()



                self.texto = f"Balas\nperdidas: {self.balas_perdidas}"

                if self.start != True:
                    self.counter_0 = f"= {self.wood_blocks}"
                    self.counter_1 = f"= {self.steel_blocks}"
                    self.counter_2 = f"= {self.concrete_blocks}"
                if self.start == True:
                    self.counter_0 = f"= {self.destroyed_wood_blocks}"
                    self.counter_1 = f"= {self.destroyed_steel_blocks}"
                    self.counter_2 = f"= {self.destroyed_concrete_blocks}"


                self.counter_destroyed = f"Bloques\ndestruidos: {self.destroyed_blocks}"
                self.text_score = f"Puntaje: {self.score}"

                self.water_counter = f"= {self.water_bullets_rest}"
                self.fire_counter = f"= {self.fire_bullets_rest}"
                self.bomb_counter = f"= {self.bomb_bullets_rest}"


                self.texto_renderizado = self.fuente.render(self.texto, True, self.white)
                self.c_0_render = self.fuente.render(self.counter_0, True, self.white)
                self.c_1_render = self.fuente.render(self.counter_1, True, self.white)
                self.c_2_render = self.fuente.render(self.counter_2, True, self.white)
                self.c_destroyed = self.fuente.render(self.counter_destroyed, True, self.white)
                self.total_score = self.fuente.render(self.text_score, True, self.white)

                self.c_water = self.fuente.render(self.water_counter, True, self.white)
                self.c_fire = self.fuente.render(self.fire_counter, True, self.white)
                self.c_bomb = self.fuente.render(self.bomb_counter, True, self.white)

                self.gui_manager.update(time_delta)


                if self.gun != None:
                    if self.gun.can_shoot:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_SPACE] and self.max_disparosf < 5:
                            Bullet_type = "fire"
                            self.fire_bullets_rest-=1

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

                    self.bullet_sprites.update()

                    if self.gun.can_shoot:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_c] and self.max_disparosw < 5:
                            Bullet_type = "water"
                            self.water_bullets_rest-=1

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
                    self.bullet_sprites.update()

                    if self.gun.can_shoot:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_v] and self.max_disparosb < 5:
                            Bullet_type = "bomb"
                            self.bomb_bullets_rest-=1
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
                self.screen.blit(self.texto_renderizado, (1218, 280))
                self.screen.blit(self.c_0_render, (1280, 65))
                self.screen.blit(self.c_1_render, (1280, 140))
                self.screen.blit(self.c_2_render, (1280, 215))
                self.screen.blit(self.c_destroyed, (1218, 330))
                self.screen.blit(self.total_score, (1218, 390))
                self.screen.blit(self.eagle_img, self.eagle_rect)
                self.screen.blit(self.fire_img, self.fire_rect)
                self.screen.blit(self.water_img, self.water_rect)
                self.screen.blit(self.bomb_img, self.bomb_rect)

                self.screen.blit(self.c_fire, (1280, 450))
                self.screen.blit(self.c_water, (1280, 520))
                self.screen.blit(self.c_bomb, (1280, 590))



                # Dibuja los elementos de la interfaz de usuario de pygame_gui
                self.gui_manager.draw_ui(self.screen)
                self.bullet_sprites.draw(self.screen)

                for button_count, i in enumerate(self.button_list):
                    if i.draw(self.screen):
                        if self.start != True:
                            self.current_tile = button_count
                if self.start != True:
                    pygame.draw.rect(self.screen, (196, 12, 12), self.button_list[self.current_tile].rect, 3)

                pos = pygame.mouse.get_pos()
                x = (pos[0]) // self.TILE_SIZE
                y = pos[1] // self.TILE_SIZE

                #revisar que el mouse se encuentre dentro de la matriz
                if pos[0] < 1173 and pos[1] < 766:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if self.world_data[y][x] != self.current_tile:
                            # si el bloque aun no ha llegado a 0
                            if (self.world_data[y][x] != -5):
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
                    if self.start != True :
                        if pygame.mouse.get_pressed()[2] == 1:
                            if self.world_data[y][x] == 0:
                                self.wood_blocks += 1
                            if self.world_data[y][x] == 1:
                                self.steel_blocks += 1
                            if self.world_data[y][x] == 2:
                                self.concrete_blocks += 1
                            self.world_data[y][x] = -1

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
        self.choque = False


    def update(self):
        keys = pygame.key.get_pressed()

        self.speed_x = 0
        self.speed_y = 0

        if not self.choque:
            if keys[pygame.K_UP]:
                self.speed_y = -3
                self.angle = 90
                #move_forward_sound.play()
            elif keys[pygame.K_DOWN]:
                self.speed_y = 3
                self.angle = 270
                #move_forward_sound.play()


            if keys[pygame.K_LEFT]:
                self.speed_x = -3
                self.angle = 180
                #move_forward_sound.play()
            elif keys[pygame.K_RIGHT]:
                self.speed_x = 3
                self.angle = 0
                #move_forward_sound.play()

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

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
        elif keys[pygame.K_UP]:
            self.angle = 90
        elif keys[pygame.K_DOWN]:
            self.angle = 270
        elif keys[pygame.K_LEFT]:
            self.angle = 180
        elif keys[pygame.K_RIGHT]:
            self.angle = 0
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
        self.speed = 1.5
        self.tank = Tank(375, 300)
        self.gun = Gun(self.tank)
        self.bullet_type = "fire_bullet"
        self.max_distance = 8 * 51.2

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length + self.gun.tip_offset - 82) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 82) * math.sin(angle_rad)

        self.rect = self.bullet_image.get_rect(center=(x + dx, y + dy))
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
        self.speed = 1.5
        self.tank = Tank(375, 300)
        self.gun = Gun(self.tank)
        self.bullet_type = "water"

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length + self.gun.tip_offset - 82) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 82) * math.sin(angle_rad)


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
        self.speed = 1.5
        self.tank = Tank(375, 300)
        self.gun = Gun(self.tank)
        self.bullet_type = "bomb_bullet"

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length+ self.gun.tip_offset - 82) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 82) * math.sin(angle_rad)


        self.rect = self.bullet_image.get_rect(center=(x+dx, y+dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        angle_rad = math.radians(self.angle)
        dx = self.speed * math.cos(angle_rad)
        dy = -self.speed * math.sin(angle_rad)
        self.rect.x += dx
        self.rect.y += dy

class Song(UIWindow):
    def __init__(self, rect, ui_manager, song_list):
        super().__init__(rect, ui_manager,
                         window_display_title='Select Song',
                         resizable=False)
        self.song_list = song_list

        self.button = UIButton(pygame.Rect(20, 10, 174, 30), 'Aceptar',
                 manager=self.ui_manager,
                 container=self)

        self.song_selection = UISelectionList(pygame.Rect(20, 70, 300, 200),
                        item_list=self.song_list,
                        manager=self.ui_manager,
                        container=self,
                        allow_multi_select=False)
    def update(self, time_delta):
        super().update(time_delta)
