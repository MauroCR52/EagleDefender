import csv
import json
import sys
import pygame
import pygame_gui
from pygame import mixer
from pygame_gui.elements import UIImage, UITextBox
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path
from tkinter import messagebox
from ingame import InGame
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UIButton
from pygame_gui.elements import UISelectionList
import os


class Login_window:
    def __init__(self, ancho, alto):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Login")
        self.background = pygame.image.load("assets/login_bg.png")

        # Inicializar el administrador de interfaz de usuario de pygame_gui
        self.gui_manager = pygame_gui.UIManager((ancho, alto), starting_language='es',
                                                translation_directory_paths=['config/translation'])

        # Crear un ComboBox
        languages_list = ['pygame-gui.English',
                          'pygame-gui.Spanish']
        self.combo_box = pygame_gui.elements.UIDropDownMenu(languages_list, 'pygame-gui.Spanish',
                                                            relative_rect=pygame.Rect(25, 30, 150, 50),
                                                            manager=self.gui_manager)

        # Cuadros de texto del Login
        self.username_rect = pygame.Rect(850, 220, 350, 45)
        self.password_rect = pygame.Rect(850, 330, 350, 45)

        # Botones
        self.button_signin = pygame.Rect(920, 430, 150, 70)
        self.button_signup = pygame.Rect(920, 520, 150, 70)

        # Crear un cuadro de entrada
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.username_rect,
                                                                  manager=self.gui_manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_rect,
                                                                  manager=self.gui_manager)
        self.password_entry.set_text_hidden(True)

        self.button_signin_label = pygame_gui.elements.UIButton(relative_rect=self.button_signin,
                                                                text="language.sign_in", manager=self.gui_manager)
        self.button_signup_label = pygame_gui.elements.UIButton(relative_rect=self.button_signup,
                                                                text="language.sign_up", manager=self.gui_manager)

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_signin:
                        self.signIn()
                    elif event.ui_element == self.button_signup:
                        signup_window = SignUp_Window(1366, 768)
                        signup_window.begin()

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    global language_set
                    if event.text == 'pygame-gui.English':
                        self.gui_manager.set_locale('en')
                    elif event.text == 'pygame-gui.Spanish':
                        self.gui_manager.set_locale('es')

                # Salir del juego con esc
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui

            self.gui_manager.update(time_delta)
            self.screen.blit(self.background, (0, 0))
            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)
            pygame.display.update()

    def signIn(self):
        with open('config/users.json', 'r') as file:
            data = json.load(file)

        for user in data['users']:
            if user['username'] == self.username_entry.get_text() and user[
                'password'] == self.password_entry.get_text():
                menu_window = Menu_window(1366, 768, self.username_entry.get_text())
                menu_window.begin()
        messagebox.showinfo("Error", "Usuario o contraseña incorrectos")


