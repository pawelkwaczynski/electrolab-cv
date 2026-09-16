# Literatura: automatyczna analiza pików CV dla elektrod drukowanych 3D

Research pod artykuł (PeakWise, AHE Łódź + UŁ). Data: 22-23.08.2026.
Źródła: (A) lokalny RAG Pawła (tag chem: Elgrishi 2018, Harvey Analytical Chemistry 2.1, LibreTexts, Yan i Bazant 2017, artykuł LSCF), cytaty wyciągnięte z oryginalnych PDF przez pdftotext; (B) internet (4 zapytania wyszukiwania), wszystkie DOI poniżej sprawdzone drugą metodą przez API Crossref (tytuł, czasopismo, rok). Gdzie nie sprawdziłem: "DOI do sprawdzenia".

Nasz algorytm (dla kontekstu): bazowa = MNK na odcinku przed onsetem (onset szukany przed najstromszym zboczem), Ip = i(Ep) minus bazowa(Ep), dla słabych pików Ep z przecięcia dwóch stycznych. Walidacja: 1-3 % vs ręczny odczyt w Origin na 45 elektrodach; w ręcznej tabeli znaleziono błędy przepisywania rzędu 10-50 %.

---

## 1. Cytaty z RAG (dosłowne, z numerami stron)

Numer strony = strona PDF w bibliotece (w nawiasie strona drukowana, do przypisu).

### 1.1 Elgrishi N., Rountree K.J., McCarthy B.D., Rountree E.S., Eisenhart T.T., Dempsey J.L., "A Practical Beginner's Guide to Cyclic Voltammetry", J. Chem. Educ. 2018, 95, 197-206, DOI 10.1021/acs.jchemed.7b00361 (Crossref OK)

Odwracalność i ΔEp, str. 3 PDF (drukowana 199):
> "If the reduction process is chemically and electrochemically reversible, the difference between the anodic and cathodic peak potentials, called peak-to-peak separation (ΔEp), is 57 mV at 25 °C (2.22 RT/F), and the width at half max on the forward scan of the peak is 59 mV."

E1/2 jako środek między pikami, str. 3 PDF (199):
> "At points B and E, the concentrations of Fc+ and Fc at the electrode surface are equal, following the Nernst equation, E = E1/2. This corresponds to the halfway potential between the two observed peaks (C and F) and provides a straightforward way to estimate the E0' for a reversible electron transfer".

Elektrochemiczna nieodwracalność i wzrost ΔEp, str. 4 PDF (200):
> "when there is a high barrier to electron transfer (electrochemical irreversibility), electron transfer reactions are sluggish and more negative (positive) potentials are required to observe reduction (oxidation) reactions, giving rise to larger ΔEp."

Randles-Sevcik, str. 4 PDF (200):
> "the Randles-Sevcik equation (eq 3) describes how the peak current ip (A) increases linearly with the square root of the scan rate υ (V s−1), where n is the number of electrons transferred in the redox event, A (cm2) is the electrode surface area (usually treated as the geometric surface area), Do (cm2 s−1) is the diffusion coefficient of the oxidized analyte, and C0 (mol cm−3) is the bulk concentration of the analyte. ip = 0.446 nFAC0 (nFυDo/RT)^1/2 (3)"

Prąd tła (pojemnościowy) i skan tła, str. 7 PDF (203):
> "A small current is still flowing between the electrodes, but no distinct features are observed. This background current is sometimes called capacitive current, double-layer current, or non-Faradaic current. The intensity of the current varies linearly with the scan rate used (see below). The background scan is essential to test if all the components of the cells are in good condition before adding the analyte as well as to quantify the capacitive current."

Spadek omowy jako przyczyna rozjazdu ΔEp, str. 8 PDF (204):
> "A telltale sign of ohmic drop in CV is increased peak-to-peak separation in the voltammogram for a redox event that is known to be electrochemically reversible".
> "Ohmic drop can be mitigated by three methods: (1) diminish i, by reducing the size of the working electrode or restricting the experiment to slow scan rates; (2) decrease Rsol, and therefore decrease Ru, by increasing the conductivity of the solution with higher electrolyte concentrations; and (3) decrease Ru directly (and increase Rc) by diminishing the distance separating the reference and working electrodes".

Kinetyka wolna, str. 8 PDF (204):
> "peak-to-peak separation is larger than the 57 mV anticipated for an electrochemically reversible one-electron redox couple".

