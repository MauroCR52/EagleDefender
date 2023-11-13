from interfaz import Login_window
from ingame import InGame
from interfaz import Menu_window


def main():

    #login_window = Login_window(1366, 768)

    login_window = InGame(1366, 768, "attacker","marco", "juan")
    #login_window = Menu_window(1366, 768, "marco")
    login_window.begin()

main()






