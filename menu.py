import sys
import pygame
import pygame_gui
from pygame import mixer
from Seleccion import Select
class Menu_window:
    def __init__(self, ancho, alto, user):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Menu")
        self.background = pygame.image.load("Multimedia/Fondo Aguila.jpg")
        #pygame.mixer.music.load("Multimedia/Number One.mp3")
        #pygame.mixer.music.play(-1)
        self.boton = pygame.Rect(920,430, 100, 50)




        self.gui_manager = pygame_gui.UIManager((ancho, alto))

        self.BotonP = pygame_gui.elements.UIButton(relative_rect=self.boton, text="Jugar", manager=self.gui_manager)



    def begin(self):
        clock = pygame.time.Clock()  # Agrega un reloj para limitar la velocidad de fotogramas
        while True:
            time_delta = clock.tick(60) / 1000.0  # Limita la velocidad de fotogramas a 60 FPS




            #salir del juego con la ventana
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
                    if event.ui_element == self.BotonP:
                        pygame.mixer.music.stop()
                        VentanaSelect= Select(1366, 768)
                        VentanaSelect.begin()


                # Pasar eventos de pygame a pygame_gui
                self.gui_manager.process_events(event)            # Actualiza el administrador de interfaz de usuario de pygame_gui
            self.gui_manager.update(time_delta)

            self.screen.blit(self.background, (0, 0))

            # Dibuja los elementos de la interfaz de usuario de pygame_gui
            self.gui_manager.draw_ui(self.screen)

            pygame.display.update()