Uwaga: Elgrishi NIE podaje jawnej procedury rysowania linii bazowej pod Ip (tylko rysunek 3 i równanie Randlesa-Sevcika). Definicję bazowej i ekstrapolacji trzeba cytować z Harveya (niżej).

### 1.2 Harvey D.T., "Analytical Chemistry 2.1" (open access, rozdz. 11 Electrochemical Methods)

Prąd resztkowy, str. 727 PDF (drukowana 703):
> "Even in the absence of analyte, a small, measurable current flows through an electrochemical cell. This residual current has two components: a faradaic current due to the oxidation or reduction of trace impurities and a nonfaradaic charging current."

Kształt woltamogramu, pik zamiast prądu granicznego, str. 727 PDF (703):
> "In the absence of convection the diffusion layer increases with time (see Figure 11.40). As shown in Figure 11.42b, the resulting voltammogram has a peak current instead of a limiting current."
> Podpis rys. 11.42: "The three common shapes for voltammograms. The dashed red line shows the residual current."

Dwie metody korekcji tła: ekstrapolacja vs blank. To jest definicja NASZEJ bazowej. Str. 739 PDF (715):
> "There are two methods to compensate for the residual current. One method is to measure the total current at potentials where the analyte's faradaic current is zero and extrapolate it to other potentials. This is the method shown in Figure 11.42. One advantage of extrapolating is that we do not need to acquire additional data. An important disadvantage is that an extrapolation assumes that any change in the residual current with potential is predictable, which may not be the case. A second, and more rigorous approach, is to obtain a voltammogram for an appropriate blank. The blank's residual current is then subtracted from the sample's total current."

Rozkład prądu całkowitego, str. 739 PDF (715):
> "i_tot = i_A + i_r ... The residual current, in turn, has two sources. One source is a faradaic current from the oxidation or reduction of trace interferents in the sample, i_int. The other source is the charging current, i_ch, that accompanies a change in the working electrode's potential."

Odczyt Ip i Ep w CV, str. 735 PDF (711), podpis rys. 11.47:
> "(b) The resulting cyclic voltammogram showing the measurement of the peak currents and peak potentials."
> oraz str. 736 PDF (712): "The peak current in cyclic voltammetry is given by the Randles-Sevcik equation ip = (2.69 × 10^5) n^3/2 A D^1/2 ν^1/2 C_A".

Dokładność i precyzja odczytu piku, KLUCZOWY cytat pod nasze 1-3 %. Str. 750 PDF (726):
> "The accuracy of a voltammetric analysis usually is limited by our ability to correct for residual currents, particularly those due to charging. For an analyte at the parts-per-million level, an accuracy of ±1-3% is routine."
> "Precision generally is limited by the uncertainty in measuring the limiting current or the peak current. Under most conditions, a precision of ±1-3% is reasonable. One exception is the analysis of ultratrace analytes in complex matrices by stripping voltammetry, in which the precision may be as poor as ±25%."

Wniosek do artykułu: zgodność automat vs Origin 1-3 % mieści się w typowej precyzji samego pomiaru woltamperometrycznego wg Harveya, więc algorytm nie dokłada błędu ponad szum metody.

### 1.3 Pozostałe w RAG (tag chem)
- LibreTexts "Electrochemistry fundamentals" (str. 9): rozróżnienie odwracalności chemicznej i elektrochemicznej; bez procedury bazowej.
- Yan, Bazant, Biesheuvel, "Theory of linear sweep voltammetry with diffuse charge", arXiv:1608.07004 (str. 16-17): "modified Randles-Sevcik" dla elektrolitów bez nadmiaru soli; przydatne tylko jeśli będziemy tłumaczyć odchylenia od R-S.
- Artykuł LSCF (Article_Voltammetry_LSCF_vf.pdf, str. 19): spadek omowy jako główne ograniczenie interpretacji CV (zgodne z Elgrishi i Veloso 2023 niżej).

---

## 2. Narzędzia open source do analizy pików CV (tabela)

