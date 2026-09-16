# Wiedza projektu — PeakWise
*Żywy dokument wiedzy. Ostatnia aktualizacja: 19.08.2026. Zasada: przy każdej zmianie kodu rób backup poprzedniej wersji.*

---

## 1. Co to jest / cel

Analizator CV dla **elektrod drukowanych 3D (FDM/SPE)** — część większego projektu
**PeakWise** (interaktywny symulator „cyfrowe laboratorium"). Podział ról:
- **Bartek Hurny** (chemia, UŁ): druk elektrod 3D + pomiary CV w NOVA (TXT/Excel).
- **Paweł** (Python): analizator CV → piki → paczka `experiment.json` dla silnika 3D.
- **Grzesiek** (Unreal): odtwarza eksperyment, animuje, rysuje CV na żywo.

Sonda modelowa: **FeMeOH** (ferrocenometanol, odwracalna para redoks, światłoczuła → cele w folii).

## 2. Co zakładaliśmy (metoda Bartka)

- Krzywa CV (I od E), zwykle 3–4 skany.
- **Pik anodowy** (utlenianie) = maksimum prądu na gałęzi forward.
- **Pik katodowy** (redukcja) = minimum prądu na gałęzi reverse.
- Dla każdego: potencjał **Ep** + natężenie **Ip = pik − baseline** (baseline = skośna linia
  przez punkty przed pikiem; potwierdzone w `Bartek_Wytlumaczenie_zczytywania_pikow.pptx`).
- Parametry elektrody: **ΔEp = Epa − Epc**, |Ipa/Ipc|. Wpływ geometrii: średnica WE, liczba
  warstw (wysokość), długość/pozycja kontaktu.

## 3. Co było błędne i naprawione

| Bug | Objaw | Naprawa |
|---|---|---|
| **pik katodowy** (zgł. Bartek 7.07) | szukany jako max dI/dE w wąskim oknie [Epa−0,30] → zwracał +0,5 V (śmieć) | lokalne minimum prądu (find_peaks na −I) w całym zakresie <Epa, prominencja skalowana do piku anodowego |
| **moja pomyłka „raw Ip"** | myślałem, że Bartek nie odejmuje baseline | pptx pokazał: odejmuje baseline dla OBU pików; wycofane |
| **baseline stałe okno** | nie generalizowało (61% błędu katodowego) | ogon dyfuzyjny NAD startem redukcji (zero-crossing), adaptacyjnie per krzywa |

## 4. Biblioteki i technologie

- **Python / Google Colab** (jeden notebook, fallback lokalny).
- `numpy`, `pandas` (parser NOVA TXT: `Potential applied (V)` / `WE(1).Current (A)`).
- `scipy.signal`: `find_peaks`, `savgol_filter`.
- `matplotlib` (woltamperogram, wykres nakładkowy porównania elektrod).
- `IPython.display.HTML` (karty wyników), `google.colab.files`.
- Do analizy materiałów od Bartka (moja praca, nie w notebooku): `openpyxl` (tabele xlsx),
  `pypdf` (korespondencja), `python-pptx` (wyjaśnienia), `ffmpeg` (klatki z wideo z labu).

## 5. Co mamy (stan)

- Notebook `PeakWise_CV_Analyzer.ipynb` z **auto-baseline** + backup `.BACKUP_20260710`.
- Ground-truth: tabele Bartka `SPE ITERATIONS DATA.xlsx` + `FDM SPE EXPERIMENTS (1).xlsx`
  (ręczne odczyty Ip/Ep per elektroda), 184 pliki laboratoryjne.
- Wyjaśnienie metody: `Bartek_Wytlumaczenie_zczytywania_pikow.pptx`.
- Pełny przegląd + audyt: `PRZEGLAD_KODU_2026-07-10.md`.

**Walidacja (45 elektrod z tabeli Bartka × 4 skany = 184 pliki):**
| | lipiec (skan 1, stara bazowa) | **20.08.2026 (skan 4, bazowa przed onsetem)** |
|---|---|---|
| Potencjały ΔEp | ✓ zgodne | bez zmian |
| **Ip anodowe (IOX)** | 9,9 % | **1,1 % (mediana 0,7 %)** |
| **Ip katodowe (IRED)** | 9,6 % | **2,8 % (mediana 1,1 %)** |
| Crashe | 0 | 0 |
Raport: `wyniki_analizy/RAPORT_walidacja_skan4_baseline_20260820.md`, skrypt
`walidacja_vs_tabela_bartka.py`. Cel (rozrzut Bartka 10-20 %) przebity o rząd wielkości.

## 6. Co odkryliśmy (insighty)

- **Elektrody 3D są silnie quasi-odwracalne** — duża separacja pików (ΔEp 0,3–0,9 V),
  pik katodowy leży daleko od anodowego (przy potencjale ujemnym). To fizyka, nie anomalia
  (ΔEp > 59 mV/n = wolniejszy transfer elektronu).
- **Baseline katodowy MUSI być fitowany NAD startem redukcji** (zero-crossing prądu), nie
  w stałym oknie — inaczej łapie strefę „diving" i psuje znak (61% → 10% błędu).
- **Baseline to metoda eksperta** (skośna linia na oko) — ale reguła jest spójna, więc
  DA SIĘ ją zautomatyzować deterministycznie. Nie trzeba ML.
- **Rozrzut własny eksperta** ±0,7–1,2 µA między skanami — realny cel to „w granicach jego
  rozrzutu", nie „co do nanoampera".
- Bartek czasem miesza elektrody w jednym uploadzie — trzymać „1 folder = 1 elektroda".

## 7. Innowacje / obietnice / kierunek

- **Onset-adaptive diffusion baseline** — nasza autorska metoda: wykryj start procesu
  redukcji per krzywa, fituj ogon dyfuzyjny nad nim, ekstrapoluj do piku. Deterministyczne,
  wytłumaczalne, publikowalne (zgodne z grantem „reguły najpierw, ML tylko gdy da poprawę").
- **Pełna automatyzacja bez trybu ręcznego** (Origin już to Bartkowi daje — auto ma wartość).
- Do dostrojenia: D=4mm anodowe lekko zaniża — dostroi się punktami kotwicznymi od Bartka.
- Otwarte: metoda styczna dla słabych pików (slajd 6 pptx — Bartek rozwinie na prośbę);
  ewentualne uśrednianie KRZYWYCH tej samej elektrody (agregacja WYNIKÓW już jest — patrz niżej).

## 7a. experiment.json dla Unreala — ZROBIONE (20.07.2026)

- **Schemat `electrolab3d.experiment/1.0`**: 1 paczka = 1 elektroda; `scans[]` z pełną
  krzywą (E_V/I_A), `apex_index` (podział gałęzi), piki (Ep, Ip po baseline, Ip raw,
  baseline, index), `derived` (ΔEp, |Ipa/Ipc|) + `aggregate` (mean/SD/n z powtórzeń).
- W notebooku: nowe komórki „Eksport experiment.json" (funkcje `zbuduj_experiment_json`,
  `zapisz_experiment_json`, parametr decymacji). Backup przed zmianą: `.BACKUP_20260720`.
- **Deliverable dla Grześka:** `eksport_unreal/` — 46 paczek JSON (komplet 184 plików labu,
  serie WE/LEYER HEIGHT/contact lenght, ~7,9 MB) + `EXPERIMENT_JSON_SPEC.md` (opis pól,
  jak rysować markery i baseline, jak animować CV bez osi czasu).
  **20.08.2026: schemat 1.1** — paczki przeliczone nową bazową; do każdego piku doszły
  `shape`, `method`, `baseline_window_V`, `readings_nA{maximum, curve_at_tangent_x,
  tangent_intersection}`, `tangent_x_V`; `cycle_used` = "ostatni". Nic nie usunięto, paczki 1.0
  w `eksport_unreal_v1.0_20260720/`.
- Walidacja 3-przebiegowa: (1) generacja 184/184 plików bez błędów (167 par pików,
  17 tylko-anodowych), (2) wykonanie komórek notebooka end-to-end headless,
  (3) audyt spójności paczek: znaki Ip, Ip=raw−baseline, ΔEp i ratio przeliczone, indeksy
  w zakresie — 0 problemów.
- Przy okazji naprawione ścieżki lokalne w notebooku (projekt przeniesiony 18.07).

### ❓ 3 pytania do Bartka — WYSŁANE 20.07; ODPOWIEDŹ CZĘŚCIOWA mailem 11.08

> **Aktualizacja 12.08.2026 (mail Bartka z 11.08, 15:37): ODPOWIEDŹ + NOWA PREZENTACJA.**
> Załącznik `Wytłumaczenie.pptx` to NOWA wersja (1,1 MB vs 959 KB starej): slajd 1 = opis
> metody stycznej, slajdy 2-6 = **5 kompletnych przykładów z liczbami** (elektroda, nr skanu,
> punkty 3 stycznych, przecięcia, Ip). Kopia w projekcie:
> `Bartek_Wytlumaczenie_styczne_5przykladow_20260811.pptx`; pełna ekstrakcja + rachunki
> kontrolne + wykryte literówki: `Bartek_styczne_5przykladow_20260811_EKSTRAKCJA.md`.
> Co to domyka: **pyt. 2 (kotwice baseline 4mm)** — punkty na slajdach 2-4; **pyt. 3 (styczna)**
> — procedura + przykłady; **pyt. 1 (cykl)** — przykłady na skanie 4 (OSTATNIM), skan 1 tylko
> „przypadkiem"; spójne z jego mailem z 07.07 („dla ostatniego skanu") i z Łukaszem w ITIES.
> OTWARTE: definicja Ip — slajd 2 liczy z KRZYWEJ, slajd 4 z PRZECIĘCIA STYCZNYCH (różnica
> 7-19%); Bartek sam obiecał się upewnić. Obiecał też „więcej przykładów jutro" (12.08).
> Szczegół: potencjały odczytuje jako punkty danych, wartości z przecięć są interpolowane →
> w porównaniach tolerować odchyłkę rzędu kroku próbkowania.
> **ZROBIONE 20.08.2026:** ostatni skan + nowa bazowa + styczne dla słabych pików; walidacja
> powtórzona: 1,1 % / 2,8 % (raport w `wyniki_analizy/`). Pytanie 1 rozstrzygnięte danymi
> (skan 4), pytanie 2 kotwicami, pytanie 3 zaimplementowane; OTWARTE tylko, czy Bartek chce
> w tabeli krzywą (jak dotąd) czy styczne (+8-14 %).

