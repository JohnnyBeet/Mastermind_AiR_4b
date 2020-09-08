import pygame
import json
import sys
from src.game_classes import Peg, Letter

""" Przykład jak 'skutecznie' zapisywać i ładować obiekty Peg oraz Letter """


screen = pygame.display.set_mode((400, 400))
test_peg = Peg((200, 200), (200, 200, 100), 30, screen)
test_letter = Letter((300, 300), (100, 200, 0), 40, screen, "A", (4, 2, 0), 30)

what_to_load = input("Załadować 'Peg' czy 'Letter'? ")

# TODO: w pliku save_game.py metoda save_game powinna loopować przez rows_of_pegs i po kolei zapisywać pegi/lettery
#  do jsona, może to być w formie zagnieżdżonej listy

# przykład jak załadować pojedyńczy obiekt typu Peg albo Letter
if what_to_load == "Peg":
    json_data = test_peg.to_json()
    with open('test_json', 'w') as f:
        json.dump(json_data, f)  # zapisuje peg do pliku test_json
elif what_to_load == "Letter":
    json_data = test_letter.to_json()
    with open('test_json', 'w') as f:
        json.dump(json_data, f)  # zapisuje letter do pliku test_json
else:
    sys.exit()  # wyjście tylko do testów

# TODO: w pliku save_game.py metoda load_game powinna loopować przez odczytaną zagnieżdzoną listę i po kolei
#  nadpisywać pegi/letttery w rows_of_pegs nowymi obiektami stworzonymi tak jak pokazano poniżej

# tworzenie pojedyńczego obiektu na nowo z json-a
with open('test_json', "r") as f:
    json_data = json.load(f)

if what_to_load == "Peg":
    new_peg = Peg.from_json(json_data, screen)  # tworzy nowego pega z załadowanych danych z jsona
    print(new_peg.__dict__)  # potwierdzenie że obiekt został stworzony
elif what_to_load == "Letter":
    new_letter = Letter.from_json(json_data, screen) # tworzy nowego lettera z załadowanych danych z jsona
    print(new_letter.__dict__)  # potwierdzenie że obiekt został stworzony

