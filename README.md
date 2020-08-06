# Mastermind_AiR_4b Dokumentacja

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
Mastermind to gra polegająca na odgadnięciu kodu w określonej liczbie rund. W podstawowej wersji wylosowany kod składa się z sekwencji kolorowych kul. W skład kodu mogą wchodzić kule o tej samej barwie. Po sprawdzeniu wprowadzone przez gracza sekwencji, otrzyma on infrormację o poprawności ułożenia kul. Jeżeli kula znajduje się we właściwym miejscu obok sekwencji pojawi się czerwona "kulka". Natomiast jeśli kula ma dobry kolor, ale znajduje się na niewłaściwym miejscu to obok pojawi się biała "kulka". W przypadku kul, które nie występują w sekwencji miejsce pozostanie puste. Gra kończy się w momencie podania identycznej sekwencji ( zwycięztwo) jak wylosowana lub po przekroczeniu maksymalnej liczby rund (porażka). 
