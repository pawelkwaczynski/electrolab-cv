# PeakWise, raport z nocy 22/23.08.2026 (sesja autonomiczna, 10 h)

Zero wysyłek, zero zmian w notebooku, zero gita, zero kasowania. Wszystko poniżej to nowe pliki w `wyniki_analizy/` i `07_dane_bartka_20260822/`.

## 1. Triage 45 elektrod vs tabela xlsx (`RAPORT_triage_45_elektrod_20260822.md`)
- 88 pików: **80 zgodnych (<= 4 %)**, błąd śr. 1,9 %, mediana 1,0 %.
- 7 niezgodnych po stronie tabeli: 3 odczyty z innego skanu (1 mm A, 12,39 C, 12,39 B), 1 błąd przepisywania (13,39 B),
  1 bez dopasowania do żadnego pliku (8,39 B), 2 graniczne (8,39 C, 1 mm C). Lista do Bartka w raporcie.
- 1 luka automatu: pik katodowy na plateau bez minimum (2 mm b; ten sam mechanizm gubił 13,39 B na skanach 1-3).
- **Propozycja poprawki NIEWDROŻONA** (`setup_fallback_20260823.py`, sekcja w raporcie triage): fallback plateau
  z 3 bezpiecznikami; na 184 plikach włącza się dokładnie w 7, w 177 zero zmian. Czeka na OK Pawła, potem backup notebooka i wdrożenie.

## 2. Powtarzalność między skanami (`RAPORT_powtarzalnosc_3_skany_20260822.md`, wykres `Ip_vs_skan_per_seria_20260822.png`)
- Skany 2-4: CV Ip_a mediana 1,7 %, Ip_c 0,5 %. Automat jest na poziomie szumu pomiaru.
- Skan 1 zawyża Ip_a o medianę +14 % (zakres −23..+61 %). Tłumaczy w całości lipcowe 9-10 %.
- **Odkrycie: dryf skanu 1 koreluje z ΔEp (Spearman 0,80, p = 1e-10), nie z wielkością piku.** Hipoteza: kondycjonowanie
  zależy od kinetyki/oporu. Do Łukasza.
- Anomalie geometrii: warstwa 0,24 mm daje największy Ip, 0,40 najmniejszy; kontakt 8,39 i 12,39 poniżej trendu, 8,39 spada
  monotonicznie skan po skanie. Pytanie do Bartka o stan tych elektrod.

## 3. Literatura (`LITERATURA_automatyczna_analiza_CV_20260822.md`, 64 DOI potwierdzone Crossref)
- 12 narzędzi open source, żadne nie ma walidacji vs ręczny odczyd na zbiorze elektrod. Luka potwierdzona.
- Cytat gotowy: Harvey, Analytical Chemistry 2.1, s. 750 PDF: „a precision of ±1-3% is reasonable" dla Ip.
- Obowiązkowe: Górski/Jakubowska (AGH) 2014 automatic baseline; Macedo/Hogan 2024/26 (błąd liniowej bazowej dla piku
  powrotnego, trzeba zaadresować przy naszej bazowej katodowej); Ha/Hwang 2025 Anal. Chem. (AI, MAPE 3,37 %).
- Ryzyko nałożenia na geometrię: Rojas/Crespo 2024 (średnica x warstwa, FcMeOH), Crapnell/Banks 2022 (długość kontaktu),
  Rodrigues 2025 (DOE). Nasz wkład musi być „metoda odczytu + walidacja + błędy ręczne", nie „optymalizacja geometrii".
- ⚠️ W liście jest „Kwaczyński, Poltorak 2023 Sci. Rep., 2025 Analyst": sprawdzić, czy to Karolina (UŁ), i jak to cytować.
- Brak w literaturze badania inter-operator dla bazowej w CV: drugi czytający (Łukasz?) + ICC domyka lukę.

## 4. Format .opju (`07_dane_bartka_20260822/OPJU_FORMAT_NOTATKI.md`, `opju_extract/opju_decode.py`)
- Zmapowane: nagłówek, 1757 rekordów kolumn, własna kompresja XOR na bitach double (wariant Gorilla, int64 predykcja),
  dane zgodne z txt, ślady 10 Linear Fitów, 4 Polynomial Fitów, Peak Analyzer (ALS i End Points Straight Line) na Book19.