class SignUp_Window:
    def __init__(self, ancho, alto):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("SignUp")
        self.background = pygame.image.load("assets/signup_bg.png")

        # Inicializar el administrador de interfaz de usuario de pygame_gui
        self.gui_manager = pygame_gui.UIManager((ancho, alto), starting_language='es',
                                                translation_directory_paths=['config/translation'])

        # Crear un ComboBox
        languages_list = ['pygame-gui.English',
                          'pygame-gui.Spanish']
        self.combo_box = pygame_gui.elements.UIDropDownMenu(languages_list, 'pygame-gui.Spanish',
                                                            relative_rect=pygame.Rect(25, 30, 150, 50),
                                                            manager=self.gui_manager)

        # Cuadros de texto del Login
        self.username_rect = pygame.Rect(540, 160, 350, 45)
        self.name_rect = pygame.Rect(540, 220, 350, 45)
        self.age_rect = pygame.Rect(540, 280, 350, 45)
        self.email_rect = pygame.Rect(540, 350, 350, 45)
        self.password_rect = pygame.Rect(540, 420, 350, 45)
        self.password_confirm_rect = pygame.Rect(540, 490, 350, 45)

        # Botones
        self.button_signin = pygame.Rect(455, 540, 150, 70)
        self.button_createaccount = pygame.Rect(750, 540, 150, 70)
        self.button_picture = pygame.Rect(1085, 360, 150, 40)

        # Crear un cuadro de entrada
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.username_rect,
                                                                  manager=self.gui_manager)
        self.name_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.name_rect,
                                                                  manager=self.gui_manager)
        self.age_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.age_rect,
                                                              manager=self.gui_manager)
        self.email_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.email_rect,
                                                                  manager=self.gui_manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_rect,
                                                                  manager=self.gui_manager)
        self.password_entry.set_text_hidden(True)
        self.password_confirm_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_confirm_rect,
                                                                          manager=self.gui_manager)
        self.password_confirm_entry.set_text_hidden(True)

        self.button_signin_label = pygame_gui.elements.UIButton(relative_rect=self.button_signin,
                                                                text="language.sign_in", manager=self.gui_manager)
        self.button_signup_label = pygame_gui.elements.UIButton(relative_rect=self.button_createaccount,
                                                                text="language.create_account",
                                                                manager=self.gui_manager)
        self.button_picture_label = pygame_gui.elements.UIButton(relative_rect=self.button_picture,
                                                                 text="language.upload_picture",
                                                                 manager=self.gui_manager)

        self.file_dialog = None

        # scale images, if necessary so that their largest dimension does not exceed these values
        self.max_image_display_dimensions = (150, 150)
        self.display_loaded_image = None

        # guardar ruta de foto de perfil
        self.pic_path = "assets/no_pic.png"

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_signin:
                        login_window = Login_window(1366, 768)
                        login_window.begin()

                    elif event.ui_element == self.button_createaccount:
                        self.createAccount()

                    elif event.ui_element == self.button_picture:
                        self.upload_picture()

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.text == 'pygame-gui.English':
                        self.gui_manager.set_locale('en')
                    elif event.text == 'pygame-gui.Spanish':
                        self.gui_manager.set_locale('es')

                # Salir del juego con esc
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    if self.display_loaded_image is not None:
                        self.display_loaded_image.kill()

                    try:
                        image_path = create_resource_path(event.text)
                        loaded_image = pygame.image.load(image_path).convert_alpha()
                        image_rect = loaded_image.get_rect()
                        aspect_ratio = image_rect.width / image_rect.height
                        need_to_scale = False
                        if image_rect.width > self.max_image_display_dimensions[0]:
                            image_rect.width = self.max_image_display_dimensions[0]
                            image_rect.height = int(image_rect.width / aspect_ratio)
                            need_to_scale = True

                        if image_rect.height > self.max_image_display_dimensions[1]:
                            image_rect.height = self.max_image_display_dimensions[1]
                            image_rect.width = int(image_rect.height * aspect_ratio)
                            need_to_scale = True

                        if need_to_scale:
                            loaded_image = pygame.transform.smoothscale(loaded_image,
                                                                        image_rect.size)

                        image_rect.center = (1160, 490)
                        self.pic_path = image_path
                        self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=loaded_image,
                                                            manager=self.gui_manager)

                    except pygame.error:
                        messagebox.showinfo("Error", "Selecciona un archivo de formato .jpg o .png")
                        pass

                if (event.type == pygame_gui.UI_WINDOW_CLOSE
                        and event.ui_element == self.file_dialog):
                    self.button_picture_label.enable()
                    self.file_dialog = None

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(event)

            self.gui_manager.update(time_delta)
            self.screen.blit(self.background, (0, 0))

            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()

    def createAccount(self):
        self.username_entry.get_text()
        self.name_entry.get_text()
        self.age_entry.get_text()
        self.email_entry.get_text()
        self.password_entry.get_text()
        self.password_entry.get_text()
        if not self.username_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa un nombre de Usuario")
        elif not self.name_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa un nombre")
        elif not self.age_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa tu edad")
        elif not self.email_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa un correo")
        elif not self.password_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa una contraseÃ±a")
        elif self.password_entry.get_text() != self.password_confirm_entry.get_text():
            messagebox.showinfo("Error", "Las contraseÃ±as no son iguales")
        else:
            with open('config/users.json', 'r') as archivo:
                data = json.load(archivo)
            new_user = {
                "username": self.username_entry.get_text(),
                "name": self.name_entry.get_text(),
                "age": self.age_entry.get_text(),
                "email": self.email_entry.get_text(),
                "password": self.password_entry.get_text(),
                "language": self.gui_manager.get_locale(),
                "profile_pic": self.pic_path,
                "songs": []
            }
            users = data["users"]
            user_exist = next((user for user in users if user["username"] == new_user["username"]), None)
            email_exist = next((user for user in users if user["email"] == new_user["email"]), None)
            if user_exist:
                messagebox.showinfo("Error", "Ya existe un usuario con ese nombre")
            elif email_exist:
                messagebox.showinfo("Error", "Ya existe un usuario con ese correo")
            else:
                data["users"].append(new_user)
                with open('config/users.json', 'w') as archivo:
                    json.dump(data, archivo, indent=4)
                messagebox.showinfo("Exito", "Su cuenta se creo exitosamente")
                login_window = Login_window(1366, 768)
                login_window.begin()

    def upload_picture(self):
        self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                        self.gui_manager,
                                        window_title='Load Image...',
                                        initial_file_path='data/images/',
                                        allow_picking_directories=True,
                                        allow_existing_files_only=True,
                                        allowed_suffixes={""})
        self.button_picture_label.disable()