> **Aktualizacja 11.08.2026:** Bartek odezwał się (czat) — robi zadanie, zapytał ile przykładów
> ma przygotować do metody stycznej. Ustalenia: (a) baseline wyznacza tak samo jak wcześniej,
> więc go NIE powtarza — kotwice bierzemy z jego „2. przykładu" (to domyka pytanie 2);
> (b) poprosiłem o **5 przykładów stycznej (minimum 3)**, z naciskiem na krzywe ze słabo
> wykształconym pikiem + 1–2 „ładne" jako odniesienie; do każdego: nazwa pliku, numer skanu
> i dwa punkty stycznej (E, I) albo zrzut z Origin + odejmowana wartość.
> **Pytanie 1 (który cykl w Origin) nadal BEZ ODPOWIEDZI** — przypomniane w tej samej wiadomości.
> Od 11.07 nie było maila od Bartka; wątek „MVP gotowy" kończą 3 wiadomości Pawła (15.07, 20.07).

1. **Który cykl czyta w Origin** przy pliku multi-cyklowym? Notebook bierze PIERWSZY
   (`wykryj_cykle`); Łukasz w ITIES (20.07) rozstrzygnął odwrotnie (brać OSTATNI). To osobne
   układy — walidacja 9-10% robiona na pierwszym cyklu, więc bez odpowiedzi NIE zmieniać.