| Narzędzie | Język, licencja | Rok, autorzy | Bazowa i Ip/Ep | Walidacja vs ręczny odczyt | Stosunek do nas |
|---|---|---|---|---|---|
| SD-fitter | Python, GPL-3 | 2026, Macedo, Hogan i in. (Anal. Chem., DOI 10.1021/acs.analchem.5c07228, Crossref OK) | semi-pochodna, tło R-CPE, dekonwolucja nakładających się pików, Ip po korekcji | NIE (3 układy eksperymentalne vs konwencjonalna bazowa) | najbliższy konkurent metodologiczny, ale cel inny (nakładające się piki), brak walidacji vs człowiek |
| Diffusional Fitter | Python, GPL-3 | 2024, Macedo i in. (Anal. Chem., DOI 10.1021/acs.analchem.3c04181, OK) | dopasowanie Cottrella/Shoup-Szabo na zboczu forward, ekstrapolacja pod pik powrotny | NIE (symulacje + CV eksperymentalne, vs bazowa liniowa) | pokazuje błąd liniowej bazowej dla piku POWROTNEGO; my liczymy pik forward, warto zacytować jako ograniczenie |
| MADAP | Python, MIT | 2023-2024, Rahmanian (DOI platformy 10.1038/s41597-023-01936-3 i 10.1039/D3DD00257H, oba OK, ale to prace o platformie bateryjnej, nie o CV) | find_peaks, Ip, Ep, ΔEp, E1/2, liniowa bazowa w oknie pojemnościowym | NIE | podobna koncepcja (liniowa bazowa z okna), bez walidacji; cytować w Introduction jako "istnieją, ale nie zwalidowane" |
| PySimpleEChem / PySimpleCV | Python, GPL-3 | 2023-2026, kevinsmia1939 (GitHub, Zenodo 10.5281/zenodo.8019091 wg repo, DOI do sprawdzenia) | GUI, suwakowa bazowa, druga pochodna, ΔEp, Nicholson | NIE | półautomat, operator wybiera zakres, czyli dokładnie to, co my eliminujemy |
| eChem (R) | R, GPL-2 | 2018, Harvey (CRAN, DOI 10.32614/CRAN.package.eChem, OK) | annotateCV(): Epc, Epa, ΔEp, Ip z bazowej z początkowych % punktów skanu | NIE (symulacje) | od autora naszego podręcznika; działa na symulowanych CV, nie na plikach z potencjostatu |
| KickStat firmware | C++/Arduino, licencja niejasna | 2020, Hoilett, Linnes i in. (Sensors, DOI 10.3390/s20082407, OK) | MNK prosta w oknie bazowym, ekstrapolacja w okno piku, max różnicy = Ip, Ep | NIE (vs Bio-Logic VSP-300: piki w granicach 9 %) | algorytm prawie identyczny z naszym, ale okna zdefiniowane z góry, nie z onsetu; 9 % vs nasze 1-3 % |
| PalmSens SDK / PyPalmSens | Python/.NET, licencja sprzętowa | 2025-2026, PalmSens BV (DOI do sprawdzenia) | średnia ruchoma jako bazowa, pochodne, PeakX | nie publikowana | komercyjne, przywiązane do sprzętu |
| Envismetrics | Python/Flask, MIT | 2026, Xue i in. (JOSS w recenzji, DOI do sprawdzenia) | max/min w zakresie użytkownika, Randles-Sevcik, Nicholson | NIE | brak ekstrapolacji bazowej |
| pybaselines | Python, BSD-3 | 2021, Erb (Zenodo 10.5281/zenodo.5608581, DOI do sprawdzenia) | >50 algorytmów bazowej (AsLS, airPLS, SNIP), bez pików | NIE | biblioteka ogólna; można użyć jako porównanie "ślepej" bazowej vs naszej fizycznej |
| SACMES | Python, open source | 2019, Curtis, Arroyo-Currás i in. (Anal. Chem., DOI 10.1021/acs.analchem.9b02553, OK) | wielomianowa bazowa, Ip i pole dla SWV/CV w czasie rzeczywistym | NIE (2x lepszy S/N po zawężeniu okna) | aptamerowe biosensory, inny cel |
| SeroWare, The Analysis Kid | MATLAB / JS | 2025, 2021 (DOI 10.1021/acschemneuro.4c00799 i 10.1021/acsmeasuresciau.1c00003, oba OK) | FSCV, odejmowanie tła | NIE | szybka CV neurochemiczna, nie nasz przypadek |
| ElectroML | web, open source | 2026, Akarsu i in. (SoftwareX, DOI 10.1016/j.softx.2026.102640, OK) | filtracja, bazowa, 47 cech (w tym wysokość i potencjał piku), AutoML | NIE (R2 0,87 na 9 próbkach) | ML na cechach pików, bez kontroli jakości bazowej |

Sprawdzone i odrzucone (parsery lub inne cele): galvani, eclabfiles, ixdat, ec-tools, gamry-parser, hardpotato, Polarographica, Voltammogrammer, pyEIS.

