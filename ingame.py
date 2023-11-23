import pygame
import pygame_gui
import button
from pygame import mixer
import math
import sys
import os
import json
import random
from mutagen.mp3 import MP3
import time
import threading
import csv
from tkinter import messagebox
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UISelectionList
from datetime import datetime
Bullet_type = ""
pause = False



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
        with open('config/users.json', 'r') as file:
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
        for i in range(len(self.img_list) - 3):
            tile_button = button.Button(1168 + (75 * self.button_col) + 50, 75 * self.button_row + 50, self.img_list[i],
                                        1)
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

        self.water_bullets_rest = 5
        self.bomb_bullets_rest = 5
        self.fire_bullets_rest = 5

        self.fuente = pygame.font.Font(None, 25)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.wood_blocks = 10
        self.steel_blocks = 10
        self.concrete_blocks = 10
        self.eagle_block = 1

        self.placed_blocks = 0
        self.destroyed_blocks = 0
        self.normal_bullets = self.water_bullets_rest
        self.power_activation = True

        self.destroyed_wood_blocks = 0
        self.destroyed_steel_blocks = 0
        self.destroyed_concrete_blocks = 0

        self.score = 0

        self.button_start = pygame.Rect(1220, 670, 130, 70)
        self.button_start_label = pygame_gui.elements.UIButton(relative_rect=self.button_start, text="Empezar",
                                                               manager=self.gui_manager)

        self.fire_img = pygame.image.load("assets/bullet.png")
        self.fire_img = pygame.transform.scale(self.fire_img, (self.TILE_SIZE - 1, self.TILE_SIZE - 1))
        self.fire_rect = self.fire_img.get_rect()
        self.fire_rect.center = (1245, 460)

        self.water_img = pygame.image.load("assets/WB.png")
        self.water_img = pygame.transform.scale(self.water_img, (self.TILE_SIZE - 1, self.TILE_SIZE - 1))
        self.water_rect = self.water_img.get_rect()
        self.water_rect.center = (1245, 530)

        self.bomb_img = pygame.image.load("assets/BB.png")
        self.bomb_img = pygame.transform.scale(self.bomb_img, (self.TILE_SIZE - 1, self.TILE_SIZE - 1))
        self.bomb_rect = self.bomb_img.get_rect()
        self.bomb_rect.center = (1245, 600)

        self.song_window = None
        self.button_song = None
        self.song_selection = None

        self.inicio = time.time()

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

        self.minutes_half = None
        self.seconds_half = None

        self.song_name = ""
        self.tempo = ""
        self.popularity = ""
        self.danceability = ""
        self.acousticness = ""

        self.cronometro = True

        self.pause_start = None
        self.tiempo_transcurrido_total = 0
    def draw_world(self):
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    self.screen.blit(self.img_list[tile], (x * self.TILE_SIZE, y * self.TILE_SIZE))

    def draw_grid(self):
        for c in range(self.COLS + 1):
            pygame.draw.line(self.screen, self.white, (c * self.TILE_SIZE, 0), (c * self.TILE_SIZE, 766))
        for c in range(self.ROWS + 1):
            pygame.draw.line(self.screen, self.white, (0, c * self.TILE_SIZE), (1173, c * self.TILE_SIZE))

    def draw_pause(self):
        background = pygame.image.load("assets/help_bg.png")
        self.screen.blit(background, (0, 0))


    def open_song_list(self):
        self.current_tile = -1
        self.song_window = UIWindow(pygame.Rect((500, 150), (380, 360)), resizable=False,
                                    window_display_title="Select Song", manager=self.gui_manager,
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

    #def actualizar_cronometro(self, seleccion):
    #     while self.cronometro:
    #         pygame.time.wait(100)
    #         if self.inicio is not None and seleccion == self.seleccion_actual:
    #             tiempo_transcurrido = (pygame.time.get_ticks() / 1000) - self.inicio
    #
    #             # Calcula los minutos y segundos
    #             self.minutos = int(tiempo_transcurrido // 60)
    #             self.segundos = int(tiempo_transcurrido % 60)
    #
    #             # Formatea el tiempo en minutos y segundos
    #             self.tiempo_formateado = f"Tiempo: {self.minutos:02d}:{self.segundos:02d}"
    #
    #             self.texto_cronometro.set_text(self.tiempo_formateado)
    #
    #             # if self.duraA / 2 - 0.5 <= tiempo_transcurrido <= self.duraA / 2 + 0.5:
    #             # if self.destroyed_blocks >= self.placed_blocks // 2:
    #             # print("se puede usar el poder")
    #             # pygame.time.set_timer(pygame.USEREVENT + 1, 10000)
    #             # while():
    #             # if self.power_activation == True:
    #             # self.water_bullets_rest = round(self.water_bullets_rest + (int(self.popularity) / float(self.danceability) * float(self.acousticness) + float(self.tempo)))
    #             # self.power_activation = False
    #             # self.water_bullets_rest = self.normal_bullets
    #             # else:
    #             # print("no se puede usar el poder")
    #
    #             if tiempo_transcurrido >= self.duraA:
    #                 pygame.mixer.music.stop()
    #                 self.texto_cronometro.set_text(f"{self.tiempo_formateado}")
    #                 self.inicio = None
    #                 if self.rol == "defender":
    #                     messagebox.showinfo("Perdistes", "El defensor " + self.user1 + " gana")
    #                 else:
    #                     messagebox.showinfo("Perdistes", "El defensor " + self.user2 + " gana")
    #
    # # def activate_power(self):

    # Función para obtener una canción aleatoria de un usuario específico
    def obtener_cancion_aleatoria(self, usuario):
        with open('config/users.json', 'r') as file:
            data = json.load(file)
            users = data['users']
            # Busca el usuario en la lista de usuarios
            for usuario_actual in users:
                if usuario_actual["username"] == usuario:
                    # Si encuentra al usuario, elige una canción aleatoria
                    cancion_aleatoria = random.choice(usuario_actual["songs"])
                    self.seleccion = cancion_aleatoria
            # Si no se encuentra el usuario, devuelve None o maneja el caso según tus necesidades
            return None

    # Función para convertir el tiempo de minutos y segundos a segundos totales
    def convertir_tiempo_a_segundos(self, tiempo):
        minutos, segundos = map(int, tiempo.split(':'))
        return minutos * 60 + segundos

    def verificar_leaderboard(self, usuario, tiempo):
        with open("config/leaderboard.csv", 'r') as file:
            # Lee el archivo CSV
            csv_reader = csv.reader(file)

            # Salta la primera línea (encabezado)
            next(csv_reader)

            # Inicializa un contador para llevar la cuenta de las filas leídas
            contador = 0

            # Itera sobre las filas del archivo
            for row in csv_reader:
                # Incrementa el contador
                contador += 1

                # Obtiene los valores de la fila
                nombre = row[0]
                tiempo_fila = row[1]
                print(f"{nombre} - {usuario}" )
                print(f"{tiempo_fila} - {tiempo}" )


                # Compara con el usuario y tiempo especificado
                if nombre == usuario and tiempo_fila == tiempo:
                    return True

                # Si hemos llegado a las primeras 5 filas, salimos del bucle
                if contador >= 5:
                    break

            # Si no se encontró la combinación usuario-tiempo
            return False

    def initGame(self):
        with open('config/songs.json', 'r') as file:
            data = json.load(file)
        # Buscar la canción en la lista de canciones
        for cancion in data["songs"]:
            if cancion["song"] == self.seleccion:
                # Acceder a los datos específicos
                self.song_name = cancion["song"]
                self.tempo = cancion["tempo"]
                self.popularity = cancion["popularity"]
                self.danceability = cancion["danceability"]
                self.acousticness = cancion["acoustic"]
                break
        else:
            # Este bloque se ejecutará si el bucle no se rompe, es decir, si no se encuentra la canción
            print(f"No se encontró la canción")

        self.button_start_label.disable()
        self.audioplay = os.path.join(self.cmusica, self.seleccion)
        pygame.mixer.music.load(self.audioplay)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.05)
        self.audioD = MP3(self.audioplay)
        self.duraA = self.audioD.info.length
        self.inicio = pygame.time.get_ticks() / 1000
        self.tank = Tank(80, 330, self.world_data, self.TILE_SIZE)
        self.gun = Gun(self.tank)
        self.all_sprites.add(self.tank, self.gun)
        self.start = True

    def begin(self):
        global pause

        if self.rol == "attacker":
            self.attacker.set_text("Atacante: " + self.user1)
            self.defender.set_text("Defensor: " + self.user2)
        else:
            self.attacker.set_text("Atacante: " + self.user2)
            self.defender.set_text("Defensor: " + self.user1)

        # cronometro_thread = threading.Thread(target=self.actualizar_cronometro, args=(self.seleccion_actual,))
        # cronometro_thread.daemon = True
        # cronometro_thread.start()

        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        global Bullet_type
        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            if self.inicio is not None:
                if not pause:

                    tiempo_transcurrido = (pygame.time.get_ticks() / 1000) - self.inicio
                    self.tiempo_transcurrido_total += tiempo_transcurrido  # Actualiza el contador total
                    # Calcula los minutos y segundos
                    self.minutos = int(tiempo_transcurrido // 60)
                    self.segundos = int(tiempo_transcurrido % 60)

                    # Formatea el tiempo en minutos y segundos
                    self.tiempo_formateado = f"Tiempo: {self.minutos:02d}:{self.segundos:02d}"

                    self.texto_cronometro.set_text(self.tiempo_formateado)

                    # if self.duraA / 2 - 0.5 <= tiempo_transcurrido <= self.duraA / 2 + 0.5:
                    # if self.destroyed_blocks >= self.placed_blocks // 2:
                    # print("se puede usar el poder")
                    # pygame.time.set_timer(pygame.USEREVENT + 1, 10000)
                    # while():
                    # if self.power_activation == True:
                    # self.water_bullets_rest = round(self.water_bullets_rest + (int(self.popularity) / float(self.danceability) * float(self.acousticness) + float(self.tempo)))
                    # self.power_activation = False
                    # self.water_bullets_rest = self.normal_bullets
                    # else:
                    # print("no se puede usar el poder")

                    if tiempo_transcurrido >= self.duraA:
                        pygame.mixer.music.stop()
                        self.texto_cronometro.set_text(f"{self.tiempo_formateado}")
                        self.inicio = None
                        if self.rol == "defender":
                            messagebox.showinfo("Perdistes", "El defensor " + self.user1 + " gana")
                        else:
                            messagebox.showinfo("Perdistes", "El defensor " + self.user2 + " gana")
                else:
                    # Si el juego está en pausa, actualiza el tiempo de pausa
                    self.tiempo_pausa = (pygame.time.get_ticks() / 1000) - self.inicio

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_ESCAPE:
                        if pause:
                            self.inicio = pygame.time.get_ticks() / 1000
                            pause = False
                            pygame.mixer.music.unpause()


                        else:
                            self.inicio = None

                            pause = True
                            pygame.mixer.music.pause()



                if (event.type == pygame_gui.UI_WINDOW_CLOSE
                        and event.ui_element == self.song_window):
                    self.button_start_label.enable()
                    self.song_window = None
                    self.button_song = None
                    self.song_selection = None

                if (event.type == pygame_gui.UI_BUTTON_PRESSED
                        and event.ui_element == self.button_song and not pause):
                    self.seleccion = self.song_selection.get_single_selection()
                    if self.seleccion == None:
                        messagebox.showinfo("Error", "Debes elegir una cancion")
                    else:
                        self.initGame()

                if (event.type == pygame_gui.UI_BUTTON_PRESSED
                        and event.ui_element == self.button_start and not pause):
                    if self.eagle_block == 0:
                        self.obtener_cancion_aleatoria(self.user1)
                        self.current_tile = -1
                        self.initGame()

                        # self.open_song_list()
                    else:
                        messagebox.showinfo("Error", "Debes colocar el águila")
                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui

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
                distance = math.sqrt(
                    (bullet.rect.centerx - bullet.start_x) ** 2 + (bullet.rect.centery - bullet.start_y) ** 2)
                if distance > 8 * 51.2:
                    bullet.kill()

                for y, row in enumerate(self.world_data):
                    for x, tile in enumerate(row):
                        if tile >= 0:
                            tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE,
                                                    self.TILE_SIZE)

                            if bullet.rect.colliderect(tile_rect):

                                if self.world_data[y][x] == 3:
                                    self.cronometro = False
                                    from interfaz import Menu_window
                                    pygame.mixer.music.stop()
                                    self.world_data[y][x] = -1
                                    if self.rol == "attacker":
                                        with open("config/leaderboard.csv", 'a', newline='') as archivo:
                                            with open('config/users.json', 'r') as file:
                                                data = json.load(file)
                                                users = data['users']
                                                for user in users:
                                                    if user['username'] == self.user1:
                                                        image_path = user['profile_pic']

                                            # Crea un objeto escritor de CSV
                                            escritor_csv = csv.writer(archivo)

                                            # Escribe una nueva fila con el nombre y el número
                                            escritor_csv.writerow(
                                                [self.user1, f"{self.minutos:02d}:{self.segundos:02d}", image_path])

                                        with open("config/leaderboard.csv", 'r', newline='') as file:
                                            # Lee los datos del archivo CSV
                                            reader = csv.reader(file)
                                            header = next(
                                                reader)  # Lee la primera fila (encabezado) y la guarda en 'header'
                                            filas = list(
                                                reader)  # Lee el resto de las filas y las guarda en 'filas'

                                        # Ordena las filas por tiempo, utilizando la función convertir_tiempo_a_segundos
                                        filas_ordenadas = sorted(filas,
                                                                 key=lambda x: self.convertir_tiempo_a_segundos(x[1]))

                                        # Escribe las filas ordenadas de nuevo en el archivo CSV
                                        with open("config/leaderboard.csv", 'w', newline='') as file:
                                            writer = csv.writer(file)
                                            writer.writerow(header)  # Escribe el encabezado
                                            writer.writerows(filas_ordenadas)  # Escribe las filas ordenadas

                                        messagebox.showinfo("Ganaste", "El atacante " + self.user1 + " gana")
                                        leaderboard = self.verificar_leaderboard(self.user1,f"{self.minutos:02d}:{self.segundos:02d}")
                                        if leaderboard:
                                            messagebox.showinfo("Felicidades", "El atacante " + self.user1 + " entró al salon de la fama")
                                        else:
                                            messagebox.showinfo("Lo siento", "El atacante " + self.user1 + " no pudo entrar al salon de la fama")



                                        menu = Menu_window(1366, 768, self.user1)
                                        menu.begin()

                                    else:
                                        with open("config/leaderboard.csv", 'a', newline='') as archivo:
                                            with open('config/users.json', 'r') as file:
                                                data = json.load(file)
                                                users = data['users']
                                                for user in users:
                                                    if user['username'] == self.user2:
                                                        image_path = user['profile_pic']

                                            # Crea un objeto escritor de CSV
                                            escritor_csv = csv.writer(archivo)

                                            # Escribe una nueva fila con el nombre y el número
                                            escritor_csv.writerow(
                                                [self.user2, f"{self.minutos:02d}:{self.segundos:02d}", image_path])

                                        with open("config/leaderboard.csv", 'r', newline='') as file:
                                            # Lee los datos del archivo CSV
                                            reader = csv.reader(file)
                                            header = next(
                                                reader)  # Lee la primera fila (encabezado) y la guarda en 'header'
                                            filas = list(
                                                reader)  # Lee el resto de las filas y las guarda en 'filas'

                                            # Ordena las filas por tiempo, utilizando la función convertir_tiempo_a_segundos
                                        filas_ordenadas = sorted(filas,
                                                                 key=lambda x: self.convertir_tiempo_a_segundos(
                                                                     x[1]))

                                        # Escribe las filas ordenadas de nuevo en el archivo CSV
                                        with open("config/leaderboard.csv", 'w', newline='') as file:
                                            writer = csv.writer(file)
                                            writer.writerow(header)  # Escribe el encabezado
                                            writer.writerows(filas_ordenadas)  # Escribe las filas ordenadas

                                        messagebox.showinfo("Ganaste", "El atacante " + self.user2 + " gana")

                                        leaderboard = self.verificar_leaderboard(self.user2,f"{self.minutos:02d}:{self.segundos:02d}")
                                        if leaderboard:
                                            messagebox.showinfo("Felicidades", "El atacante " + self.user2 + " entró al salon de la fama")
                                        else:
                                            messagebox.showinfo("Lo siento", "El atacante " + self.user2 + " no pudo entrar al salon de la fama")

                                        menu = Menu_window(1366, 768, self.user1)
                                        menu.begin()


                                elif self.world_data[y][x] == 0:
                                    self.world_data[y][x] = -1
                                    self.destroyed_wood_blocks += 1
                                    self.score += 5
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "water" and self.world_data[y][x] == 1:
                                    self.world_data[y][x] = 5

                                elif Bullet_type == "water" and self.world_data[y][x] == 5:
                                    self.world_data[y][x] = -1
                                    self.destroyed_steel_blocks += 1
                                    self.score += 10
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "water" and self.world_data[y][x] == 2:
                                    self.world_data[y][x] = 4

                                elif Bullet_type == "water" and self.world_data[y][x] == 4:
                                    self.world_data[y][x] = 6

                                elif Bullet_type == "water" and self.world_data[y][x] == 6:
                                    self.world_data[y][x] = -1
                                    self.destroyed_concrete_blocks += 1
                                    self.score += 15
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "fire" and self.world_data[y][x] == 1:
                                    self.world_data[y][x] = -1
                                    self.destroyed_steel_blocks += 1
                                    self.score += 10
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "fire" and self.world_data[y][x] == 5:
                                    self.world_data[y][x] = -1
                                    self.destroyed_steel_blocks += 1
                                    self.score += 15
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "fire" and self.world_data[y][x] == 2:
                                    self.world_data[y][x] = 6

                                elif Bullet_type == "fire" and self.world_data[y][x] == 4:
                                    self.world_data[y][x] = -1
                                    self.destroyed_concrete_blocks += 1
                                    self.score += 10
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "fire" and self.world_data[y][x] == 6:
                                    self.world_data[y][x] = -1
                                    self.destroyed_concrete_blocks += 1
                                    self.score += 15
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "bomb" and self.world_data[y][x] == 1:
                                    self.world_data[y][x] = -1
                                    self.destroyed_steel_blocks += 1
                                    self.score += 10
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "bomb" and self.world_data[y][x] == 2:
                                    self.world_data[y][x] = -1
                                    self.destroyed_concrete_blocks += 1
                                    self.score += 15
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "bomb" and self.world_data[y][x] == 4:
                                    self.world_data[y][x] = -1
                                    self.destroyed_concrete_blocks += 1
                                    self.score += 10
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "bomb" and self.world_data[y][x] == 5:
                                    self.world_data[y][x] = -1
                                    self.destroyed_steel_blocks += 1
                                    self.score += 15
                                    self.destroyed_blocks += 1

                                elif Bullet_type == "bomb" and self.world_data[y][x] == 6:
                                    self.world_data[y][x] = -1
                                    self.destroyed_concrete_blocks += 1
                                    self.score += 15
                                    self.destroyed_blocks += 1
                                bullet.kill()
                                print(self.destroyed_blocks)

            self.texto = f"Balas\nperdidas: {self.balas_perdidas}"

            self.counter_eagle = f"= {self.eagle_block}"

            self.counter_song = f"Cancion: {self.song_name}"
            self.counter_popularity = f"Popularidad: {self.popularity}"
            self.counter_tempo = f"Tempo: {self.tempo}"
            self.counter_danceability = f"Bailabilidad: {self.danceability}"
            self.counter_accousticness = f"Acústico: {self.acousticness}"

            if self.start != True:
                self.counter_0 = f"= {self.wood_blocks}"
                self.counter_1 = f"= {self.steel_blocks}"
                self.counter_2 = f"= {self.concrete_blocks}"
            if self.start == True:
                self.counter_0 = f"= {self.destroyed_wood_blocks}"
                self.counter_1 = f"= {self.destroyed_steel_blocks}"
                self.counter_2 = f"= {self.destroyed_concrete_blocks}"

            self.text_score = f"Puntaje: {self.score}"

            self.water_counter = f"= {self.water_bullets_rest}"
            self.fire_counter = f"= {self.fire_bullets_rest}"
            self.bomb_counter = f"= {self.bomb_bullets_rest}"

            self.texto_renderizado = self.fuente.render(self.texto, True, self.white)
            self.c_0_render = self.fuente.render(self.counter_0, True, self.white)
            self.c_1_render = self.fuente.render(self.counter_1, True, self.white)
            self.c_2_render = self.fuente.render(self.counter_2, True, self.white)
            self.eagle_counter_render = self.fuente.render(self.counter_eagle, True, self.white)

            self.song_render = self.fuente.render(self.counter_song, True, self.black)
            self.tempo_render = self.fuente.render(self.counter_tempo, True, self.black)
            self.popularity_render = self.fuente.render(self.counter_popularity, True, self.black)
            self.acousticness_render = self.fuente.render(self.counter_accousticness, True, self.black)
            self.danceability_render = self.fuente.render(self.counter_danceability, True, self.black)

            self.total_score = self.fuente.render(self.text_score, True, self.white)

            self.c_water = self.fuente.render(self.water_counter, True, self.white)
            self.c_fire = self.fuente.render(self.fire_counter, True, self.white)
            self.c_bomb = self.fuente.render(self.bomb_counter, True, self.white)

            self.gui_manager.update(time_delta)

            if self.gun != None:
                if not pause:
                    if self.gun.can_shoot:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_SPACE] and self.fire_bullets_rest != 0:
                            Bullet_type = "fire"
                            self.fire_bullets_rest -= 1

                            bullet_angle = self.gun.angle
                            bullet_x = self.gun.rect.centerx + (self.gun.gun_length + self.gun.tip_offset) * math.cos(
                                math.radians(bullet_angle))
                            bullet_y = self.gun.rect.centery - (self.gun.gun_length + self.gun.tip_offset) * math.sin(
                                math.radians(bullet_angle))
                            bullet = Bullet(bullet_x, bullet_y, bullet_angle, self.world_data, self.TILE_SIZE)
                            self.all_sprites.add(bullet)
                            self.bullet_sprites.add(bullet)
                            self.gun.can_shoot = False
                            self.gun.shoot_cooldown = self.gun.cooldown_duration
                            self.balas_perdidas += 1

                    self.bullet_sprites.update()

                    if self.gun.can_shoot:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_c] and self.water_bullets_rest != 0:
                            Bullet_type = "water"
                            self.water_bullets_rest -= 1

                            bullet_angle = self.gun.angle
                            bullet_x = self.gun.rect.centerx + (self.gun.gun_length + self.gun.tip_offset) * math.cos(
                                math.radians(bullet_angle))
                            bullet_y = self.gun.rect.centery - (self.gun.gun_length + self.gun.tip_offset) * math.sin(
                                math.radians(bullet_angle))
                            self.waterbullet = WB(bullet_x, bullet_y, bullet_angle, self.world_data, self.TILE_SIZE)
                            self.all_sprites.add(self.waterbullet)
                            self.bullet_sprites.add(self.waterbullet)
                            self.gun.can_shoot = False
                            self.gun.shoot_cooldown = self.gun.cooldown_duration
                            self.balas_perdidas += 1
                    self.bullet_sprites.update()

                    if self.gun.can_shoot:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_v] and self.bomb_bullets_rest != 0:
                            Bullet_type = "bomb"
                            self.bomb_bullets_rest -= 1
                            bullet_angle = self.gun.angle
                            bullet_x = self.gun.rect.centerx + (self.gun.gun_length + self.gun.tip_offset) * math.cos(
                                math.radians(bullet_angle))
                            bullet_y = self.gun.rect.centery - (self.gun.gun_length + self.gun.tip_offset) * math.sin(
                                math.radians(bullet_angle))
                            bombbullet = BB(bullet_x, bullet_y, bullet_angle, self.world_data, self.TILE_SIZE)
                            self.all_sprites.add(bombbullet)
                            self.bullet_sprites.add(bombbullet)
                            self.gun.can_shoot = False
                            self.gun.shoot_cooldown = self.gun.cooldown_duration
                            self.balas_perdidas += 1
                    self.bullet_sprites.update()

            self.screen.blit(self.background, (0, 0))
            self.draw_grid()
            self.draw_world()
            self.screen.blit(self.texto_renderizado, (1218, 330))
            self.screen.blit(self.c_0_render, (1280, 65))
            self.screen.blit(self.c_1_render, (1280, 140))
            self.screen.blit(self.c_2_render, (1280, 215))
            self.screen.blit(self.eagle_counter_render, (1280, 290))

            self.screen.blit(self.song_render, (10, 660))
            self.screen.blit(self.tempo_render, (10, 680))
            self.screen.blit(self.popularity_render, (10, 700))
            self.screen.blit(self.acousticness_render, (10, 720))
            self.screen.blit(self.danceability_render, (10, 740))

            self.screen.blit(self.total_score, (1218, 390))
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

            # revisar que el mouse se encuentre dentro de la matriz
            if pos[0] < 1173 and pos[1] < 766:
                if not pause:
                    if pygame.mouse.get_pressed()[0] == 1:
                        if self.world_data[y][x] != self.current_tile:
                            if (self.current_tile == 3 and self.eagle_block != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.eagle_block -= 1
                                    self.placed_blocks += 1
                            elif (self.current_tile == 0 and self.wood_blocks != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.wood_blocks -= 1
                                    self.placed_blocks += 1
                            elif (self.current_tile == 1 and self.steel_blocks != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.steel_blocks -= 1
                                    self.placed_blocks += 1
                            elif (self.current_tile == 2 and self.concrete_blocks != 0):
                                if self.world_data[y][x] == -1:
                                    self.world_data[y][x] = self.current_tile
                                    self.concrete_blocks -= 1
                                    self.placed_blocks += 1
                    if self.start != True:
                        if pygame.mouse.get_pressed()[2] == 1:
                            if self.world_data[y][x] == 0:
                                self.wood_blocks += 1
                                self.placed_blocks -= 1
                            if self.world_data[y][x] == 1:
                                self.steel_blocks += 1
                                self.placed_blocks -= 1
                            if self.world_data[y][x] == 2:
                                self.concrete_blocks += 1
                                self.placed_blocks -= 1
                            if self.world_data[y][x] == 3:
                                self.eagle_block += 1
                                self.placed_blocks -= 1
                            self.world_data[y][x] = -1
                            print(self.placed_blocks)



            self.all_sprites.draw(self.screen)
            if pause:
                self.draw_pause()

            pygame.display.update()


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, world_data, TILE_SIZE):
        super().__init__()
        self.original_tank_image = pygame.image.load("assets/tr2.png").convert_alpha()
        self.tank_image = pygame.transform.scale(self.original_tank_image, (60, 50))
        self.image = self.tank_image
        self.rect = self.tank_image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 0
        self.rotation_speed = 0
        self.choque = False
        self.world_data = world_data
        self.TILE_SIZE = TILE_SIZE

    def update(self):
        keys = pygame.key.get_pressed()

        self.speed_x = 0
        self.speed_y = 0

        if not pause:
            if keys[pygame.K_UP]:
                self.speed_y = -3
                self.angle = 90
                # move_forward_sound.play()
            elif keys[pygame.K_DOWN]:
                self.speed_y = 3
                self.angle = 270
                # move_forward_sound.play()

            if keys[pygame.K_LEFT]:
                self.speed_x = -3
                self.angle = 180
                # move_forward_sound.play()
            elif keys[pygame.K_RIGHT]:
                self.speed_x = 3
                self.angle = 0
                # move_forward_sound.play()

            old_x, old_y = self.rect.x, self.rect.y

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            self.image = pygame.transform.rotate(self.tank_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            for y, row in enumerate(self.world_data):
                for x, tile in enumerate(row):
                    if tile >= 0:
                        tile_rect = pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE+5, self.TILE_SIZE-10,
                                                self.TILE_SIZE-10)

                        if self.rect.colliderect(tile_rect):
                            self.rect.x, self.rect.y = old_x, old_y




            angle_rad = math.radians(self.angle)
            dx = math.cos(angle_rad) * self.speed
            dy = math.sin(angle_rad) * self.speed

            self.rect.x += dx
            self.rect.y -= dy


class Gun(pygame.sprite.Sprite):
    def __init__(self, tank):
        super().__init__()
        self.tank = tank
        self.original_gun_image = pygame.image.load("assets/gr3.png").convert_alpha()
        self.gun_image = pygame.transform.scale(self.original_gun_image, (60, 30))
        self.image = self.gun_image
        self.rect = self.gun_image.get_rect(center=self.tank.rect.center)
        self.angle = 0
        self.rotation_speed = 0
        self.tank = tank
        self.gun_length = 22
        self.gun_rotation_direction = 0
        self.tip_offset = 25
        self.original_gun_length = 0
        self.gun_back_start_time = 0
        self.gun_back_duration = 200
        self.can_shoot = True
        self.shoot_cooldown = 0
        self.cooldown_duration = 500  # modifica el tiempo entre disparos del tanque
        self.last_update_time = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()

        if not pause:

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

        self.image = pygame.transform.rotate(self.gun_image, self.angle)
        self.rect = self.image.get_rect(center=self.tank.rect.center)

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
    def __init__(self, x, y, angle, world_data, TILE_SIZE):
        super().__init__()
        self.original_bullet_image = pygame.image.load("assets/bullet.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.original_bullet_image, (20, 20))
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 1.5
        self.tank = Tank(375, 3000, world_data, TILE_SIZE)
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
        if not pause:
            angle_rad = math.radians(self.angle)
            dx = self.speed * math.cos(angle_rad)
            dy = -self.speed * math.sin(angle_rad)
            self.rect.x += dx
            self.rect.y += dy


class WB(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, world_data, TILE_SIZE):
        super().__init__()
        self.original_bullet_image = pygame.image.load("assets/WB.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.original_bullet_image, (20, 20))
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 1.5
        self.tank = Tank(375, 300, world_data, TILE_SIZE)
        self.gun = Gun(self.tank)
        self.bullet_type = "water"

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length + self.gun.tip_offset - 82) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 82) * math.sin(angle_rad)

        self.rect = self.bullet_image.get_rect(center=(x + dx, y + dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        if not pause:
            angle_rad = math.radians(self.angle)
            dx = self.speed * math.cos(angle_rad)
            dy = -self.speed * math.sin(angle_rad)
            self.rect.x += dx
            self.rect.y += dy


class BB(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, world_data, TILE_SIZE):
        super().__init__()
        self.original_bullet_image = pygame.image.load("assets/BB.png").convert_alpha()
        self.bullet_image = pygame.transform.scale(self.original_bullet_image, (20, 20))
        self.image = self.bullet_image
        self.angle = angle
        self.speed = 1.5
        self.tank = Tank(375, 300, world_data, TILE_SIZE)
        self.gun = Gun(self.tank)
        self.bullet_type = "bomb_bullet"

        angle_rad = math.radians(self.angle)

        dx = (self.gun.gun_length + self.gun.tip_offset - 82) * math.cos(angle_rad)
        dy = -(self.gun.gun_length + self.gun.tip_offset - 82) * math.sin(angle_rad)

        self.rect = self.bullet_image.get_rect(center=(x + dx, y + dy))
        self.start_x = self.rect.centerx
        self.start_y = self.rect.centery

    def update(self):
        if not pause:
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
