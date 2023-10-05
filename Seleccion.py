import pygame
import pygame_gui
import button
from pygame import mixer
import sys
import os

class Select:
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
                self.gui_manager.update(time_delta)

                self.screen.blit(self.background, (0, 0))

                # Dibuja los elementos de la interfaz de usuario de pygame_gui
                self.gui_manager.draw_ui(self.screen)

                pygame.display.update()