class Menu_window:
    def __init__(self, ancho, alto, user):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Menu")
        self.background = pygame.image.load("assets/mainmenu_bg.png")
        self.gui_manager = pygame_gui.UIManager((ancho, alto), 'config/theme_menu.json')

        self.user = user

        pygame.mixer.music.load("Efectos/The Army Song 8 Bi.mp3")
        pygame.mixer.music.play(-1)

        # Buttons
        self.button_play = pygame.Rect(395, 180, 160, 90)
        self.button_help = pygame.Rect(395, 300, 160, 90)
        self.button_leaderboard = pygame.Rect(395, 420, 160, 90)
        self.button_load = pygame.Rect(395, 540, 160, 90)



        self.button_logout = pygame.Rect(50, 700, 140, 50)

        self.button_play_label = pygame_gui.elements.UIButton(relative_rect=self.button_play, text="Jugar",
                                                              manager=self.gui_manager)
        self.button_logout_label = pygame_gui.elements.UIButton(relative_rect=self.button_logout, text="Cerrar Sesion",
                                                                manager=self.gui_manager)
        self.button_help_label = pygame_gui.elements.UIButton(relative_rect=self.button_help, text="Ayuda",
                                                              manager=self.gui_manager)
        self.button_leaderboard_label = pygame_gui.elements.UIButton(relative_rect=self.button_leaderboard,
                                                                     text="Salon de la fama", manager=self.gui_manager)
        self.button_load_label = pygame_gui.elements.UIButton(relative_rect=self.button_load,
                                                                     text="Cargar", manager=self.gui_manager)


        # Nombre de usuario
        self.username = pygame.Rect(15, 150, 140, 50)
        self.username_label = pygame_gui.elements.UILabel(relative_rect=self.username, text=self.user,
                                                          manager=self.gui_manager)

        self.max_image_display_dimensions = (120, 120)

        self.playlist = pygame_gui.elements.UISelectionList(pygame.Rect(810, 170, 310, 400),
                                                            item_list=[],
                                                            manager=self.gui_manager,
                                                            allow_multi_select=False)

        self.button_addSong = pygame.Rect(810, 600, 130, 40)
        self.button_addSong_label = pygame_gui.elements.UIButton(relative_rect=self.button_addSong, text="Añadir",
                                                                 manager=self.gui_manager)

        self.button_remove = pygame.Rect(990, 600, 130, 40)
        self.button_remove_label = pygame_gui.elements.UIButton(relative_rect=self.button_remove, text="Quitar",
                                                                manager=self.gui_manager)

        self.tituloplaylist = pygame.Rect(870, 130, 200, 40)
        self.playlist_label = pygame_gui.elements.UILabel(relative_rect=self.tituloplaylist, text=" My Playlist",
                                                                manager=self.gui_manager)

        self.song_window = None
        self.button_song = None
        self.song_selection = None

        self.namesongs = os.listdir("Musica")
        self.songs = [archivo for archivo in self.namesongs if archivo.endswith(".mp3")]

    def open_song_list(self):
        self.song_window = UIWindow(pygame.Rect((500, 150), (380, 360)), resizable=False,
                                    window_display_title="Select Song", manager=self.gui_manager,
                                    draggable=False)

        self.button_song = UIButton(pygame.Rect(80, 20, 174, 30), 'Aceptar',
                                    manager=self.gui_manager,
                                    container=self.song_window)

        self.song_selection = UISelectionList(pygame.Rect(20, 70, 300, 200),
                                              item_list=self.songs,
                                              manager=self.gui_manager,
                                              container=self.song_window,
                                              allow_multi_select=False)

        self.button_addSong_label.disable()
        self.button_logout_label.disable()
        self.button_help_label.disable()
        self.button_play_label.disable()
        self.button_remove_label.disable()
        self.button_leaderboard_label.disable()
        self.button_load_label.disable()
        # self.playlist.disable()

    def addSong(self):
        with open('config/users.json', 'r') as file:
            data = json.load(file)
            users = data['users']
            for user in users:
                if user['username'] == self.user:
                    if self.selected_addsong in user['songs']:
                        messagebox.showinfo("Error", "Ya tienes esta canción en tu playlist")
                    else:
                        self.playlist.add_items([self.selected_addsong])
                        user['songs'].append(self.selected_addsong)
                        with open('config/users.json', 'w') as archivo:
                            json.dump(data, archivo, indent=4)

    def removeSong(self):
        # Cargar el archivo JSON
        with open('config/users.json', 'r') as file:
            data = json.load(file)

        for user in data['users']:
            if user['username'] == self.user:
                songs = user['songs']
                if self.selected_removesong in songs:
                    self.playlist.remove_items([self.selected_removesong])
                    songs.remove(self.selected_removesong)  # Eliminar la canción de la lista
                break

        # Guardar los cambios en el archivo JSON
        with open('config/users.json', 'w') as file:
            json.dump(data, file, indent=4)

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas
        with open('config/users.json', 'r') as file:
            data = json.load(file)
            users = data['users']
            for user in users:
                if user['username'] == self.user:
                    user_songs = user['songs']
                    self.playlist.add_items(user_songs)
                    image_path = user['profile_pic']
                    try:
                        loaded_image = pygame.image.load(image_path).convert_alpha()
                        image_rect = loaded_image.get_rect()
                        aspect_ratio = image_rect.width / image_rect.height
                        need_to_scale = False
                        if image_rect.width > self.max_image_display_dimensions[0]:
                            image_rect.width = self.max_image_display_dimensions[0]
                            image_rect.height = int(image_rect.width / aspect_ratio)
                            need_to_scale = True

                        if image_rect.height > self.max_image_display_dimensions[1]:
                            image_rect.height = self.max_image_display_dimensions[1]
                            image_rect.width = int(image_rect.height * aspect_ratio)
                            need_to_scale = True

                        if need_to_scale:
                            loaded_image = pygame.transform.smoothscale(loaded_image,
                                                                        image_rect.size)

                        image_rect.center = (90, 90)
                        self.pic_path = image_path
                        self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=loaded_image,
                                                            manager=self.gui_manager)

                    except pygame.error:
                        pass

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Salir del juego con esc
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if (event.type == pygame_gui.UI_WINDOW_CLOSE
                        and event.ui_element == self.song_window):
                    self.button_addSong_label.enable()
                    self.button_logout_label.enable()
                    self.button_help_label.enable()
                    self.button_play_label.enable()
                    self.button_remove_label.enable()
                    self.button_leaderboard_label.enable()
                    self.playlist.enable()
                    self.button_load_label.disable()

                    self.song_window = None
                    self.button_song = None
                    self.song_selection = None

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_play:
                        if self.playlist.item_list.__len__() == 0:
                            messagebox.showinfo("Error", "Debes tener al menos 1 cancion en tu playlist")

                        else:
                            pygame.mixer.music.stop()
                            login2 = Login_player2_window(1366, 768, self.user)
                            login2.begin()

                    if event.ui_element == self.button_logout:
                        pygame.mixer.music.stop()
                        login_window = Login_window(1366, 768)
                        login_window.begin()

                    if event.ui_element == self.button_help:
                        pygame.mixer.music.stop()
                        help = help_window(1366, 768, self.user)
                        help.begin()

                    if event.ui_element == self.button_leaderboard:
                        pygame.mixer.music.stop()
                        leaderboard = Leaderboard_window(1366, 768, self.user)
                        leaderboard.begin()

                    if event.ui_element == self.button_addSong_label:
                        self.open_song_list()

                    if event.ui_element == self.button_song:
                        self.selected_addsong = self.song_selection.get_single_selection()

                        if self.selected_addsong != None:
                            self.addSong()

                    if event.ui_element == self.button_remove_label:
                        self.selected_removesong = self.playlist.get_single_selection()

                        if self.selected_removesong != None:
                            self.removeSong()

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui
            self.gui_manager.update(time_delta)

            self.screen.blit(self.background, (0, 0))

            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()


