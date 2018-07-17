# coding=utf-8
# Turniej wiedzy
# Gra sprawdzająca wiedzę ogólną, odczytująca dane ze zwykłego pliku tekstowego

import pickle
import sys


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
    try:
        f = open("high_scores.dat", "rb")
        high_scores = pickle.load(f)
        f.close()
    except FileNotFoundError:
        high_scores = []
    HIGH_SCORES_SIZE = 3
    is_score_big_enough = False
    if len(high_scores) >= HIGH_SCORES_SIZE:
        if score > high_scores[HIGH_SCORES_SIZE - 1][1]:
            is_score_big_enough = True
    if len(high_scores) < HIGH_SCORES_SIZE or is_score_big_enough:
        player_name = input("Twój wynik jest jednym z najlepszych! Podaj swoje imię, które znajdziesz na liście najlepszych wyników: ")
        high_scores.append((player_name, score))
        high_scores.sort(key=lambda tup: tup[1], reverse=True)
        high_scores = high_scores[:HIGH_SCORES_SIZE]
        f = open("high_scores.dat", "wb")
        pickle.dump(high_scores, f)
        f.close()


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
    add_score_to_best_scores(score)


main()
input("\n\nAby zakończyć program, naciśnij klawisz Enter.")