Wniosek z tabeli: ŻADNE z 12 narzędzi nie raportuje zgodności z niezależnym ręcznym odczytem na zbiorze elektrod, ani nie stosuje bazowej wyznaczanej z onsetu piku. Najbliżej nas jest KickStat (MNK w oknie, 9 % vs instrument referencyjny).

---

## 3. Publikacje

### 3.1 Automatyczna / algorytmiczna analiza woltamogramów (2019-2026)

1. Ha L.D., Hwang S., 2025, Analytical Chemistry, DOI 10.1021/acs.analchem.4c04448 (OK). Sieć neuronowa rozdziela prąd faradajowski od niefaradajowskiego w CV i wyciąga Ip i Ep; dane eksperymentalne: MAPE Ip 3,37 %, błąd Ep < 0,75 mV. Relacja: najbliższy konkurent liczbowy (3,4 % vs nasze 1-3 %), ale czarna skrzynka vs nasza procedura fizyczna; cytować w Introduction i Discussion.
2. Macedo D.S., Rodopoulos T., Vepsäläinen M., Bajaj S., Hogan C.F., 2024, Analytical Chemistry, DOI 10.1021/acs.analchem.3c04181 (OK). Bazowa dyfuzyjna (Cottrell) pod pikiem powrotnym zamiast liniowej. Relacja: argument, że liniowa bazowa jest ok dla piku forward, a nie dla powrotnego; cytować jako ograniczenie zakresu.
3. Macedo D.S. i in., 2026, Analytical Chemistry, DOI 10.1021/acs.analchem.5c07228 (OK). SD-fitter, dekonwolucja nakładających się pików. Relacja: konkurencja w kategorii "open-source CV tool", bez walidacji vs człowiek.
4. Tichter T., Roth C., 2026, ACS Electrochemistry, "Acquisition and Processing of Voltammetric Data: Dos and Don'ts", DOI 10.1021/acselectrochem.5c00370 (OK). Tutorial: błędy Ip 1-10 % z nieskompensowanej rezystancji; odejmowanie tła może przeszacować wysokość i przesunąć pik, bo sygnał i tło są splecione, nie addytywne. Relacja: cytować przy uzasadnieniu bazowej z odcinka PRZED onsetem (nie odejmujemy blanku).
5. Van Echelpoel R., de Jong M., Daems D., Van Espen P., De Wael K., 2021, Talanta, DOI 10.1016/j.talanta.2021.122605 (OK). Rozpoznawanie pików CV/LSV/SWV z bazą ekspercką; wprost nazywa zależność od interpretacji eksperta barierą. Relacja: cytat pod motywację (operator-dependence), bez liczb dokładności.
6. Górski Ł., Ciepiela F., Jakubowska M., 2014, Electrochimica Acta, "Automatic baseline correction in voltammetry", DOI 10.1016/j.electacta.2014.05.076 (OK). Automatyczna bazowa (AGH Kraków); odzysk Pb(II) 101,8-106,6 %, r ≥ 0,998; autorzy piszą, że bazowe z prądu resztkowego mają zwykle niską powtarzalność. Relacja: polska szkoła, cytować obowiązkowo; inna technika (stripping, DPV), nie CV na elektrodach 3D.
7. Górski Ł., Ciepiela F., Jakubowska M., Kubiak W.W., 2011, Electroanalysis, DOI 10.1002/elan.201100285 (OK). Bazowa przez DWT i splajny w metodzie dodatku wzorca. Relacja: jak wyżej, Introduction.
8. Du L., Thoma Y., Rodino F., Carrara S., 2024, Electrochimica Acta, DOI 10.1016/j.electacta.2024.144304 (OK). k-means + wielomianowa bazowa + mieszanina Gaussów do detekcji pików CV; MAPE stężenia 0,32 % (etopozyd) i 4,78 % (metotreksat). Relacja: konkurencja w "automatyczne piki CV", ale dokładność liczona na stężeniu, nie na Ip.
9. Sun S. i in., 2020 (online), Journal of Chemometrics, DOI 10.1002/cem.3314 (OK; Crossref podaje 2020, inne źródło 2021). Regresja symboliczna wzorów na Ip z symulowanych CV. Relacja: ważne dla wątku SR (AI_genius), dane wyłącznie syntetyczne.
10. Hoar B.B. i in., 2022, ACS Measurement Science Au, DOI 10.1021/acsmeasuresciau.2c00045 (OK) oraz Hoar i in., 2024, ACS Electrochemistry, DOI 10.1021/acselectrochem.4c00014 (OK). Deep learning do klasyfikacji mechanizmów z CV (98,5 % na symulacjach; EchemNet >96 % detekcji zdarzeń redoks). Relacja: inny cel (mechanizm, nie Ip), cytować jako trend.
11. Fenton A.M., Brushett F.R., 2022, J. Electroanal. Chem., DOI 10.1016/j.jelechem.2021.115751 (OK). Model fizyczny + test Bayesa, 27/27 zbiorów poprawnie, błąd stężenia 10-12 %. Relacja: tło, inny cel.
12. Curtis S.D. i in., 2019, Analytical Chemistry, DOI 10.1021/acs.analchem.9b02553 (OK). SACMES, patrz tabela.
13. Mena S. i in., 2022, ACS Measurement Science Au, DOI 10.1021/acsmeasuresciau.1c00060 (OK). Automatyczne granice całkowania + ANN dla FSCV; analiza < 1 s vs > 2 h ręcznie. Relacja: argument czasowy za automatyzacją.
14. Nederhoff R.J. i in., 2026, Talanta, DOI 10.1016/j.talanta.2026.129401 (OK). Bazowa + identyfikacja pików SWV z kompensacją pH. Relacja: tło.
15. Akarsu C.H. i in., 2026, SoftwareX, DOI 10.1016/j.softx.2026.102640 (OK). ElectroML, patrz tabela.
16. Adams A.C. i in., 2022, ChemPlusChem, DOI 10.1002/cplu.202100418 (OK; Crossref: 2021 online). ML na SWV do stałych szybkości, błąd 0,38 %. Relacja: tło.