class Login_player2_window:
    def __init__(self, ancho, alto, user1):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Login2")
        self.background = pygame.image.load("assets/login2_bg.png")
        self.user1 = user1

        # Inicializar el administrador de interfaz de usuario de pygame_gui
        self.gui_manager = pygame_gui.UIManager((ancho, alto), 'config/theme_signin2.json', starting_language='es',
                                                translation_directory_paths=['config/translation'])

        # Cuadros de texto del Login
        self.username_rect = pygame.Rect(490, 250, 350, 45)
        self.password_rect = pygame.Rect(490, 350, 350, 45)

        # Botones
        self.button_signin = pygame.Rect(660, 520, 150, 70)
        self.button_return = pygame.Rect(450, 520, 150, 70)

        # Crear un cuadro de entrada
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.username_rect,
                                                                  manager=self.gui_manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_rect,
                                                                  manager=self.gui_manager)
        self.password_entry.set_text_hidden(True)

        self.button_signin_label = pygame_gui.elements.UIButton(relative_rect=self.button_signin,
                                                                text="language.sign_in", manager=self.gui_manager)
        self.button_return_label = pygame_gui.elements.UIButton(relative_rect=self.button_return, text="Regresar",
                                                                manager=self.gui_manager)

        self.instruction = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (1210, 300)),
                                                       text="Inicia sesion para el segundo jugador",
                                                       manager=self.gui_manager)

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_signin:
                        self.signIn()
                    elif event.ui_element == self.button_return:
                        menu = Menu_window(1366, 768, self.user1)
                        menu.begin()

                # Salir del juego con esc
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui

            self.gui_manager.update(time_delta)
            self.screen.blit(self.background, (0, 0))
            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)
            pygame.display.update()

    def signIn(self):
        with open('config/users.json', 'r') as file:
            data = json.load(file)
        user_found = False
        for user in data['users']:
            if self.user1 == self.username_entry.get_text():
                messagebox.showinfo("Error", "Este usuario ya es el jugador 1")
                user_found = True
                break

            if user['username'] == self.username_entry.get_text() and user[
                'password'] == self.password_entry.get_text() and ['username'] != self.user1:
                user_found = True
                role_window = Role_window(1366, 768, self.user1, self.username_entry.get_text())
                role_window.begin()
        if not user_found:
            messagebox.showinfo("Error", "Usuario o contraseña incorrectos")