2. Punkty kotwiczne baseline dla D=4mm (auto lekko zaniża Ip anodowe).
3. Rozwinięcie metody stycznej dla słabych pików (slajd 6 pptx).

## 8. Powiązanie z ITIES (siostrzany projekt)

Oba to analizatory CV z tym samym rdzeniem. Co PeakWise dał ITIES / czym się dzielą — patrz
`~/Desktop/MVP_Colab/ITIES/WIEDZA_PROJEKTU_ITIES.md` sekcja 8. Kluczowy transfer: **baseline
z PeakWise → poprawne natężenia w ITIES** (odblokowuje stężenia/kalibrację i multi-substancję).
Docelowo wspólny silnik `electrochem-core` (open-science-accessibility-suite).

## Literatura lokalna (dodane 19.08.2026)
Podręczniki i artykuły pobrane legalnie (open access) leżą w `~/Biblioteka_ksiazek/`.
Pełny spis z opisem „do czego który" w osobnych notatkach (nie w repo).
Najważniejsze dla PeakWise:
- **`chem/cyclic-voltammetry-practical-guide-elgrishi.pdf`** (10 str., ACS J. Chem. Educ. 2018) —
  kanoniczny przewodnik po CV: konwencje odczytu piku, linia bazowa, wpływ szybkości
  skanowania. Pierwsze źródło przy pytaniu „czy robimy to poprawnie", cytowalny w Methods.