### 3.2 Błędy ręcznego odczytu pików, zmienność operatora, błędy przepisywania

17. Pižeta I., Omanović D., Branica M., 1999, Analytica Chimica Acta, "The influence of data treatment on the interpretation of experimental results in voltammetry", DOI 10.1016/S0003-2670(99)00491-2 (OK). Typ bazowej zmienia wynik dodatku wzorca i nawet liczbę wykrytych kompleksów (3 vs 4). Relacja: fundament pod tezę, że wybór bazowej to decyzja naukowa, nie kosmetyka.
18. Omanović D. i in., 2010, Analytica Chimica Acta, DOI 10.1016/j.aca.2010.02.008 (OK). Na symulowanych woltamogramach bazowa "tangent fit" generuje sztuczny ligand; autorzy odradzają. Relacja: UWAGA, to uderza w styczne; musimy pokazać, że nasza styczna z odcinka przed onsetem jest inna niż "tangent fit" krytykowany tam (u nich ASV, inny kształt tła).
19. Jirasek A., Schulze G., Yu M.M.L., Blades M.W., Turner R.F.B., 2004, Applied Spectroscopy, "Accuracy and Precision of Manual Baseline Determination", DOI 10.1366/0003702042641236 (OK). 16 osób ręcznie korygowało 100 syntetycznych widm: dokładność spada przy niskim SNR i pochyłej bazowej; początkujący przeszacowują, doświadczeni niedoszacowują. Relacja: jedyne znalezione KONTROLOWANE badanie inter-operator dla bazowej (spektroskopia, nie CV); cytować jako analogię.
20. Pavitt A.S., Tratnyek P.G., 2019, Environ. Sci.: Processes & Impacts, DOI 10.1039/C9EM00313D (OK). Nierówne bazowe czyniły wiele wartości Ip dwuznacznymi; automatyczna średnia ruchoma usuwała realne cechy. Relacja: przykład, że "ślepa" bazowa (pybaselines-like) szkodzi; nasza bazowa jest fizyczna (odcinek przed onsetem).
21. van Veen E., Comber S., Gardner M., 2001/2002, J. Environ. Monit., DOI 10.1039/B108103A (OK). Porównanie międzylaboratoryjne ASV: wyniki w granicach 50 %, stałe trwałości rozrzut 10^7-10^12. Relacja: skala rozrzutu między ludźmi i labami.
22. Jain R., Sharma R., 2012, J. Pharm. Anal., DOI 10.1016/j.jpha.2012.03.005 (OK); Ghoneim M.M. i in., 2015, RSC Advances, DOI 10.1039/C5RA05086C (OK). RSD 1,2-2,6 % między analitykami i dniami dla Ip. Relacja: liczby odniesienia dla naszego 1-3 %.
23. Ellison S.L.R., Hardcastle W.A., 2012, Accred. Qual. Assur., DOI 10.1007/s00769-012-0894-2 (OK). Ankieta uczestników badań biegłości: 44 % zgłasza błąd ludzki, ok. 5 % przyczyn to błędy przepisywania. Relacja: pod nasze odkrycie błędów 10-50 % w ręcznej tabeli.
24. Kuselman I., Pennecchi F., 2016, Pure Appl. Chem., IUPAC/CITAC Guide o błędach ludzkich w laboratorium, DOI 10.1515/pac-2015-1101 (OK). Przepisywanie, obliczenia i decyzje operatora jako ryzyko poza budżetem niepewności; brak bazy empirycznej częstości. Relacja: ramy klasyfikacji naszych błędów przepisywania.
25. Mays J.A., Mathias P.C., 2019, JAMIA, DOI 10.1093/jamia/ocy170 (OK). 3,7 % ręcznych wpisów niezgodnych z interfejsem, część > 20 %. Relacja: analogia kliniczna; używać ostrożnie, inna dziedzina.
26. Bornhorst J. i in., 2024 (online 2023), Clinical Chemistry, DOI 10.1093/clinchem/hvad195 (OK). Drugi przegląd ręczny łapie 95,7 % błędów, AI znajduje kolejne. Relacja: argument za automatem jako drugą kontrolą.

