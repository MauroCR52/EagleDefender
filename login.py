import json
import sys
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage
from pygame_gui.windows import UIFileDialog
from pygame_gui.core.utility import create_resource_path
from Menu import Menu_window
from tkinter import messagebox


class Initial_window:
    def __init__(self, ancho, alto):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Login")
        self.background = pygame.image.load("assets/login_bg.png")

        # Inicializar el administrador de interfaz de usuario de pygame_gui
        self.gui_manager = pygame_gui.UIManager((ancho, alto), starting_language='es', translation_directory_paths=['config/translation'])

        # Crear un ComboBox
        languages_list = ['pygame-gui.English',
                          'pygame-gui.Spanish']
        self.combo_box = pygame_gui.elements.UIDropDownMenu(languages_list, 'pygame-gui.Spanish', relative_rect=pygame.Rect(25, 30, 150, 50), manager=self.gui_manager)

        #Cuadros de texto del Login
        self.username_rect = pygame.Rect(850, 220, 350, 45)
        self.password_rect = pygame.Rect(850, 330, 350, 45)

        #Botones
        self.button_signin = pygame.Rect(920, 430, 150, 70)
        self.button_signup = pygame.Rect(920, 520, 150, 70)


        # Crear un cuadro de entrada
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.username_rect, manager=self.gui_manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_rect, manager=self.gui_manager)
        self.password_entry.set_text_hidden(True)

        self.button_signin_label = pygame_gui.elements.UIButton(relative_rect=self.button_signin, text="language.sign_in", manager=self.gui_manager)
        self.button_signup_label = pygame_gui.elements.UIButton(relative_rect=self.button_signup, text="language.sign_up", manager=self.gui_manager)

    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            #salir del juego con la ventana
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
                self.gui_manager.process_events(event)            # Actualiza el administrador de interfaz de usuario de pygame_gui

            self.gui_manager.update(time_delta)
            self.screen.blit(self.background, (0, 0))
            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)
            pygame.display.update()

    def signIn(self):
        with open('config/users.json', 'r') as file:
            data = json.load(file)

        for user in data['users']:
            if user['username'] == self.username_entry.get_text() and user['password'] == self.password_entry.get_text():
                menu_window = Menu_window(1366, 768, self.username_entry.get_text())
                menu_window.begin()
        messagebox.showinfo("Error","Usuario o contraseña incorrectos")


class SignUp_Window:
    def __init__(self, ancho, alto):
        pygame.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("SignUp")
        self.background = pygame.image.load("assets/signup_bg.png")

        # Inicializar el administrador de interfaz de usuario de pygame_gui
        self.gui_manager = pygame_gui.UIManager((ancho, alto), starting_language='es', translation_directory_paths=['config/translation'])

        # Crear un ComboBox
        languages_list = ['pygame-gui.English',
                          'pygame-gui.Spanish']
        self.combo_box = pygame_gui.elements.UIDropDownMenu(languages_list, 'pygame-gui.Spanish', relative_rect=pygame.Rect(25, 30, 150, 50), manager=self.gui_manager)

        #Cuadros de texto del Login
        self.username_rect = pygame.Rect(540, 260, 350, 45)
        self.password_rect = pygame.Rect(540, 380, 350, 45)
        self.password_confirm_rect = pygame.Rect(540, 450, 350, 45)

        #Botones
        self.button_signin = pygame.Rect(455, 540, 150, 70)
        self.button_createaccount = pygame.Rect(750, 540, 150, 70)
        self.button_picture = pygame.Rect(1085, 360, 150, 40)

        # Crear un cuadro de entrada
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.username_rect, manager=self.gui_manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_rect, manager=self.gui_manager)
        self.password_entry.set_text_hidden(True)
        self.password_confirm_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_confirm_rect,
                                                                  manager=self.gui_manager)
        self.password_confirm_entry.set_text_hidden(True)

        self.button_signin_label = pygame_gui.elements.UIButton(relative_rect=self.button_signin, text="language.sign_in", manager=self.gui_manager)
        self.button_signup_label = pygame_gui.elements.UIButton(relative_rect=self.button_createaccount, text="language.create_account", manager=self.gui_manager)
        self.button_picture_label = pygame_gui.elements.UIButton(relative_rect=self.button_picture, text="language.upload_picture", manager=self.gui_manager)

        self.file_dialog = None

        # scale images, if necessary so that their largest dimension does not exceed these values
        self.max_image_display_dimensions = (150, 150)
        self.display_loaded_image = None


    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas

        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS

            #salir del juego con la ventana
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.button_signin:
                        login_window = Initial_window(1366, 768)
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

                        self.display_loaded_image = UIImage(relative_rect=image_rect,
                                                            image_surface=loaded_image,
                                                            manager=self.gui_manager)

                    except pygame.error:
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
        self.password_entry.get_text()
        self.password_entry.get_text()
        if not self.username_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa un nombre de Usuario")
        elif not self.password_entry.get_text().strip():
            messagebox.showinfo("Error", "Ingresa una contraseña")
        elif self.password_entry.get_text() != self.password_confirm_entry.get_text():
            messagebox.showinfo("Error", "Las contraseñas no son iguales")
        else:
            with open('config/users.json', 'r') as archivo:
                data = json.load(archivo)
            new_user = {
                "username": self.username_entry.get_text(),
                "password": self.password_entry.get_text(),
                "language": self.gui_manager.get_locale()
            }
            users = data["users"]
            user_exist = next((user for user in users if user["username"] == new_user["username"]), None)
            if user_exist:
                messagebox.showinfo("Error", "Ya existe un usuario con ese nombre")
            else:
                data["users"].append(new_user)
                with open('config/users.json', 'w') as archivo:
                    json.dump(data, archivo, indent=4)
                messagebox.showinfo("Exito", "Su cuenta se creó exitosamente")
                login_window = Initial_window(1366, 768)
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