- **`chem/harvey-analytical-chemistry-2.1.pdf`** (1122 str., CC BY-NC-SA) — LOD/LOQ,
  walidacja metody, propagacja niepewności.
- **`chem/metrological-traceability-in-chemical-measurement...pdf`** (Eurachem, 45 str.) —
  spójność pomiarowa i wzorce, pod pytania recenzenta o wiarygodność liczb.
- **`chem/linear-sweep-voltammetry-at-diffuse-charge...pdf`** (47 str., Poisson-Nernst-Planck) —
  teoria kształtu krzywej.

Procedury odczytu piku (dwie, zależnie od jakości piku), pułapka cyrkularności D i tabela
reżimów dyfuzji wg średnicy elektrody: skill **`cv-analiza-pikow`**.
⚠️ PeakWise i ITIES to OSOBNE projekty. Literatura jest wspólna, wnioski NIE.

## Wątek poboczny: generatywne 3D vs CAD parametryczny (19.08.2026)
Dotyczy druku 3D, nie analizy CV. Powstało przy rozmowie Pawła z prof. Półtorakiem
o modelu `Hunyuan3D-Buffalo 1.0` (Tencent, 05.08.2026).

- Model generuje **siatki GLB** z tekstu (plus edycja i QA o scenie). Do elektrod i celek
  **nieprzydatny**: brak wymiarów, tolerancji i powtarzalnej geometrii, a to jest cała
  wartość drukowanego elementu w elektrochemii.
- Na 19.08 **kod i wagi niewydane** (tylko preprint + strona projektu).
- 🔴 Licencja rodziny Hunyuan3D **wyklucza Unię Europejską** (i UK, Koreę Płd.), więc nawet
  po wydaniu odpada dla pracy na UŁ.
- **Użyteczny kierunek:** LLM piszący kod parametryczny (CadQuery / build123d / OpenSCAD)
  → STEP + skrypt. Geometria elektrody staje się wersjonowalnym kodem, a nie plikiem STL
  bez historii; skrypt można dołączyć do publikacji jako supplementary.

Pełna analiza z linkami: LifeOS `40_Resources/Clippings/Hunyuan3D-Buffalo 1.0 - ocena pod ITIES.md`.

## Ścieżka „zarobić / wypromować": kurs NAVOICA (MNiSW / OPI PIB) — wątek z lutego 2026
Gmail: „Zapytanie o możliwość realizacji kursów Navoica w ramach Koła Informatyki (AHE / UŁ)",
22.02.2026 Paweł → NAVOICA (OPI PIB); **odpowiedź 23.02.2026: Maciej Kolankowski**, kierownik
projektu NAVOICA, Dział Innowacyjnych Technologii Kształcenia OPI PIB. **Paweł NIE odpowiedział (stan 20.08.2026, 6 miesięcy ciszy).**

Zaproponowane kursy: (1) „Projektowanie elektrod do chemii analitycznej metodą druku 3D oraz
automatyczne przetwarzanie wyników analizy w Pythonie" (AHE+UŁ, czyli PeakWise jako kurs),
(2) „Analityka danych w Pythonie, SQL i AI" (sam Paweł).

