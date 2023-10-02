import json
import sys
import pygame
import pygame_gui
from pygame_button import Button
import pygame_textinput
from pygame.examples.textinput import TextInput


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
        self.username_rect = pygame.Rect(920, 230, 350, 45)
        self.password_rect = pygame.Rect(920, 320, 350, 45)
        self.button_signin = pygame.Rect(920, 430, 150, 70)
        self.button_signup = pygame.Rect(920, 520, 150, 70)


        # Crear un cuadro de entrada
        self.username_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.username_rect, manager=self.gui_manager)
        self.password_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.password_rect, manager=self.gui_manager)
        self.password_entry.set_text_hidden(True)

        self.button_signin_label = pygame_gui.elements.UIButton(relative_rect=self.button_signin, text="language.sign_in", manager=self.gui_manager)
        self.button_signup_label = pygame_gui.elements.UIButton(relative_rect=self.button_signup, text="language.sign_up", manager=self.gui_manager)




    account_string = '''
    {
        "account":
         {
            "username": "",
            "password": "",
        } 
    }
    '''

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
                        print("Hola")
                        self.username_entry.clear()
                        self.password_entry.clear()
                    elif event.ui_element == self.button_signup:
                        self.username_entry.get_text()
                        self.password_entry.get_text()
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
                            print(f"El usuario ya existe")
                        else:
                            data["users"].append(new_user)
                            with open('config/users.json', 'w') as archivo:
                                json.dump(data, archivo, indent=4)
                            print("Usuario agregado")

                if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.text == 'pygame-gui.English':
                        self.gui_manager.set_locale('en')
                    elif event.text == 'pygame-gui.Spanish':
                        self.gui_manager.set_locale('es')

                #  if event.type == pygame.MOUSEBUTTONDOWN:
               #     if self.ca_button.collidepoint(event.pos):
               #        print("Me cago en JSON")

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