class Role_window:
    def __init__(self, ancho, alto, user1, user2):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Role")
        self.background = pygame.image.load("assets/rol_bg.png")
        self.gui_manager = pygame_gui.UIManager((ancho, alto), 'config/theme_role.json')

        self.user1 = user1
        self.user2 = user2

        # Buttons
        self.button_attacker = pygame.Rect(385, 400, 160, 90)
        self.button_defender = pygame.Rect(910, 400, 160, 90)
        self.button_return = pygame.Rect(35, 695, 140, 50)

        self.button_attacker_label = pygame_gui.elements.UIButton(relative_rect=self.button_attacker, text="Atacante",
                                                                  manager=self.gui_manager)
        self.button_defender_label = pygame_gui.elements.UIButton(relative_rect=self.button_defender, text="Defensor",
                                                                  manager=self.gui_manager)
        self.button_return_label = pygame_gui.elements.UIButton(relative_rect=self.button_return, text="Regresar",
                                                                manager=self.gui_manager)

        # Nombre de usuario
        self.username = pygame.Rect(15, 150, 140, 50)
        self.username_label = pygame_gui.elements.UILabel(relative_rect=self.username, text=self.user1,
                                                          manager=self.gui_manager, object_id='names')

        # Nombre de usuario
        self.username2 = pygame.Rect(1200, 150, 140, 50)
        self.username2_label = pygame_gui.elements.UILabel(relative_rect=self.username2, text=self.user2,
                                                           manager=self.gui_manager, object_id='names')

        self.max_image_display_dimensions = (120, 120)

        self.instruction = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (1340, 420)),
                                                       text="Seleccione el rol para " + self.user1,
                                                       manager=self.gui_manager, object_id='instruction')

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas
        with open('config/users.json', 'r') as file:
            data = json.load(file)
            users = data['users']
            for user in users:
                if user['username'] == self.user1:
                    if user['language'] == 'es':
                        self.gui_manager.set_locale('es')
                    if user['language'] == 'en':
                        self.gui_manager.set_locale('en')
                    image_path = user['profile_pic']
                    try:
                        loaded_image = pygame.image.load(image_path).convert_alpha()
                        image_rect = loaded_image.get_rect()
                        aspect_ratio = image_rect.width / image_rect.height
                        need_to_scale = False
                        if image_rect.width > self.max_image_display_dimensions[0]:
                            image_rect.width = self.max_image_display_dimensions[0]
                            image_rect.height = int(image_rect.width / aspect_ratio)
                            need_to_scale = True

                        if image_rect.height > self.max_image_display_dimensions[1]:
                            image_rect.height = self.max_image_display_dimensions[1]
                            image_rect.width = int(image_rect.height * aspect_ratio)
                            need_to_scale = True

                        if need_to_scale:
                            loaded_image = pygame.transform.smoothscale(loaded_image,
                                                                        image_rect.size)

                        image_rect.center = (90, 90)
                        self.pic_path = image_path
                        self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=loaded_image,
                                                            manager=self.gui_manager)

                    except pygame.error:
                        pass

                elif user['username'] == self.user2:
                    image_path = user['profile_pic']
                    try:
                        loaded_image = pygame.image.load(image_path).convert_alpha()
                        image_rect = loaded_image.get_rect()
                        aspect_ratio = image_rect.width / image_rect.height
                        need_to_scale = False
                        if image_rect.width > self.max_image_display_dimensions[0]:
                            image_rect.width = self.max_image_display_dimensions[0]
                            image_rect.height = int(image_rect.width / aspect_ratio)
                            need_to_scale = True

                        if image_rect.height > self.max_image_display_dimensions[1]:
                            image_rect.height = self.max_image_display_dimensions[1]
                            image_rect.width = int(image_rect.height * aspect_ratio)
                            need_to_scale = True

                        if need_to_scale:
                            loaded_image = pygame.transform.smoothscale(loaded_image,
                                                                        image_rect.size)

                        image_rect.center = (1275, 90)
                        self.pic_path = image_path
                        self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=loaded_image,
                                                            manager=self.gui_manager)

                    except pygame.error:
                        pass

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Salir del juego con esc
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_attacker:
                        pygame.mixer.music.stop()
                        game = InGame(1366, 768, "attacker", self.user1, self.user2)
                        game.begin()

                    if event.ui_element == self.button_defender:
                        pygame.mixer.music.stop()
                        game = InGame(1366, 768, "defender", self.user1, self.user2)
                        game.begin()

                    if event.ui_element == self.button_return:
                        pygame.mixer.music.stop()
                        menu = Menu_window(1366, 768, self.user1)
                        menu.begin()

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui
            self.gui_manager.update(time_delta)

            self.screen.blit(self.background, (0, 0))

            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()


