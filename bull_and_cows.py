import random

# TODO: dodaj opcję wyboru długości odgadywanego kodu
ran_num=[]
for x in range(4):
    ran_num.append(str(random.randint(0,9)))
# TODO: stwórz poprawne wpisywanie wejścia, nie rzutuj chamsko na stringa na listę
user_num=list((input("Podaj 4 cyfrową liczbę: ")))
main_counter=1


while ran_num != user_num :
    main_counter+=1
    bulls=0
    cows=0
    #check for cows
    for i,num in enumerate(user_num):
        if num in ran_num and (i-1)!=ran_num.index(num):
            cows+=1
            print("gotten cow!")
    #check for bulls
    for num_i in  range(4):
        if ran_num[num_i] == user_num[num_i]:
            bulls+=1

    print(cows," cows ", bulls, " bulls")
    user_num=list((input("Spróbuj zgadnąć jeszcze raz: ")))

print("Gratulacje! Zgadłeś za " + str(main_counter) + " razem!")