Co powiedział OPI:
- Kursy mile widziane, publikacja bez ograniczeń (platforma MNiSW, system kluczowy dla nauki).
- Formalnie: **jedna umowa uczelnia–OPI** (+ powierzenie danych osobowych), bezterminowa, bez listy
  kursów; podpisuje Rektor, proceduje jednostka, przy której jest koło (AHE) albo UŁ. Trzeba
  rozstrzygnąć, kto jest organizatorem którego kursu.
- **Dwie drogi:** (a) własnym sumptem: robimy zasoby, OPI pomaga osadzić kurs na platformie;
  (b) **z finansowaniem: konkurs dla uczelni co roku w kwietniu** (wyniki w wakacje, produkcja od
  nowego roku akademickiego); finansuje opracowanie merytoryczne i zasoby (np. filmy), kursy
  robią metodycy OPI, warunek: uczelnia wpisuje kurs do programu kształcenia. Kwiecień 2026
  przepadł → **następny nabór kwiecień 2027**.
- Formaty: filmy, audio, kilkanaście typów ćwiczeń, grafiki, tekst; dokumentację przyślą;
  **brak sandboxa do ćwiczeń z kodem**.
- Zaproszenie na rozmowę Teams / telefon / na miejscu w Łodzi.

Dlaczego to pasuje do PeakWise teraz: walidacja 1-3 % + cykl 6 odcinków wideo z podziału z 21.02
(Bartek: elektroda i pomiar, Paweł: Python, Grzesiek: Unreal) to gotowy materiał na kurs (1),
a kurs na platformie ministerialnej to widoczność dla Bartka (kariera) i dla AHE/UŁ.
**Do zrobienia:** odpisać Kolankowskiemu (przeprosić za zwłokę, zaproponować rozmowę, zapytać
o termin naboru 2027 i dokumentację formatów), ustalić z dziekanem Wojciechowskim, czy AHE
podpisze umowę ramową.

## Korespondencja z Bartkiem 21.08.2026: prośba o dane do walidacji co do bitu
- 21.08 10:24 mail w wątku „MVP gotowy" WYSŁANY (wynik 1,1 % / 2,8 % vs tabela, 3 prośby: punkty bazowej
  E1,I1,E2,I2; jedna definicja Ip na piśmie; jeden numer skanu + pełna precyzja). 11:07 mail do Grześka (paczka 1.1).
- Bartek odpisał na WhatsApp (nie mailem): „co chcesz" i „ile próbek, 5-10?". Mail był za długi, prośby
  zakopane pod akapitem o publikacji. Lekcja: do Bartka krótko, lista na górze.
- USTALONA PROŚBA (wysłana przez WhatsApp 21.08): **10 elektrod, dobranych, nie losowych**: po 3 z każdej serii
  (średnica, warstwa, kontakt), wszystkie 4 mm (tam bazowa robiła największą różnicę), 13,39 B (rozjazd slajd
  −4,73 µA vs tabela −3,06 µA), 1-2 ze słabym pikiem; dla każdej oba piki, ten sam skan co w tabeli.
  Zamiast arkusza: **plik projektu Origin (.opj/.opju)** z kotwicami i odczytami. Plus tabela metryczki elektrod
  (średnica, grubość warstwy, kontakt, stężenie FeMeOH, szybkość skanu, data druku) pod Methods i paczkę Unreal.
  Dlaczego 10, nie 5: na 5 jeden odstający punkt przesuwa średnią o kilka procent, nie odróżnimy błędu programu
  od kliknięcia w Originie. Kryterium: jak na 10 zejdziemy poniżej 1 %, reszta 45 niepotrzebna.
- NA MAIL PO OTRZYMANIU DANYCH (celowo nie na WhatsApp): zgoda na dane w repo (prywatne teraz, publiczne przy
  artykule; Łukasz wspominał o patencie 3DSPE), autorstwo/afiliacja/ORCID. Opcjonalnie: jedna elektroda 5 razy
  pod rząd = zmierzona powtarzalność pomiaru (dziś 10-20 % to szacunek ze słów Bartka, nie z danych).


