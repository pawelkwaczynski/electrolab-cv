# Triage 45 elektrod: automat vs tabela xlsx Bartka (22.08.2026)

Wejście: `dane_wyniki/FDM SPE EXPERIMENTS (1).xlsx` (arkusze Diameter/Height/Lenght, 45 elektrod, IOX i IRED),
pliki `SPE iterations/*` (4 skany na elektrodę: ba, ba(1), ba(2), ba(3) = skan 4).
Automat: komórka SETUP `PeakWise_CV_Analyzer.ipynb` (bez zmian), odczyt raportowany (pik wyraźny = maksimum, słaby = krzywa@x).
Skrypt: `wyniki_analizy/triage_45_elektrod_20260822.py` -> `triage_45_elektrod_20260822.csv` (88 wierszy = piki),
wykresy rozbieżności: `wyniki_analizy/triage_20260822/*.png` (krzywa, bazowa z oknem, onset, E_x stycznych, punkt Ip).
Próg rozbieżności 4 % (automat ba(3) vs xlsx), próg „inny skan" 2 %.

## Liczby zbiorcze

| | |
|---|---|
| pików w tabeli | 88 (45 elektrod; 8,39 B i 8,39 C bez IRED) |
| OK (|d| <= 4 %) | 80 (91 %) |
| klasa a: xlsx = inny skan | 3 |
| klasa b: xlsx nie pasuje do żadnego pliku | 4 (2 graniczne 4,0 i 4,3 %) |
| klasa c: automat do poprawki | 1 (plus 13,39 B skany 1-3, patrz niżej) |
| błąd |d| na 87 pikach z wynikiem | śr. 1,9 %, mediana 1,0 %, 68 pików <= 2 % |

## Tabela rozbieżności

| elektroda | pik | xlsx µA | auto ba(3) µA | d % | skan1 / skan2 / skan3 d % | kształt | klasa | diagnoza |
|---|---|---|---|---|---|---|---|---|
| 1 mm A | anod | 1,247 | 1,185 | -5,0 | +0,4 / -4,7 / -5,6 | weak | a | xlsx = skan 1. Uwaga: Ip_max skanu 4 (1,260) też pasuje na 1,1 % |
| 12,39 C | katod | -5,097 | -5,321 | -4,4 | +1,5 / -3,4 / -4,4 | weak | a | xlsx = skan 1 |
| 12,39 B | katod | -1,338 | -1,418 | -6,0 | +4,0 / -1,8 / -4,3 | weak | a | xlsx = skan 2; Ip_max -1,053 vs krzywa@x -1,418 (35 % różnicy definicji) |
| 1 mm C | katod | -1,039 | -0,995 | +4,3 | +7,3 / +6,8 / +5,9 | weak | b | graniczny; żaden skan < 2 %; wykres poprawny; inna bazowa Bartka |
| 13,39 B | katod | -3,058 | -4,563 | -49,2 | brak / brak / brak | weak | b | błąd przepisywania potwierdzony (nowa rozpiska Bartka -4,612, automat 1,1 % od niej) |
| 8,39 B | anod | 3,377 | 3,150 | -6,7 | +50,3 / +15,1 / +2,6 | weak | b | xlsx między skanem 3 i 4; wykres skanu 4 poprawny; do ponownego odczytu |
| 8,39 C | anod | 4,268 | 4,441 | +4,0 | +18,4 / +16,1 / +9,2 | weak | b | graniczny; ramię bez maksimum, Ip zależy od punktu odczytu; bazowa poprawna |
| 2 mm b | katod | -0,793 | brak | | brak / brak / brak | | c | automat nie widzi piku na żadnym skanie (plateau bez minimum) |

Poza progiem, ale warte wzmianki (3-4 %): 11,39 B katod +3,7 % (wszystkie skany 3,2-3,5 %), 10,39 C anod -3,5 % (skan 2 pasuje na 0,8 %).

## Lista do odesłania Bartkowi (7 pików)

1. 1 mm A anodowy: xlsx 1,247 µA to skan 1; skan 4 daje 1,19-1,26 µA. Prośba o odczyt ze skanu 4.
2. 12,39 C katodowy: xlsx -5,097 to skan 1; skan 4 daje -5,32 µA.
3. 12,39 B katodowy: xlsx -1,338 to skan 2; skan 4 daje -1,42 µA (albo -1,05 przy odczycie w minimum).
4. 13,39 B katodowy: xlsx -3,058 błędne, poprawna wartość ok. -4,6 µA (jego rozpiska z 22.08 -4,612). Poprawić w tabeli.
5. 8,39 B anodowy: xlsx 3,377 nie pasuje do żadnego skanu (skan 4: 3,15, skan 3: 3,47). Prośba o ponowny odczyt.
6. 8,39 C anodowy: xlsx 4,268 vs automat 4,441 (4,0 %), ramię bez maksimum; prośba o kotwice (linie przez 2 punkty) jak w pptx z 22.08.
7. 1 mm C katodowy: xlsx -1,039 vs automat -0,995 (4,3 %), żaden skan bliżej niż 5,9 %; prośba o kotwice.
Do tego pytanie: 2 mm b katodowy, xlsx -0,793 µA. Gałąź katodowa nie ma minimum, prosić o kotwice (gdzie postawił punkt i bazową).

