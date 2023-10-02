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
        self.background = pygame.image.load("assets/fondo_espanol.png")

        # Inicializar el administrador de interfaz de usuario de pygame_gui
        self.gui_manager = pygame_gui.UIManager((ancho, alto))

        # Crear un ComboBox
        self.combo_box = pygame_gui.elements.UIDropDownMenu(options_list=["Español", "Ingles"],
                                                            starting_option="Español",
                                                            relative_rect=pygame.Rect(25, 50, 150, 50),
                                                            manager=self.gui_manager)

        #Cuadros de texto del Login
        self.email_rect = pygame.Rect(920, 225, 350, 50)
        self.password_rect = pygame.Rect(920, 320, 350, 50)

        # Crear un cuadro de entrada
        self.email_entry = pygame_gui.elements.UITextEntryLine(relative_rect=self.email_rect,
                                                        manager=self.gui_manager)




       # self.button = Button((300, 200, 200, 50), (0, 0, 0, 0), text = "s")


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