## 2026-08-22 wieczór — dane od Bartka: 9 elektrod z kotwicami, walidacja 15/18 <= 2,4 %
- Paczka: `07_dane_bartka_20260822/` (pptx 18 slajdów, nowy `SPE iterations.opju` 19 MB, zdjęcie). Procedura Bartka
  doprecyzowana na WhatsApp: linie przez 2 punkty z danych (nie Linear Fit), Ep = przecięcie stycznych na krzywą,
  Ip = I_krzywa(Ep) − I_bazowa(Ep), skan 4 zawsze; statystyka = 3 ostatnie skany.
- Skrypt `walidacja_kotwice_bartka_20260822.py`, raport `wyniki_analizy/RAPORT_walidacja_kotwice_bartka_20260822.md`.
  Automat vs Bartek: 15 z 18 pików <= 2,4 %. 3 odstające (9-13 %) są po stronie Bartka: 4 mm B anod. odczytany ze
  skanu 1 (dowód: jego I pasuje do pliku `ba`), 4 mm C katod. i 13,39 A katod. nie pasują do żadnego z 4 plików.
- Rozjazd 13,39 B katod. (pytanie z 20.08) rozstrzygnięty: pptx −4,61 = automat −4,56; xlsx −3,06 było błędne.
  Tabela xlsx = referencja z błędami przepisywania, walidacja z 20.08 częściowo do złej referencji.
- .opju bez Origina nieczytelny (brak otwartego parsera), liczby bierzemy z pptx.
- Bartek: Francja od października (pół roku), chce spotkania z Łukaszem (promotor, współautor); po dentyście, nie naciskać.
- CZEKAMY: ponowny odczyt 3 pików, ewentualne 4 kolejne iteracje, odpowiedź Grześka.

### .opju: jak czytać bez Origina (research 22.08, web)
- Format OPJU (nagłówek `CPYUA`) NIE ma otwartego parsera: liborigin/LabPlot (bug KDE 520813, 05.2026), SciDAVis, OpenOPJ,
  Ropj czytają tylko stare .opj. `originpro` na PyPI steruje zainstalowanym Originem na Windows.
- Darmowy **Origin Viewer**: Windows 10.4 (eksport aktywnego arkusza do CSV, bez batcha/CLI); Mac 9.6.5 tylko do macOS 10.15
  (na Apple Silicon nie odpali). Viewer potrafi też File > Save Project As do starego .opj, który czyta liborigin/opj2dat.
- Wine/CrossOver: OriginLab odradza, brak wpisu w bazie CrossOver, eksperyment bez gwarancji.
- Najtańsza droga: Bartek raz wkleja w Origin Script Window:
  `fdlog.openpath(B); doc -e W { doc -e LW { string sheet$=wks.name$; expASC type:=csv path:=%B%H_%(sheet$) encoding:=utf8 shortname:=1; }; }`
  i wysyła zip CSV. Alternatywa u nas: UTM + Windows 11 ARM + Viewer 10.4 (ok. 1 h, ~15 GB, ręczny eksport arkuszy).
- Realna wartość .opju jest mała: surowe CV mamy jako 184 txt, w projekcie są tylko kotwice i wykresy Bartka, które i tak
  przepisuje do pptx. Czytać .opju warto dopiero, gdy ma dużo dopasowań, których nie chce przepisywać.

## 2026-08-23 noc — sesja autonomiczna, pełny raport: `wyniki_analizy/RAPORT_NOCNY_20260823.md`
- Triage 45 elektrod: 80/88 pików zgodnych z xlsx, 7 błędów tabeli (lista do Bartka), 1 luka automatu (plateau katodowe).
  Poprawka w `wyniki_analizy/setup_fallback_20260823.py`, zwalidowana (7/184 plików dotkniętych), NIEWDROŻONA, czeka na OK.