class help_window:

    def __init__(self, ancho, alto, user):
        pygame.init()
        mixer.init()
        self.user = user

        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Help")
        self.background = pygame.image.load("assets/help_bg.png")
        self.gui_manager = pygame_gui.UIManager((ancho, alto))

        self.button_return = pygame.Rect(1200, 610, 140, 60)

        self.button_return_label = pygame_gui.elements.UIButton(relative_rect=self.button_return, text="Regresar",
                                                                manager=self.gui_manager)

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_return_label:
                        pygame.mixer.music.stop()
                        menu = Menu_window(1366, 768, self.user)
                        menu.begin()

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui
            self.gui_manager.update(time_delta)

            self.screen.blit(self.background, (0, 0))

            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()


class Leaderboard_window:

    def __init__(self, ancho, alto, user):
        pygame.init()
        mixer.init()
        self.user = user

        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Leaderboard")
        self.background = pygame.image.load("assets/leaderboard_bg.png")
        self.gui_manager = pygame_gui.UIManager((ancho, alto))

        self.button_return = pygame.Rect(35, 695, 140, 50)

        self.button_return_label = pygame_gui.elements.UIButton(relative_rect=self.button_return, text="Regresar",
                                                                manager=self.gui_manager)

        self.fuente = pygame.font.Font(None, 40)

        self.datos = self.cargar_datos()

        self.max_image_display_dimensions = (80, 80)

    # Función para cargar datos desde el archivo CSV
    def cargar_datos(self):
        with open('config/leaderboard.csv', 'r') as file:
            reader = csv.reader(file)
            datos = [row for row in reader][1:6]  # Obtener las primeras 5 filas
        return datos

    # Función para mostrar etiquetas en la pantalla
    def mostrar_etiquetas(self, datos):
        font = pygame.font.Font(None, 36)
        y_pos = 200

        for nombre, tiempo, imagen in datos:
            label_name = font.render(nombre, True, (255, 194, 72))
            label_time = font.render(tiempo, True, (255, 194, 72))
            try:
                loaded_image = pygame.image.load(imagen).convert_alpha()
                image_rect = loaded_image.get_rect()
                aspect_ratio = image_rect.width / image_rect.height
                need_to_scale = False
                if image_rect.width > self.max_image_display_dimensions[0]:
                    image_rect.width = self.max_image_display_dimensions[0]
                    image_rect.height = int(image_rect.width / aspect_ratio)
                    need_to_scale = True

                if image_rect.height > self.max_image_display_dimensions[1]:
                    image_rect.height = self.max_image_display_dimensions[1]
                    image_rect.width = int(image_rect.height * aspect_ratio)
                    need_to_scale = True

                if need_to_scale:
                    loaded_image = pygame.transform.smoothscale(loaded_image,
                                                                image_rect.size)

                image_rect.center = (1075, y_pos)
                self.pic_path = imagen
                self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                    image_surface=loaded_image,
                                                    manager=self.gui_manager)

            except pygame.error:
                pass

            self.screen.blit(label_name, (420, y_pos))
            self.screen.blit(label_time, (760, y_pos))
            y_pos += 100

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            # salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_return_label:
                        pygame.mixer.music.stop()
                        menu = Menu_window(1366, 768, self.user)
                        menu.begin()

                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(
                    event)  # Actualiza el administrador de interfaz de usuario de pygame_gui
            self.gui_manager.update(time_delta)

            self.screen.blit(self.background, (0, 0))

            self.mostrar_etiquetas(self.datos)

            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()