- Nierozwiązane: rejestr delty D przy izolowanym tagu `d` (~2 % wierszy) i okno bitowe dla wartości blisko zera.
  Błąd propaguje, pełnego CSV nie ma. **Zamykam ten wątek**: eksport z Origina (10 min) daje 100 %, dekoder to 2 x 1 h bez końca.
- Potencjalny open source (pierwszy czytnik OPJU), ale dopiero z kontrolowanym plikiem testowym od Bartka.

## Do Pawła (decyzje)
1. OK na wdrożenie fallbacku plateau do notebooka (backup + walidacja są gotowe).
2. Wysłać Bartkowi listę 7 pików + pytanie o 2 mm b i o stan elektrod 8,39 / 12,39 (tekst poniżej).
3. Czy Karolina w literaturze to „nasza" Karolina i czy chcemy ją w cytowaniach/autorach.

## Tekst do Bartka (WhatsApp, po jego odpowiedzi na 3 piki)
> Przeleciałem automatem całą tabelę z 45 elektrod przeciwko skanowi 4. 80 z 88 pików zgadza się do 4 %, większość poniżej 2 %.
> 7 wpisów w tabeli nie pasuje do skanu 4, wygląda na inny skan albo przepisanie:
> 1. 1 mm A anodowy 1,247 to skan 1 (skan 4: ok. 1,2)
> 2. 12,39 C katodowy −5,097 to skan 1 (skan 4: −5,32)
> 3. 12,39 B katodowy −1,338 to skan 2 (skan 4: −1,42)
> 4. 13,39 B katodowy −3,058 w tabeli, dobre jest Twoje −4,6
> 5. 8,39 B anodowy 3,377 nie pasuje do żadnego skanu (skan 4: 3,15)
> 6. 8,39 C anodowy i 1 mm C katodowy: różnica 4 %, poproszę o kotwice jak w pptx
> 7. 2 mm b katodowy: nie widzę minimum na gałęzi, gdzie postawiłeś punkt i bazową?
> I pytanie z innej beczki: 8,39 (A, B, C) i 12,39 B mają wyraźnie niższe prądy niż sąsiednie iteracje, a 8,39 spada z każdym skanem. Coś było z tymi elektrodami (druk, kontakt, pęknięcie)?

## 5. Test z literatury: liniowa bazowa katodowa ZANIŻA Ip_c o ~25 % (ostrzeżenie Macedo/Hogan potwierdzone na naszych danych)
- Dla FcMeOH (układ odwracalny) Ip_c/Ip_a powinno wynosić ~1. Nasza bazowa (= procedura Bartka, zgodność 1-3 %) daje
  **medianę 0,715** (IQR 0,67-0,76) na 42 elektrodach. Poprawka Nicholsona 1966 (Ip_c0/Ip_a + 0,485·I_sp0/Ip_a + 0,086)
  z tych samych plików daje **medianę 0,971** (IQR 0,91-1,04).
- Różnica nasza minus Nicholson: −0,25, silniej ujemna przy małych ΔEp (Spearman −0,47), czyli zaniżenie rośnie, gdy
  ogon dyfuzyjny piku anodowego wchodzi pod pik katodowy.
- Wniosek: automat i Bartek są ZGODNI, ale OBAJ systematycznie zaniżają prąd katodowy, bo prosta przed onsetem na gałęzi
  powrotnej nie opisuje zanikającego ogona anodowego. To nie błąd kodu, to błąd metody ręcznej, który automat wiernie odtwarza.
- Do artykułu: (1) raportować Ip_c także z poprawką Nicholsona albo z bazową ogonową (ekstrapolacja zaniku t^-1/2 z gałęzi
  anodowej, metoda z Macedo/Hogan), (2) IRED z tabeli Bartka traktować jako „Ip_c względem liniowej bazowej", nie jako
  prawdziwy prąd piku, (3) to mocny argument za automatem: ręcznie nikt nie policzy poprawki na 184 plikach.
- Do Łukasza: czy lab akceptuje Nicholsona jako referencję dla Ip_c, czy wolą bazową ogonową. Decyzja wpływa na ΔEp? Nie, tylko na Ip_c.