## Automat wymaga poprawki (konkretne diagnozy)

1. **2 mm b katod, klasa c.** Gałąź powrotna to plateau: prąd -0,86..-0,88 µA dla E < 0,15 V, bez lokalnego minimum.
   `find_peaks(-Is, prominence=max(5 % Ip_a, 20 nA))` nie zwraca nic, `pik_c = None` na wszystkich 4 plikach.
   Test fallbacku (minimum gałęzi jako pseudo-pik + bazowa „onset"): Ip_max -0,875, krzywa@x -0,939, styczne -1,056 µA,
   xlsx -0,793 (10-18 % od fallbacku, więc Bartek liczył z innej bazowej, ale pik istnieje). Poprawka: gdy brak minimum,
   brać minimum gałęzi w oknie [Ep_a-0,30; Ep_a-0,01] (lub do końca gałęzi) i oznaczać `ksztalt='plateau'`.
2. **13,39 B katod, skany 1-3, ten sam mechanizm.** Prominencja minimum 280-360 nA vs próg 5 % Ip_a = 347-439 nA.
   Skan 4 przeszedł o 11 nA (358 vs 347), skany 1-3 odpadły. Próg jest kruchy dla słabych pików katodowych
   (zob. `triage_20260822/13,39_B_katod_4skany.png`). Ten sam fallback co w p. 1 rozwiązuje oba przypadki.
3. **Bramka kształtu `weak` przy widocznym maksimum (1 mm A anod, 8,39 B anod).** Maksimum jest wyraźne w skali całego
   piku, ale spadek w oknie 0,08 V za maksimum < 5 % wzrostu, więc bramka mówi weak i raportuje krzywa@x zamiast Ip_max.
   Skutek mały (1 mm A: 1,185 vs 1,260, 6 %; 8,39 B: 3,150 vs 3,169), ale etykieta myli. Do rozważenia: okno
   `PEAK_SHAPE_LOOK_V` 0,15-0,20 V albo kryterium „spadek do końca gałęzi".
4. **Słaby pik przy stromej bazowej (12,39 B katod).** E_x stycznych (0,159 V) leży na zboczu 0,19 V przed minimum
   (-0,029 V); przy stromej bazowej krzywa@x (-1,418) i Ip_max (-1,053) różnią się 35 %. To nie błąd kodu, tylko
   wrażliwość definicji; w artykule podawać obie wartości dla pików słabych (już są w CSV/JSON).

Reszta (80 pików OK, 4 klasy b) nie wymaga zmian w kodzie: bazowe na wykresach leżą na płaskim odcinku przed onsetem,
punkty Ip w maksimum/minimum lub na ramieniu przy E_x, zgodnie z procedurą z 20.08.

## Propozycja poprawki (NIEWDROŻONA, czeka na OK Pawła)

Plik: `wyniki_analizy/setup_fallback_20260823.py` = kopia komórki SETUP (cells[1]) notebooka + fallback plateau dla piku
katodowego. Notebook nietknięty. Anodowy bez zmian: `znajdz_pik_anodowy` bierze argmax w oknie (0,05; 0,80) V, więc
nigdy nie zwraca None z powodu braku maksimum; fallback nie ma tam sensu.

Mechanizm: gdy `find_peaks` nie znajdzie minimum o prominencji >= max(5 % Ip_a, 20 nA) w oknie E <= Ep_a − 0,02 V,
bierzemy minimum wygładzonego prądu w tym oknie jako pseudo-pik; bazowa ta sama (reguła onset); `ksztalt='weak'`,
`metoda='fallback plateau'`, Ip = krzywa@x (jak dla każdego słabego piku). Trzy bezpieczniki, bez których fallback
włączał się fałszywie na 12 plikach bez fali redukcji (3 mm B, 8,39 B, 8,39 C; Ep_c = −0,5 V, Ip_c dodatnie):
minimum >= 5 pkt przed końcem gałęzi, bazowa musi być z reguły onset (nie „ogon nad zc"), krzywa@x musi leżeć pod bazową.

Weryfikacja (`walidacja_vs_tabela_bartka.py wyniki_analizy/setup_fallback_20260823.py --skan ostatni`,
csv `wyniki_analizy/walidacja_fallback_20260823.csv`, porównane z `walidacja_v9_skan_ostatni.csv`):
- 45 elektrod, 0 crashy; zmiany > 0,1 % poza 2 mm b: ZERO (wszystkie pola Ipa/Ipc/max/krzywa@x/styczne/ΔEp identyczne).
- Wszystkie 184 pliki (4 skany), stary kod vs nowy: fallback włączony w 7 plikach (2 mm b x4, 13,39 B skany 1-3),
  w pozostałych 177 plikach zero zmian w Ep_a, Ep_c i wszystkich odczytach Ip. Tam, gdzie wcześniej był pik, fallback nie wchodzi.
- 2 mm b katod: Ip_c −0,920 / −0,930 / −0,932 / −0,939 µA (skany 1-4), Ep_c 0,105-0,115 V, Ip_max −0,83..−0,88,
  styczne −1,04..−1,06. xlsx −0,793 (automat −18 %, Ip_max −10 %). Pik istnieje, różnica to bazowa Bartka; do jego kotwic.
- 13,39 B katod skany 1-3: Ip_c −4,292 / −4,431 / −4,524 µA (Ep_c −0,20 V), skan 4 bez zmian −4,563; spójny trend
  z rozpiską Bartka −4,612 dla skanu 4.
- Statystyki tabeli po poprawce: Ip_a 1,1 % / 0,7 % (bez zmian), Ip_c 3,2 % / 1,2 % na 43 pikach (było 2,8 % na 42;
  wzrost to wyłącznie dodany 2 mm b z −18 %).

Diff (cells[1] notebooka -> setup_fallback_20260823.py):
```diff
--- HURNY_CV_Analyzer.ipynb cells[1]	2026-08-22 23:48:57
+++ wyniki_analizy/setup_fallback_20260823.py	2026-08-22 23:48:24
@@ -53,6 +53,7 @@
 # 45 elektrod, skan 4: Ip_a 1,5 %, Ip_c 3 %), a przecięcie stycznych daje ~8-14 % więcej.
 # Bartek sam ma rozstrzygnąć definicję (mail 11.08) — do tego czasu 'krzywa';
 # obie wartości są ZAWSZE w wyniku (Ip_*_krzywa, Ip_*_styczne).
+FALLBACK_MARGIN_PKT  = 5          # fallback plateau: minimum musi leżeć >= 5 pkt przed końcem gałęzi
 SLABY_PIK_STYCZNE    = False      # True = dla piku słabego (ramię) raportuj przecięcie
                                   # stycznych (procedura prof. z 18.08); False = jak tabela Bartka
 
@@ -395,9 +396,18 @@
     prog = max(0.05 * abs(pik_a['Ip_a']) * 1e-9, 20e-9)
     peaks, props = find_peaks(-Is, prominence=prog)
     keep = [(p, props['prominences'][i]) for i, p in enumerate(peaks) if maska[p]]
-    if not keep:
-        return None
-    best = max(keep, key=lambda t: t[1])[0]
+    fallback = False
+    if keep:
+        best = max(keep, key=lambda t: t[1])[0]
+    else:
+        # FALLBACK PLATEAU (propozycja 23.08.2026, NIEWDROŻONA w notebooku): brak lokalnego
+        # minimum o wymaganej prominencji (plateau albo bardzo płytki pik). Bierzemy
+        # minimum wygładzonego prądu w oknie poniżej Ep_a; dalej ta sama bazowa onset.
+        idx_w = np.where(maska)[0]
+        best = int(idx_w[np.argmin(Is[idx_w])])
+        if best >= n - FALLBACK_MARGIN_PKT:      # minimum na końcu gałęzi = brak plateau, nie zgadujemy
+            return None
+        fallback = True
     Ep_c = float(E_down[best])
     # zero-crossing (start redukcji) miedzy apexem a pikiem katodowym
     seg = np.where((E_down < pik_a['Ep_a'] - 0.02) & (E_down > Ep_c))[0]
@@ -427,6 +437,12 @@
     bl = bl_at(Ep_c)
     # normalizacja: reverse biegnie w dół E, pik jest minimum ⇒ Eb=-E, y=-I
     dp = ip_dwie_procedury(-E_down, -Is, int(best), lambda eb: -bl_at(-eb))
+    if fallback:
+        if regula != "onset" or dp["Ip_krzywa_x"] is None or dp["Ip_krzywa_x"] <= 0:
+            return None                          # brak płaskiej bazowej albo krzywa nad bazową: to nie jest pik
+        dp["shape"] = "weak"; dp["metoda"] = "fallback plateau"
+        dp["Ip"] = dp["Ip_krzywa_x"] if (dp["Ip_krzywa_x"] is not None and not SLABY_PIK_STYCZNE) else \
+                   (dp["Ip_styczne"] if dp["Ip_styczne"] is not None else dp["Ip_max"])
     return {
         "Ep_c":     Ep_c,
         "Ip_c_raw": float(I_down[best] * 1e9),
@@ -589,4 +605,4 @@
     </div>"""))
 
 
-print(f"✅ Setup zakończony (cykl: {KTORY_CYKL}, Ip: {IP_DEFINICJA}, słaby pik→styczne: {SLABY_PIK_STYCZNE}). Możesz uruchomić kolejne komórki.")
+print(f"Setup (fallback plateau, propozycja 23.08) zakończony (cykl: {KTORY_CYKL}, Ip: {IP_DEFINICJA}, słaby pik→styczne: {SLABY_PIK_STYCZNE}). Możesz uruchomić kolejne komórki.")
```
