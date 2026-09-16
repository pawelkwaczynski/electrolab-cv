# Powtarzalność Ip między skanami, 46 elektrod (22.08.2026, noc)

Skrypt `powtarzalnosc_3_skany_20260822.py`, csv obok. Automat (notebook, ostatnia wersja) na każdym z 4 plików elektrody.
Bartek do statystyki bierze 3 ostatnie skany, skan 1 zawsze odrzuca.

## Liczby
- Ip_a, skany 2-4: CV mediana **1,7 %**, średnia 2,3 %, max 17,9 % (46 elektrod).
- Ip_c, skany 2-4: CV mediana **0,5 %**, średnia 0,7 %, max 3,7 % (41 elektrod z pikiem katodowym).
- **Skan 1 vs skan 4 (Ip_a): mediana +13,9 %, średnia +14,6 %, zakres −23..+61 %.** Skan 2 vs 4: +3,0 %.

## Wnioski
1. Skan 1 to kondycjonowanie elektrody, systematycznie zawyża Ip_a o ok. 14 %. To w całości tłumaczy lipcowe 9-10 % błędu
   walidacji (liczona na skanie 1 do tabeli ze skanu 4). Reguła Bartka „skan 1 odrzucam" ma pomiar za sobą.
2. Powtarzalność automatu między skanami 2-4 (1,7 % / 0,5 %) jest tego samego rzędu co zgodność automat vs ręczny odczyt
   (1-2 %), czyli automat jest na granicy szumu pomiaru, nie metody.
3. Seria kontaktów 8,39 mm: Ip_a spada monotonicznie skan po skanie (A: 6,55 > 5,37 > 5,01 > 4,80; B: 5,07 > 3,15).
   To nie szum, to degradacja/ustalanie elektrody o krótkim kontakcie, materiał do Discussion (krótszy kontakt = większy opór = wolniejsze ustalanie?).
4. 12,39 B: skok 2,01 > 2,81 µA między skanem 2 a 3 przy bardzo małym piku, podejrzenie, że automat zmienia wybór piku/bazowej.
   Do sprawdzenia w triage (osobny raport).

## Do artykułu
Tabela „repeatability scans 2-4" per seria + wykres Ip vs numer skanu dla 8,39 i 4 mm. Zdanie do Methods: first scan discarded
as conditioning (median +14 % overestimation of anodic peak current relative to the 4th scan, n = 46).

## Odkrycie: dryf skanu 1 koreluje z ΔEp, nie z wielkością piku
- Spearman dryf(s1 vs s4) ~ Ip_a: 0,03 (p = 0,83), brak związku.
- **Spearman dryf ~ ΔEp(skan 4): 0,80 (p = 1e-10), n = 42.** Elektrody o dużej separacji pików (wolna kinetyka lub
  większy opór nieskompensowany: 4 mm, 13,39, 8,39) kondycjonują się najmocniej (20-60 %), elektrody 1 mm z ΔEp 0,23-0,48 V
  tylko 6-8 %.
- Interpretacja (hipoteza do Łukasza): pierwszy skan na świeżej powierzchni PLA/grafen zawyża prąd anodowy tym bardziej,
  im gorsza kinetyka/wyższy opór; po 1 cyklu powierzchnia i warstwa podwójna się ustalają. Jeśli to opór, to dryf
  powinien skalować z iR, czyli z Ip·R; sprawdzić po otrzymaniu R z EIS albo z nachylenia ΔEp vs v.
- Per seria, mediana dryfu s1 vs s4: średnica 9,3 %, warstwa 10,3 %, kontakt 17,0 %. Wykres: `Ip_vs_skan_per_seria_20260822.png`.
- Obserwacja na wykresie: w serii wysokości warstwy 0,24 mm daje największy Ip, 0,40 najmniejszy (niemonotoniczne);
  w serii kontaktu 12,39 i 8,39 wypadają poniżej trendu (12,39 B ma Ip 2,8 µA, reszta serii 6-8). Do zapytania Bartka,
  czy te elektrody były uszkodzone albo inaczej drukowane.
