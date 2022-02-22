from . import date
import locale
import sys

lastLocale = locale.getlocale()
locale.setlocale(locale.LC_ALL, 'ru_RU')

print(date(*sys.argv[1:]))

locale.setlocale(locale.LC_ALL, lastLocale)