- Powtarzalność: skany 2-4 CV 1,7 % / 0,5 %; skan 1 +14 % i koreluje z ΔEp (Spearman 0,80). Anomalie 8,39 i 12,39.
- Literatura: `wyniki_analizy/LITERATURA_automatyczna_analiza_CV_20260822.md`, 64 DOI; luka = walidacja automatu vs ręczny odczyt + błędy ludzkie; cytaty Harvey s. 750, AGH 2014, Macedo/Hogan, Ha/Hwang 2025.
- .opju: format w 98 % zmapowany (`07_dane_bartka_20260822/OPJU_FORMAT_NOTATKI.md`, `opju_extract/opju_decode.py`), pełny dekoder nie powstał, wątek zamknięty na rzecz eksportu z Origina.
- **ODKRYCIE 23.08:** liniowa bazowa katodowa (Bartek i automat) zaniża Ip_c o ~25 %: Ip_c/Ip_a mediana 0,715 vs Nicholson 0,971 (n=42, FcMeOH odwracalny). Do artykułu i do Łukasza (Nicholson vs bazowa ogonowa). Raport nocny sekcja 5.
- 23.08 rano: fallback plateau WDROŻONY do notebooka (backup `.BACKUP_20260823`), walidacja identyczna z kopią (Ip_a 1,1 %, Ip_c 3,2 % na 43). DRAFTY w Gmailu (NIEWYSŁANE): do Bartka w wątku „MVP gotowy" (3 piki + 7 z tabeli + anomalie + skrypt Origin), do Łukasza cc Karolina (bazowa katodowa 25 %, dryf vs ΔEp, cytowania Karoliny, spotkanie). Karolina (UŁ), jej 3 prace (Sci.Rep. 2023, Analyst 2025, Talanta 2026) to tło metodyczne PeakWise.

## 2026-08-23, 12:30 — Bartek odczytał ponownie 2 z 3 pików (WhatsApp)
- 13,39 A katod.: krzywa −4,146, bazowa 1,181 → **−5,33 µA** (było −6,107). Automat −5,258: różnica 1,4 %.
- 4 mm C katod.: krzywa −7,63, bazowa 1,52 → **−9,15 µA** (było −10,025). Automat −8,935: różnica 2,4 %. Jego bazowa zmieniła się z 1,31 na 1,52 µA.
- 4 mm B anod.: twierdzi, że skan 4, ale przez screen reader; otwarte.
- Stan: **17 z 18 pików <= 2,4 %**.
- KLUCZOWE DO ARTYKUŁU: powtarzalność ręcznego odczytu tej samej osoby na tych samych danych: 13,39 A 14 % różnicy między dwoma dniami, 4 mm C 9 %. Cytat Bartka: „dziś na nowo robiłem i znów inne wyniki, nawet jak mam tak samo linie nie zmienione to wyjdzie minimalnie inaczej" oraz „to tylko dowodzi, że taki soft ma rację bytu, ta sama osoba, te same dane, ale jak jest ich dużo i wchodzi zmęczenie, to błąd ludzki wychodzi". Pomysł: formalny test intra-operator (Bartek czyta 10 elektrod x 3 dni) + ICC, domyka lukę z literatury.

## 2026-09-09 — PRZEGLĄD KODU, znaleziska dotyczące PeakWise (bez zmian w kodzie)

Pełny raport (wspólny dla ITIES i PeakWise): `../RAPORT_REVIEW_KODU_CV_20260909.md`.

⚠️ **Liczba 1,1 % / 2,8 % jest raportowana w sposób, który zawyża zgodność.**
`walidacja_vs_tabela_bartka.py`:
- l. 115-121 (`blad`): rekordy, gdzie automat nie dał wyniku, są pomijane (`continue`),
  więc wypadają z mianownika. `n` jest drukowane, ale nagłówkowa liczba już go nie niesie;
- l. 149-150: na liście „najgorsze elektrody" brak wyniku daje `ea = 0`, czyli zgodność
  IDEALNĄ, więc elektroda, na której automat poległ, nigdy się na tej liście nie pokaże;
- odtworzone: utrata detekcji na 10 najtrudniejszych z 45 elektrod zmienia raportowany
  błąd z 3,53 % na 0,61 % i opróżnia listę najgorszych;
- l. 154: `(r['IRED'] or 1)` w liczniku — przy braku IRED odejmuje 1 AMPER (l. 153 obok
  robi to poprawnie przez `or 0`);
