# PeakWise

<p align="center">
  <a href="README.md">🇬🇧 In English</a> ·
  <a href="#co-to-robi">Co to robi</a> ·
  <a href="#walidacja">Walidacja</a> ·
  <a href="#czego-to-nie-robi">Czego nie robi</a>
</p>

Analiza pików woltamperometrii cyklicznej dla elektrod sitodrukowanych wytwarzanych drukiem 3D
(sonda FeMeOH), napisana jako notatnik Google Colab, żeby działała bez instalowania czegokolwiek.

## Co to robi

Z plików tekstowych wyeksportowanych z NOVA program znajduje pik anodowy i katodowy, prowadzi
linię bazową tak, jak robi to analityk w Origin, czyli prostą najmniejszych kwadratów przez płaski
odcinek pojemnościowy tuż przed narastaniem sygnału faradajowskiego, i podaje prąd piku na trzy sposoby:

- w maksimum,
- na krzywej w punkcie przecięcia stycznych,
- w samym punkcie przecięcia stycznych.

Pliki wielocyklowe są czytane z ostatniego cyklu. Wyniki trafiają do pliku CSV oraz do paczek
`experiment.json`, przeznaczonych do odtworzenia eksperymentu w silniku gry
(schemat w `docs/EXPERIMENT_JSON_SPEC.md`).

## Walidacja

Porównanie z ręczną tabelą z Origin dla **45 elektrod** (trzy serie: średnica elektrody pracującej,
wysokość warstwy, długość kontaktu; czwarty skan każdej elektrody):

| wielkość | błąd średni | mediana |
|---|---|---|
| prąd piku anodowego | 1,1 % | 0,7 % |
| prąd piku katodowego | 2,8 % | 1,1 % |

`validate_against_manual_table.py` odtwarza te liczby, gdy pliki surowe zostaną położone
w katalogu `data/`; **nie są one częścią tego repozytorium**.

To samo porównanie z dwóch innych stron: `walidacja_kotwice_bartka_20260822.py` sprawdza wobec
ręcznie wskazanych punktów kotwiczących zamiast tabeli zbiorczej, a `powtarzalnosc_3_skany_20260822.py`
bada powtarzalność między skanami dla każdej elektrody.

Raporty z walidacji: `docs/validation_2026-08/`.

## Czego to nie robi

- **Nie zawiera danych pomiarowych.** Pliki surowe trzeba dostarczyć samemu.
- Nie decyduje za analityka przy przypadkach granicznych.
- Nie obsługuje innych sond niż FeMeOH bez sprawdzenia, czy założenia o kształcie tła nadal trzymają.

## Licencja

MIT. Copyright 2026 Paweł Kwaczyński.
