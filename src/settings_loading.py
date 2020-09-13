import json
""" Wczytywanie danych z pliku CONFIG.txt do odpowiednich miejsc w plikach src """

with open("src/CONFIG.txt") as f:
    data = json.load(f)

""" Słownik nazwa koloru -> wartość RGB koloru """
colors = data["colors"]

""" Konieczne dane konfiguracyjne do każdego obiektu w grze """
game_configs = data["gamesettings"]
menu_configs = data["menu"]
board_configs = data["board"]
logbox_configs = data["logbox"]
menu_button_configs = data["GameSettingMenuButton"]
checkbutton_configs = data["checkbutton"]
