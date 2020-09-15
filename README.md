# Mastermind_AiR_4b Dokumentacja

## Spis treści
* [Funkcjonalości](#funkcjonalnoci)
* [Wybór platformy](#wybr-platformy)
* [Na czym polega Mastermind?](#na-czym-polega-mastermind)
* [Technologia](#technologia)
* [Przykład działania](#przykad-dziaania)
* [Uruchamianie](#uruchamianie)
* [Historia zmian](#historia-zmian)

## Funkcjonalności
- Implementacja zasad gry.
- Gra z komputerem.
- Ustawienie poziomu trudności.
- Statystyka wygranych parametrów.
- Zapis/odczyt stanu gry.
- "Słowny" tryb gry

## Wybór platformy
Grupa wybrała do realizacji projektu platformę GitHub,  ponieważ  posiada on  najwięcej przydatnych funkcjonalości. Mimo, że nie jest to tak intuicyjne środowisko, to jest jedynym wspierającym wspólną pracę nad kodem. Rozważaliśmy wybór platformy Trello, jednak w dyskusji zauważyliśmy, że Trello jest oparte na listach, a GitHub również posiada tę funkcjonalność. Postanowiliśmy więc nie rozdzielać projektu na dwie platformy i w całości zrealizować ją w GitHubie. Jest on również najbezpieczniejszym miejscem pracy nad kodem, gdyż można na bieżąco sprawdzać czy nowy fragmant jest kompatybilny z resztą kodu i nie powoduje wystąpienia błędów. Bardzo prosto można też oceniać postęp w pracach nad projektem dzięki wzkaźnikowi procentowego ukńczenia przy milestonach.

## Na czym polega Mastermind?
Mastermind to gra polegająca na odgadnięciu kodu w określonej liczbie rund. W podstawowej wersji wylosowany kod składa się z sekwencji kolorowych kul. W skład kodu mogą wchodzić kule o tej samej barwie. Po sprawdzeniu wprowadzone przez gracza sekwencji, otrzyma on infrormację o poprawności ułożenia kul. W słownej informacji zwrotnej pojawi się liczba bulls (kula o dobrym kolorze w odpowiednim miejscu) i cows (kula o dobrym kolorze w niewłaściwym miejscu). Gra kończy się w momencie podania identycznej sekwencji (zwycięztwo) jak wylosowana lub po przekroczeniu maksymalnej liczby rund (porażka).
Ponadto w tej wersji gry można grać w trybie słownym. Polega on na odgadnięciu słowa (w języku angielskim). Słowa mają 3-6 znaków i nie są zbudowane z losowych liter (normalnie występujące słowa). Dzięki tej wersji oprócz myślenia możesz ćwiczyć angielskie słówka.

## Technologia
Przy tworzeniu projektu korzystano z następujących narzędzi:
 - Python 3.8
 - pygame 1.9.6
 - JSON
 
 ## Przykład działania
<details>
  <summary>Rozwiń</summary>
  
 ![Tak to działa](/gfx/how_it_works.gif)
 
</details>

## Uruchamianie
Aby uruchomić grę należy najpierw upewnić się, czy posiada się wszystkie wymagane pakiety.
W tym celu będąc w katalogu głównym gry wpisujemy w cmd:

    pip install -r requirements.txt

A następnie aby już zagrać:

    python menu.py
    
Bądź też można skorzystać z pliku 'Zagraj.bat', który włączy grę za nas.

## Historia zmian
Historię zmian można sprawdzić [tutaj](https://github.com/JohnnyBeet/Mastermind_AiR_4b/commits/master)
