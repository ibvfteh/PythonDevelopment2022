from . import bullscows, gameplay
import typing as tp
import sys
import urllib.request

def ask(prompt: str, valid: tp.List[str] = None):
    if valid is None:
        print(prompt)
        return input()
    
    while True:
        print(prompt)
        w = input()
        if w in valid:
            return w

def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))

dictionary_path = sys.argv[1]
try:
    f = open(dictionary, "r", encoding='utf-8')
    words = f.read().split()
except:
    f = urllib.request.urlopen(dictionary_path)
    words = f.read().decode('utf-8').split()

words_len = 5
if len(sys.argv) > 2:
    words_len = sys.argv[2]

words = [w for w in words if len(w) == words_len]

print(gameplay(ask, inform, words))
