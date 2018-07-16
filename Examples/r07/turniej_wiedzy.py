# coding=utf-8
# Turniej wiedzy
# Gra sprawdzająca wiedzę ogólną, odczytująca dane ze zwykłego pliku tekstowego

import sys
import pickle
import shelve

def open_file(file_name, mode):
    """Otwórz plik."""
    try:
        the_file = open(file_name, mode)
    except IOError as e:
        print("Nie można otworzyć pliku", file_name, "Program zostanie zakończony.\n", e)
        input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
        sys.exit()
    else:
        return the_file

def next_line(the_file):
    """Zwróć kolejny wiersz pliku kwiz po sformatowaniu go."""
    line = the_file.readline()
    line = line.replace("/", "\n")
    return line

def next_block(the_file):
    """Zwróć kolejny blok danych z pliku kwiz."""
    category = next_line(the_file)

    points = next_line(the_file)
    
    question = next_line(the_file)
    
    answers = []
    for i in range(4):
        answers.append(next_line(the_file))
        
    correct = next_line(the_file)
    if correct:
        correct = correct[0]
        
    explanation = next_line(the_file) 

    return category, points, question, answers, correct, explanation

def welcome(title):
    """Przywitaj gracza i pobierz jego nazwę."""
    print("\t\t Witaj w turnieju wiedzy!\n")
    print("\t\t", title, "\n")


def add_score_to_best_scores(score):
    s = shelve.open("best_scores.dat")
    best_scores = [s["best_scores"]]
    BEST_SCORES_SIZE = 5
    if best_scores.__len__() < BEST_SCORES_SIZE | score > best_scores[BEST_SCORES_SIZE - 1][1]:
        player_name = input("Twój wynik jest jednym z najlepszych! Podaj imię gracza: ")
        best_scores.append((player_name, score))
        best_scores.sort(key=lambda tup: tup[1], reverse=True)
        if best_scores.__len__() > BEST_SCORES_SIZE:
            del best_scores[BEST_SCORES_SIZE]
            # TODO: Save

 
def main():
    trivia_file = open_file("kwiz.txt", "r")
    title = next_line(trivia_file)
    welcome(title)
    score = 0

    # pobierz pierwszy blok
    category, points, question, answers, correct, explanation = next_block(trivia_file)
    while category:
        # zadaj pytanie
        print(category)
        print("Za poprawną odpowiedź na to pytanie możesz otrzymać następującą ilość punktów:", points)
        print(question)
        for i in range(4):
            print("\t", i + 1, "-", answers[i])

        # uzyskaj odpowiedź
        answer = input("Jaka jest Twoja odpowiedź?: ")

        # sprawdź odpowiedź
        if answer == correct:
            print("\nOdpowiedź prawidłowa!", end=" ")
            score += int(points)
        else:
            print("\nOdpowiedź niepoprawna.", end=" ")
        print(explanation)
        print("Wynik:", score, "\n\n")

        # pobierz kolejny blok
        category, points, question, answers, correct, explanation = next_block(trivia_file)

    trivia_file.close()

    print("To było ostatnie pytanie!")
    print("Twój końcowy wynik wynosi", score)

 
main()  
input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