Luka w literaturze (potwierdzona w dodatkowym przeglądzie): NIE znaleziono kontrolowanego badania, w którym kilku analityków niezależnie rysuje bazowe na tych samych woltamogramach CV i raportuje ICC lub RSD.

### 3.3 Elektrody drukowane 3D (FDM) z CV FcMeOH / ferricyjanku i porównaniem geometrii

Grupa Półtoraka (UŁ), nasze własne tło:
27. Kwaczyński K., Szymaniec O., Bobrowska D.M., Poltorak Ł., 2023, Scientific Reports, DOI 10.1038/s41598-023-49599-9 (OK). Aktywacja rozpuszczalnikowa (aceton, DCM, DCE, ACN, THF, 20-1800 s) trzech filamentów, FcMeOH; ΔEp do ok. 100 mV. Relacja: baza metodyczna PeakWise, cytować jako punkt wyjścia.
28. Kwaczyński K. i in., 2025, Analyst, DOI 10.1039/D5AN00195A (OK). THF-aktywowana Protopasta, kwas salicylowy. Relacja: jw.
29. Kowalski G., Kwaczyński K., Poltorak Ł., 2026 (online 2025), Talanta, DOI 10.1016/j.talanta.2025.128467 (OK). W pełni drukowana platforma, FcMeOH, aktywacja DCM + elektrochemiczna. Relacja: jw.

