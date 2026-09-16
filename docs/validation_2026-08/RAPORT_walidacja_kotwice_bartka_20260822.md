# Walidacja na kotwicach Bartka, 9 elektrod, skan 4 (22.08.2026)

Wejście: `07_dane_bartka_20260822/dane iterations do pythona.pptx` (18 slajdów: 9 elektrod x anodowy/katodowy,
tabela E1/I1/E2/I2 trzech linii + punkt zrzutowany + przecięcie z bazową), `SPE iterations.opju` (19 MB, nowa wersja,
md5 0f06c11a; w projekcie leży starsza z 28.06, md5 f7019da3), zdjęcie WhatsApp = slajd 1.
Skrypt: `walidacja_kotwice_bartka_20260822.py` -> `wyniki_analizy/walidacja_kotwice_bartka_20260822.csv`.
Procedura Bartka (WhatsApp 22.08 14:27): linie przez 2 punkty z danych (NIE Linear Fit), Ep = przecięcie stycznych
zrzutowane na krzywą, Ip = I_krzywa(Ep) − I_bazowa(Ep). Potwierdził: skan 4 (ostatni) zawsze.

## Wynik

| porównanie | anod. śr / med / max | katod. śr / med / max |
|---|---|---|
| odtworzenie z kotwic Bartka vs jego liczby | 1,6 / 0,4 / 8,8 % | 3,6 / 1,7 / 13,4 % |
| automat (raportowane) vs Bartek | 2,1 / 0,9 / 8,6 % | 3,7 / 1,1 / 13,9 % |
| automat krzywa@x vs Bartek | 1,8 / 0,5 / 9,0 % | 3,7 / 1,1 / 13,9 % |
| automat styczne vs Bartek | 8,3 / 8,3 / 12,3 % | 11,4 / 10,7 / 19,7 % |

Bez 3 odstających pików: automat vs Bartek **<= 2,4 % na 15 z 18 pików**, większość poniżej 1 %.
Styczne (prąd z przecięcia) konsekwentnie +8 % / −10 % -> tabela Bartka = krzywa, potwierdzone drugi raz.

## 3 piki odstające, wszystkie PO STRONIE BARTKA (sprawdzone na 4 plikach każdej elektrody)

Test: dla Ep_B z pptx odczytałem I z krzywej w każdym z 4 plików i porównałem z jego I1 „punkt zrzutowany".
- **4 mm B anodowy**: Ip_B 9,928 µA, z ba(3) wychodzi 9,051. Jego I pasuje do pliku `ba` (skan 1, różnica 0,07 µA),
  do ba(3) nie (−0,73 µA). **Odczytał skan 1.** Tabela xlsx ma 8,858 (bliżej skanu 4). Automat 9,078.
- **4 mm C katodowy**: Ip_B −10,025, z ba(3) −8,933. Jego I (−8,72 µA) nie pasuje do ŻADNEGO z 4 plików
  (rozjazd 1,07-1,55 µA). Tabela xlsx ma −9,149. Automat −8,935. Prawdopodobnie inny plik/elektroda albo literówka.
- **13,39 A katodowy**: Ip_B −6,107, z ba(3) −5,289. Jego I (−4,79) nie pasuje do żadnego pliku (0,68-0,76 µA).
  Tabela xlsx −5,160. Automat −5,258.

## Rozjazd 13,39 B z 20.08 ROZSTRZYGNIĘTY
Pytaliśmy: slajd −4,73 µA vs tabela xlsx −3,06 µA. Nowa rozpiska daje −4,612, odtworzenie z kotwic −4,551,
automat −4,563. **Tabela xlsx była błędna**, nie slajd. Wniosek: tabela xlsx ma przynajmniej 1 pewny błąd
przepisywania, walidacja 1,1/2,8 % z 20.08 liczona była częściowo do błędnej referencji.

## Co z tego wynika
1. Automat jest zgodny z ręczną procedurą Bartka na poziomie jej własnej powtarzalności (ok. 1-2 %).
2. Referencja „ręczna tabela" ma błędy rzędu 10-50 % w pojedynczych komórkach (skan 1 zamiast 4, przepisywanie).
   To argument do artykułu: automat eliminuje tę klasę błędów.
3. Do Bartka: 3 piki do ponownego odczytu (4 mm B anod., 4 mm C katod., 13,39 A katod.) + potwierdzenie, że 13,39 B
   katod. −4,6 µA jest dobre, a xlsx −3,06 było złe.
4. .opju: nie czytamy go bez Origina (format binarny, brak otwartego parsera dla .opju; liborigin czyta tylko stare .opj).
   Niepotrzebny, dopóki Bartek wkleja liczby do pptx.
