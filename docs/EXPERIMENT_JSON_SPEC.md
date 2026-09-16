# experiment.json — spec dla silnika Unreal (PeakWise)

Schemat: `electrolab3d.experiment/1.0` | Generator: `PeakWise_CV_Analyzer.ipynb` | Stan: 20.07.2026

Jedna paczka = **jedna elektroda** ze wszystkimi jej powtórzonymi skanami CV.
W tym folderze: 46 paczek wygenerowanych z kompletu danych laboratoryjnych Bartka
(184 pliki NOVA, serie: WE 1-4 mm, LEYER HEIGHT 0,16-0,40, contact lenght 7,39-13,39).

## Struktura

```json
{
 "schema": "electrolab3d.experiment/1.0",
 "generator": "PeakWise_CV_Analyzer",
 "electrode": { "id": "3 mm A", "series": "WE" },
 "technique": { "type": "CV", "solution": "FeMeOH 1 mM", "probe": "FeMeOH (ferrocenomethanol)" },
 "units": { "potential": "V", "current": "A", "peak_current": "nA" },
 "scans": [ ... ],
 "aggregate": { ... }
}
```

## scans[] — jeden powtórzony skan tej samej elektrody

| pole | znaczenie |
|---|---|
| `file` | nazwa źródłowego pliku NOVA |
| `status` | `ok` (para pików) / `tylko_anodowy` / `tylko_katodowy` / `brak_pikow` |
| `n_points` | liczba punktów krzywej po decymacji |
| `n_cycles_in_file` | ile cykli było w pliku źródłowym |
| `cycle_used` | który cykl wyeksportowano (obecnie zawsze 1 = pierwszy) |
| `decimation` | 1 = pełna krzywa; N = co N-ty punkt |
| `curve.E_V` | potencjał [V], kolejność = kolejność pomiaru (tak animować!) |
| `curve.I_A` | prąd [A], ta sama długość co `E_V` |
| `branches.apex_index` | indeks szczytu potencjału: forward = `[0..apex]`, reverse = `[apex..koniec]` |
| `peaks.anodic` / `peaks.cathodic` | patrz niżej; `null` gdy pik niewykryty |
| `derived.delta_Ep_mV` | separacja pików Epa−Epc [mV] |
| `derived.ratio_abs_Ipa_Ipc` | \|Ipa/Ipc\| (miara odwracalności) |

### peaks.anodic / peaks.cathodic

| pole | znaczenie |
|---|---|
| `Ep_V` | potencjał piku [V] |
| `Ip_nA` | natężenie piku **po odjęciu baseline** [nA] — to jest wartość „naukowa" do wyświetlania; anodowy > 0, katodowy < 0 |
| `Ip_raw_nA` | surowa wartość prądu w piku [nA] — do rysowania markera NA krzywej |
| `baseline_nA` | wartość baseline w punkcie piku [nA] — do narysowania linii bazowej |
| `index` | indeks piku w obrębie gałęzi (anodowy: w forward `[0..apex]`; katodowy: w reverse liczony OD apexu) |

Uwaga do rysowania: marker piku stawiaj w `(Ep_V, Ip_raw_nA)` (leży na krzywej);
`Ip_nA` to długość odcinka pik–baseline (jak strzałka w Origin).
Uwaga: `index` odnosi się do pełnej (niedecymowanej) gałęzi — przy `decimation` > 1
lokalizuj pik po `Ep_V`, nie po indeksie (wszystkie paczki w tym folderze mają `decimation: 1`).

## aggregate — statystyka z powtórzonych skanów

Dla `Ep_a_V`, `Ep_c_V`, `Ip_a_nA`, `Ip_c_nA`, `delta_Ep_mV`, `ratio_abs_Ipa_Ipc`:
`{ "mean": ..., "sd": ..., "n": ... }` (sd=0 przy n=1; `null` gdy brak danych).
Rozrzut skan-do-skanu rzędu 5–15% jest normalny (tyle samo ma ekspert czytający ręcznie).

## Animacja CV „na żywo"

Plik NOVA nie zawiera osi czasu. CV ma stałą szybkość skanowania, więc czas ≈ liniowy
w indeksie punktu: animuj po kolejnych indeksach `curve` ze stałym krokiem.
Kierunek: E rośnie do `apex_index` (utlenianie), potem maleje (redukcja).

## Fizyka (żeby wykresy „miały sens")

- Elektrody 3D są quasi-odwracalne: ΔEp duże (0,3–0,9 V) — to cecha materiału, nie błąd.
- Pik anodowy: garb w górnej gałęzi; katodowy: dolina w dolnej, przy niższym potencjale.
- `tylko_anodowy` zdarza się przy słabych elektrodach — rysuj krzywą bez markera katodowego.

---

## Wersja 1.1 (20.08.2026) — co doszło, nic nie ubyło

`"schema": "electrolab3d.experiment/1.1"`. Wszystkie pola z 1.0 zostają i znaczą to samo.
Paczki 1.0 leżą w `eksport_unreal_v1.0_20260720/`.

Zmiany w liczbach: linia bazowa jest teraz liczona z płaskiego odcinka tuż przed sygnałem
(tak jak Bartek rysuje ją w Originie), więc `baseline_nA` i `Ip_nA` różnią się od 1.0,
zwłaszcza dla elektrod 4 mm (tam 1.0 zaniżało Ip o ~35 %). Zgodność z ręczną tabelą Bartka:
Ip anodowe 1,1 %, katodowe 2,8 % (45 elektrod).

Nowe pola w każdym piku (`peaks.anodic` / `peaks.cathodic`):

| pole | typ | znaczenie |
|---|---|---|
| `shape` | `"clear"` / `"weak"` | czy pik ma wyraźne maksimum (`clear`), czy jest tylko ramieniem (`weak`) |
| `method` | string | jak policzono `Ip_nA` (`maksimum` albo `krzywa przy przecięciu (pik słaby)`) |
| `baseline_window_V` | `[E1, E2]` | odcinek potencjału, po którym dopasowano linię bazową; do narysowania bazowej w tym zakresie |
| `readings_nA.maximum` | nA | prąd w maksimum piku minus bazowa (klasyczny odczyt) |
| `readings_nA.curve_at_tangent_x` | nA / null | prąd krzywej przy potencjale przecięcia stycznych minus bazowa |
| `readings_nA.tangent_intersection` | nA / null | przecięcie stycznej do zbocza ze styczną za pikiem minus bazowa |
| `tangent_x_V` | V / null | potencjał przecięcia stycznych (pionowa kreska na wykresie, jak w Originie) |

`cycle_used` przyjmuje teraz wartość `"ostatni"` (ostatni cykl w pliku; pliki z labu mają
po jednym cyklu, więc to ten sam zestaw punktów co dotąd).

Do wyświetlania w Unrealu wystarczy nadal `Ep_V`, `Ip_nA`, `baseline_nA`, `index`.
Jeśli chcesz pokazać „jak zmierzono": narysuj bazową na `baseline_window_V` i przedłuż ją do
`Ep_V`, a dla `shape == "weak"` dodaj pionową kreskę w `tangent_x_V`.