Geometria i parametry druku (konkurencja dla wątku "optymalizacja geometrii"):
30. Rojas D., Torricelli D., Cuartero M., Crespo G.A., 2024, Analytical Chemistry, DOI 10.1021/acs.analchem.4c02098 (OK). FcMeOH; wysokość warstwy 50-300 µm i średnice WE 3, 4, 6, 8 mm; 200 µm najlepszy kompromis, Ip liniowe z polem geometrycznym. Relacja: RYZYKO, najbliższe naszemu porównaniu średnica x warstwa, choć cel potencjometryczny; "automatyzacja" dotyczy druku, nie analizy pików.
31. Crapnell R.D., Whittingham M.J., Banks C.E. i in., 2022, Sensors, "Adjusting the Connection Length", DOI 10.3390/s22239521 (OK). Długość połączenia 10-100 mm do dysku 3,1 mm; ΔEp rośnie z ok. 118 do 291 mV. Relacja: RYZYKO dla wątku "długość kontaktu", ale RuHex, nie FcMeOH.
32. Garcia-Miranda Ferrari A., Banks C.E. i in., 2022, Analyst, DOI 10.1039/D2AN01412B (OK). Kształty WE 2-10 mm; prąd rośnie z polem, odwracalność nie skaluje się idealnie. RuHex. Relacja: cytować przy średnicy WE.
33. Abdalla A., Patel B.A. i in., 2020, Electrochimica Acta, DOI 10.1016/j.electacta.2020.136618 (OK). Wysokość warstwy 0,1-0,4 mm i orientacja; cienkie, pionowe lepsze. RuHex. Relacja: RYZYKO dla wątku "wysokość warstwy".
34. Rocha R.G., Richter E.M. i in., 2022, J. Electroanal. Chem., DOI 10.1016/j.jelechem.2022.116910 (OK). Orientacja, warstwy 0,05-0,30 mm, perymetry, prędkość; 0,05 mm i pion najlepsze. RuHex. Relacja: jw.
35. Shergill R.S., Miller C.L., Patel B.A., 2023, Scientific Reports, DOI 10.1038/s41598-023-27656-7 (OK). Dysza 0,30-0,60 mm i temperatura stołu nie zmieniają Ipa ani ΔEp przy stałej warstwie. Ferricyjanek. Relacja: Introduction.
36. Shergill R.S., Patel B.A., 2022, ChemElectroChem, DOI 10.1002/celc.202200831 (OK). Prędkość druku 20-100 mm/s; ok. 60 mm/s optimum. Relacja: Introduction.
37. Bernalte E., Crapnell R.D., Banks C.E. i in., 2024, ChemElectroChem, DOI 10.1002/celc.202300576 (OK). Wzór wypełnienia zmienia Ip i ΔEp. Relacja: Introduction.
38. Shergill R.S. i in., 2023 (online), ACS Sustainable Chem. Eng., DOI 10.1021/acssuschemeng.3c06200 (OK). Wypełnienie 30-100 % bez istotnej zmiany Ip i ΔEp, FcMeOH i ferricyjanek. Relacja: Introduction.
39. Miller C., Keattch O., Shergill R.S., Patel B.A., 2024, Analyst, DOI 10.1039/D3AN01592K (OK). Wzory powierzchni WE, FcMeOH. Relacja: Introduction.
40. Rodrigues J.G.A. i in., 2025, ACS Omega, DOI 10.1021/acsomega.4c08593 (OK). Plan 2^3: wysokość elektrody, średnica, prędkość; istotna tylko wysokość (długość przewodnika 20 mm, dysk 6 mm). Ferricyjanek. Relacja: RYZYKO, DOE na średnicy i długości, ale bez FcMeOH i bez automatycznej analizy pików.
41. Ahmed S., Patel B., O'Neil G. i in., 2025, ACS Electrochemistry, DOI 10.1021/acselectrochem.5c00240 (OK). Porównanie filamentów, FcMeOH/FeCN/RuHex; elektrody 0,4-0,6 mm i ścieżki < 1 cm ograniczają ΔEp z iR. Relacja: RYZYKO, cytować przy długości kontaktu.
42. Veloso W.B., Paixão T.R.L.C., Meloni G.N., 2023, Electrochimica Acta, DOI 10.1016/j.electacta.2023.142166 (OK). Symulacje: pozorne ΔEp zdominowane przez rezystancję kontaktu i dyfuzję w zagłębieniu, nie przez kinetykę. Relacja: cytować, żeby nie nadinterpretować ΔEp jako k0.
43. Shergill R. i in., 2025, Green Analytical Chemistry, DOI 10.1016/j.greeac.2025.100307 (OK). Wypełnienie 0/30/100 %, konstrukcje kontaktu, aktywacja plateau ok. 600 s, FcMeOH. Relacja: Introduction.
44. Wisby R. i in., 2026, Int. J. Electrochem., DOI 10.1155/ijel/1316405 (OK); da Trindade S.O.D. i in., 2026, Analytica, DOI 10.3390/analytica7010004 (OK); Domingo-Roca R. i in., 2022, Analyst, DOI 10.1039/D2AN00862A (OK). Wzór i orientacja wypełnienia, temperatura i szerokość warstwy, orientacja i grubość. Relacja: Introduction.
45. Prace fundamentalne i aktywacja: Manzanares Palenzuela i Pumera 2018 (DOI 10.1021/acs.analchem.8b00083, OK); Richter, Muñoz, Banks 2019 (DOI 10.1021/acs.analchem.9b02573, OK); Browne i Pumera 2018 (10.1021/acsami.8b14701, OK); Rocha 2020 (10.1016/j.electacta.2020.135688, OK); Redondo 2021 (10.1016/j.carbon.2021.01.107, OK); Koterwa, Ryl 2022 (10.1016/j.apsusc.2021.151587, OK); Kozłowska, Niedziałkowski 2024 (10.3390/ma17122833, OK); Carvalho 2024 (10.1016/j.electacta.2024.144995, OK); Kováč 2025 (10.1021/acsomega.5c05879, OK). Relacja: Introduction, jeden akapit o aktywacji.

We wszystkich 33 sprawdzonych pracach o elektrodach 3D sposób odczytu Ip i ΔEp jest nieopisany (NR): ani ręczny, ani automatyczny, bez podania procedury bazowej.

---

## 4. Luka: co nasz artykuł wnosi

