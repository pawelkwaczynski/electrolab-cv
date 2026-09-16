# PeakWise: walidacja po przejściu na ostatni skan + nowa linia bazowa (20.08.2026)

## Co zmieniono w notebooku (`PeakWise_CV_Analyzer.ipynb`, backup `.BACKUP_20260820`)
1. **Cykl:** analiza czyta OSTATNI cykl z pliku (`KTORY_CYKL='ostatni'`). Pliki labu mają po
   JEDNYM cyklu, więc „skan 4" Bartka = plik `ba(3)` (sprawdzone: prądy z jego slajdów
   zgadzają się z plikami `ba(3)` co do 4 cyfr, a slajd 2 „skan 1" = plik `ba`).
2. **Linia bazowa, jedna reguła dla obu gałęzi:** onset sygnału = pierwszy punkt za
   najbardziej płaskim odcinkiem, w którym nachylenie przekracza
   max(0,2 · maks. nachylenie zbocza, 1,5 · 10. percentyl); bazowa = MNK po
   [onset − 0,35 V; onset − 0,05 V]. Odtwarza kotwice Bartka z 11.08 (anodowe −0,24…0,06 V,
   katodowe 0,86…0,63 V przy apeksie 1,10 V). Stara reguła (stopa `E < Epa − 0,35`) wchodziła
   w początek wzrostu i przy 4 mm odejmowała 3,7-4,5 µA zamiast ~0,8 µA (to był cały
   „problem 4 mm").
3. **Ip trzema odczytami** + bramka kształtu (`clear`/`weak`, spadek za maksimum < 5 % wzrostu):
   `maksimum` (klasyczne), `krzywa@x` (krok 4 Bartka: krzywa przy E przecięcia stycznych),
   `styczne` (przecięcie). Raportowane: pik wyraźny → maksimum, pik słaby → krzywa@x.
   Przełączniki: `IP_DEFINICJA`, `SLABY_PIK_STYCZNE`. Wszystkie odczyty są w CSV i w JSON.

## Wynik vs tabela Bartka (`FDM SPE EXPERIMENTS (1).xlsx`, 45 elektrod, 0 crashy)
| skan | Ip_a śr. / mediana | Ip_c śr. / mediana | bias a / c |
|---|---|---|---|
| **ostatni (ba(3))** | **1,1 % / 0,7 %** | **2,8 % / 1,1 %** | −0,1 % / −0,6 % |
| pierwszy (ba) | 16,1 % / 14,6 % | 2,8 % / 2,4 % | +15,0 % / +1,6 % |
| średnia z 4 | 5,5 % / 4,9 % | 2,9 % / 1,6 % | +4,7 % / −0,3 % |
| stary kod (lipiec), pierwszy | 9,9 % / 7,0 % | 9,6 % / 5,4 % | +3,3 % / +9,4 % |

Per seria (ostatni): WE 0,9 % / 1,7 %, LAYER HEIGHT 0,6 % / 1,5 %, CONTACT LENGTH 1,5 % / 4,3 %.
Żadna elektroda nie przekracza 15 % błędu.

Odczyt stycznymi daje systematycznie więcej: Ip_a +8 %, Ip_c +14 % względem tabeli →
**tabela Bartka powstała z odczytu krzywej, nie z przecięcia stycznych** (to samo widać na
jego slajdach: 2 = krzywa, 4 = styczne, różnica 7-19 %).

## 5 przykładów Bartka z liczbami (plik `ba(3)`, S2 = `ba`)
| slajd | wielkość | Bartek | auto | uwaga |
|---|---|---|---|---|
| S2 4mm A anod (skan 1) | E przecięcia | 0,8109 | 0,8091 | |
| | bazowa przy E_x | 1,45e-7 | 2,2e-7 | |
| | Ip krzywa / styczne | 1,156e-5 / 1,235e-5 | 1,137e-5 / 1,224e-5 | −2 % / −1 % |
| S3 4mm B anod | E przecięcia | 0,7383 | 0,7363 | |
| | Ip krzywa / styczne | 9,13e-6 / 9,93e-6 | 9,08e-6 / 9,77e-6 | −0,5 % / −2 % |
| S4 4mm B katod | E przecięcia | −0,0129 | −0,0024 | |
| | Ip krzywa / styczne | −6,46e-6 / −7,20e-6 | −6,25e-6 / −7,01e-6 | −3 % / −3 % |
| S5 13,39 B katod | Ip krzywa / styczne | −4,73e-6 / −5,65e-6 | −3,93e-6 / −5,42e-6 | −17 % / −4 %; ⚠️ tabela ma −3,06e-6 |
| S6 13,39 C katod | Ip krzywa / styczne | −4,08e-6 / −5,00e-6 | −3,80e-6 / −4,82e-6 | −7 % / −4 % |

⚠️ 13,39 B: slajd 5 Bartka (−4,73 µA) i jego tabela (−3,06 µA) to różne liczby dla tej
samej elektrody. Do wyjaśnienia z nim.

## Jak odtworzyć
```
uv run --with matplotlib --with scipy --with pandas --with ipython --with openpyxl \
  python walidacja_vs_tabela_bartka.py --skan ostatni --csv wyniki_analizy/walidacja.csv
```
(bez argumentu SETUP skrypt bierze komórkę SETUP prosto z notebooka).
Wyniki per elektroda: `wyniki_analizy/walidacja_v9_skan_{ostatni,pierwszy,srednia}.csv`.

## Czego NIE zmieniono
- Detekcja potencjałów pików (Ep, ΔEp): bez zmian.
- Progi `find_peaks` dla piku katodowego: bez zmian.
- `experiment.json`: schemat 1.0 → 1.1 (dodane pola, nic nie usunięte).
