import random


def main():
    def get_code_lenght():
        available_range = [str(x) for x in range(3, 11)]
        code_lenght = input("Podaj dlugosc zgadywanego kodu(z zakresu od 3 do 10 znaków): ")
        while code_lenght not in available_range:
            print("Nieporawna dlugosc kodu!")
            code_lenght = input("Podaj dlugosc zgadywanego kodu(z zakresu od 3 do 10 znaków): ")
        return int(code_lenght)

    def generate_code(code_lenght):
        return [str(random.randint(0, 9)) for x in range(code_lenght)]

    def get_user_code(code_lenght):
        """ TODO: stwórz poprawne wpisywanie wejścia, nie rzutuj chamsko na stringa na listę
            Dominik edit: nie mam pomysłu jak nie rzutować po chamsku stringa na listę, ale dodałem kontrolę poprawności
            wprowadzanych danych przez użytkownika oraz chyba w poprzedniej wersji program podawał niepoprawnie wartości
            cows, więc to zmieniłem
        """
        retry = True
        available_chars = [str(x) for x in range(0, 10)]
        user_input = []
        while retry:
            retry = False
            user_input = list(input("Podaj {}-cyfrowy kod: ".format(code_lenght)))
            if len(user_input) != code_lenght:
                retry = True
            else:
                for i in user_input:
                    if i not in available_chars:
                        retry = True
        return user_input

    def set_difficulty_lvl(code_lenght):
        available_diff_lvls={"easy":4*code_lenght,"medium":3*code_lenght,"hard":2*code_lenght,"impossible":code_lenght}
        print("Wybierz poziom trudnosci gry:")
        for i in available_diff_lvls.keys():
            print("{} - {} prób".format(i,available_diff_lvls[i]))
        diff = input("Wskaż poziom trudności na którym chcesz grać: ")
        while diff not in available_diff_lvls.keys():
            print("Niepoprawny poziom trudności!")
            diff = input("Wskaż poziom trudności na którym chcesz grać: ")
        return available_diff_lvls[diff]

    def gameplay(ran_num, user_num, code_lenght, difficulty):
        main_counter = 1
        while ran_num != user_num:
            main_counter += 1
            bulls = 0
            cows = 0
            # check for cows
            for i, num in enumerate(user_num):
                if num in ran_num:
                    cows += 1
            # check for bulls
            for num_i in range(code_lenght):
                if ran_num[num_i] == user_num[num_i]:
                    bulls += 1
            cows -= bulls
            print(cows, " cows ", bulls, " bulls")
            if(main_counter <= difficulty):
                print("Spróbuj zgadnąć jeszcze raz. Zostało Ci {} prób!".format(1+difficulty-main_counter))
                user_num = get_user_code(code_lenght)
            else:
                print("Niestety przekroczyłeś liczbę możliwych prób :(\nPoprawnym kodem było {}".format(ran_num))
                break
        else:
            print("Gratulacje! Zgadłeś za " + str(main_counter) + " razem!")

    code_lenght = get_code_lenght()
    ran_num = generate_code(code_lenght)
    difficulty = set_difficulty_lvl(code_lenght)
    user_num = get_user_code(code_lenght)
    gameplay(ran_num, user_num, code_lenght, difficulty)


main()
