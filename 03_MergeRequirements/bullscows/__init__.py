import textdistance
import typing as tp
import random 

def bullscows(guess: str, secret: str) -> (int, int):
    ham = textdistance.hamming.similarity(guess, secret)
    bag = textdistance.bag.similarity(guess, secret)
    return (ham, bag - ham)


def gameplay(ask: callable, inform: callable, words: tp.List[str]) -> int:

    secret = random.choice(words)
    count = 0

    while True:
        guess = ask("Введите слово: ", words)
        b, c = bullscows(guess, secret)
        inform("Быки: {}, Коровы: {}", b, c)
        count += 1
        if b == len(secret):
            return count