1. Walidacja automatu vs niezależny ręczny odczyt (Origin) na 45 elektrodach, z liczbą (1-3 %). Żadne z 12 narzędzi open source i żadna z 16 publikacji algorytmicznych nie raportuje takiej zgodności; najbliżej: KickStat (9 % vs instrument), Ha i Hwang 2025 (MAPE 3,37 % vs sieć neuronowa, nie vs człowiek).
2. Bazowa wyznaczana FIZYCZNIE z odcinka przed onsetem (onset z najstromszego zbocza), nie z okna zadanego z góry (KickStat, MADAP) i nie "ślepa" (pybaselines, średnia ruchoma krytykowana przez Pavitt 2019). To odpowiada dosłownie metodzie ekstrapolacji z Harveya (str. 739 PDF).
3. Reguła dwóch procedur (pik wyraźny vs dwie styczne dla słabego) zakodowana jako bramka; literatura (Omanović 2010) ostrzega przed "tangent fit", więc mamy gotowy punkt do Discussion: kiedy styczne są bezpieczne.
4. Wykrycie błędów przepisywania 10-50 % w ręcznej tabeli laboratoryjnej jako empiryczny dowód, że automat działa jak druga kontrola (analogia: Bornhorst 2024, Ellison 2012, IUPAC/CITAC 2016). W elektrochemii nikt tego nie opisał liczbowo.
5. Zastosowanie do porównania geometrii elektrod 3D (średnica WE, wysokość warstwy, długość kontaktu) z FcMeOH: 33 prace o elektrodach 3D nie opisują sposobu odczytu pików. Nasza praca jest pierwszą, w której optymalizacja geometrii opiera się na odczycie powtarzalnym i audytowalnym.
6. Brak w literaturze kontrolowanego badania inter-operator dla bazowej w CV (jedyne: Jirasek 2004 dla widm). Opcja na wzmocnienie: poprosić 2-3 osoby z UŁ o niezależny ręczny odczyt tych samych 45 plików i policzyć ICC; to domknęłoby lukę jednym akapitem.

## 5. Ryzyka: kto już to zrobił lub zrobi

- Rojas, Cuartero, Crespo 2024 (Anal. Chem.): średnica WE 3-8 mm x warstwa 50-300 µm z FcMeOH. Najbliższe naszej macierzy geometrii; trzeba jasno odróżnić (inny filament, inny cel, brak analizy pików, u nas dodatkowo długość kontaktu i automat).
- Crapnell/Banks 2022 (Sensors): długość połączenia 10-100 mm. Ahmed/O'Neil 2025: ścieżki < 1 cm. Rodrigues 2025: DOE średnica x wysokość. Nasz wkład w geometrii musi być skwantyfikowany inaczej (np. model regresyjny Ip i ΔEp od trzech czynników) albo zostanie uznany za powtórzenie.
- Macedo i Hogan 2024/2026 (Anal. Chem.): pokazali, że liniowa bazowa zaniża lub zawyża pik POWROTNY; recenzent spyta, czy nasz algorytm liczy pik powrotny i jak. Odpowiedź: walidujemy forward, powrotny zgłaszamy jako ograniczenie lub dokładamy bazową dyfuzyjną.
- Ha i Hwang 2025: MAPE 3,37 % z AI; nasze 1-3 % trzeba raportować z tym samym typem metryki (MAPE, nie tylko zakres) i z liczbą pików.
- Omanović 2010 odradza bazową styczną w ASV; nasze dwie styczne dla słabych pików wymagają jawnego warunku użycia i pokazania błędu (7-19 % rozbieżności między procedurami wg notatek lab).
- Górski i Jakubowska (AGH) 2011-2014: polska grupa z "automatic baseline correction in voltammetry"; pominięcie ich w cytowaniach byłoby błędem recenzyjnym.
- Veloso 2023 i Tichter i Roth 2026: ΔEp na elektrodach 3D jest zdominowane przez iR, więc wnioski o "odwracalności" z ΔEp trzeba formułować ostrożnie (porównawczo, nie jako k0).

## 6. Do zrobienia przed pisaniem
- Crossref potwierdził 64 DOI. Niepotwierdzone zostały tylko: Zenodo PySimpleCV (10.5281/zenodo.8019091), Zenodo pybaselines (10.5281/zenodo.5608581), PalmSens SDK i Envismetrics (brak DOI czasopisma).
- Pobrać pełne teksty: Ha i Hwang 2025, Macedo 2024, Górski 2014, Rojas 2024, Tichter i Roth 2026, Pižeta 1999 (do RAG, tag chem).
- Ustalić z Bartkiem, czy ręczny odczyt w Origin był jednej osoby (wtedy 1-3 % to zgodność, nie inter-operator) i czy da się dołożyć drugiego czytającego.