- l. 13: `warnings.filterwarnings('ignore')` globalnie, w skrypcie, którego zadaniem jest
  wyłapywać problemy; zasłania `mean of empty slice` przy niezabezpieczonym `np.mean(ea)`
  w l. 145;
- testy prawdziwościowe (`if r.get('Ipa') and ...`) zamiast `is not None` gubią Ip = 0,0.
DO ZROBIENIA przed jakimkolwiek cytowaniem liczby: `n_ref` / `n_policzonych` /
`n_bez_wyniku` + imienna lista elektrod bez wyniku.

**Pik anodowy = `argmax` w oknie potencjału, bez wymogu lokalnego maksimum**
(`PeakWise_CV_Analyzer.ipynb` CELL 1, `_NOTEBOOK_KOD.py:338`). Gdy w oknie rośnie ściana
utleniania, Ep_a przykleja się do krawędzi okna, a status i tak jest `ok`, kształt `clear`.
Błędne Ep_a rozszerza maskę katodową, więc psuje też Ip_c. Sprawdzić, ile z 45 elektrod
Bartka ma pik na krawędzi okna — jeśli zero, przejście na `find_peaks` nie zmieni
zgodności z tabelą ręczną.

**Brak bazowej katodowej daje po cichu bazową = 0** (`_NOTEBOOK_KOD.py:437`,
`bl_at = lambda e: 0.0`), a `regula` jest ustawiana PRZED ifem, więc wynik raportuje
„ogon nad zc" mimo braku bazowej. Ip_c staje się wtedy surowym prądem. To ta sama strona
błędu, co otwarte podejrzenie zaniżenia Ip_c (0,715 vs Nicholson 0,971).
🔔 **Policzyć, na ilu z 45 elektrod poszła ścieżka awaryjna, ZANIM ktokolwiek ruszy model
bazowej.** Bartek w Originie ciągnie PROSTĄ, więc zmiana modelu to zmiana protokołu,
nie naprawa kodu — wymaga rozmowy z nim i z Łukaszem.

**Parser (l. 90-103), dwie sprawy, obie uśpione ale realne:**
- dopasowanie nazw kolumn jest wrażliwe na wielkość liter (`WE(1).current (A)` nie trafi),
  a fallback bierze kolumny 0 i 1 pozycyjnie i nie zostawia ŻADNEGO ostrzeżenia
  (zwraca `{"plik": ...}` bez `sep`/`dec`/`n`). ITIES ma to zabezpieczone
  („NIE zgadujemy osi"), PeakWise nie. SPRAWDZONE: dziś nie gryzie — l. 79 próbuje
  `utf-8-sig` jako pierwsze kodowanie, więc BOM z 180 plików znika przy dekodowaniu,
  a 4 pliki 9-kolumnowe trafiają w `WE(1).Current (A)` poprawnie;
- `dropna()` wołane OSOBNO na E i osobno na I, potem `n = min(len(E), len(I))`.
  Jedna pusta komórka prądu przesuwa całą resztę względem potencjału (na odtworzeniu
  Ip_c zmienia się o 14 %), a ostatni punkt E jest ucinany bez śladu. ITIES robi to
  poprawnie, wspólnym `dropna` po wierszach. Ta sama kopia parsera z tym samym błędem
  siedzi w `wyniki_analizy/setup_fallback_20260823.py:95-96, 102-103`.

**Wybór pliku skanu po DŁUGOŚCI NAZWY** (`walidacja_vs_tabela_bartka.py:56-58`):
`sorted(fs, key=lambda f: (len(basename), f))`, a `--skan ostatni` bierze `fs[-1]`.
To nie jest parsowanie numeru skanu, więc dowolny plik o nazwie dłuższej niż pliki danych
po cichu stanie się „ostatnim skanem". SPRAWDZONE: dziś w danych zero takich plików
i zero `.DS_Store`, więc to hardening, nie awaria.

**CELL 12 (ręczna korekta) wpisuje SUROWY prąd w pole `Ip_a_nA`** i nie aktualizuje
`pik_a`, więc w jednym wierszu CSV stoją obok siebie liczby z dwóch różnych definicji Ip
(zawyżenie 6-18 % na syntetykach). Minimum od razu: pole `korekta_reczna=True` w CSV i JSON.
