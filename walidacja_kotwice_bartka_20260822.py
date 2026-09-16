"""Walidacja na 9 elektrodach z kotwicami Bartka (pptx 22.08.2026, skan 4 = plik ba(3)).

Dla każdej elektrody i piku:
  1. odtwarzam procedurę Bartka z jego kotwic (linie przez 2 punkty, Ep = przecięcie
     stycznych -> najbliższy punkt danych, Ip = I_krzywa(Ep) - I_bazowa(Ep)),
  2. porównuję z liczbami, które sam wpisał do tabeli w pptx,
  3. porównuję z automatem (analizuj_plik z notebooka) i z tabelą xlsx.
Użycie: uv run --with matplotlib --with scipy --with pandas --with ipython --with python-pptx --with openpyxl python walidacja_kotwice_bartka_20260822.py
"""
import os, re, json, glob, warnings
import numpy as np
from pptx import Presentation
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = os.path.join(HERE, '07_dane_bartka_20260822', 'dane iterations do pythona.pptx')
DATA = os.path.join(HERE, 'SPE iterations')

def num(s):
    s = s.strip().replace(',', '.').replace('*10*-', '*10^-')
    m = re.match(r'^(-?[\d.]+)(?:\*10\^(-?\d+))?$', s)
    return float(m.group(1)) * 10 ** int(m.group(2) or 0)

FOLDER = {'4 mm WE': ('WE', '4mm', '4 mm {L}'), '13,39 mm contact': ('contact lenght', '13,39', '13,39 {L}'),
          '0,40mm': ('LEYER HEIGHT', '0,40', '0,40 {L}')}

def slajdy():
    for s in Presentation(PPTX).slides:
        tyt = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame][0].strip()
        tab = [sh for sh in s.shapes if sh.has_table][0].table
        rows = [[c.text for c in r.cells] for r in tab.rows]
        m = re.match(r'(4 mm WE|13,39 mm contact|0,40mm)\s+([ABC]) skan 4 proces (anodowy|katodowy)', tyt)
        seria, lit, proc = m.groups()
        d = {r[0].strip(): [num(x) for x in r[1:] if x.strip()] for r in rows[1:]}
        yield dict(tytul=tyt, seria=seria, lit=lit, proc=proc,
                   baz=d['Linia bazowa'], skok=d['Linia skoku krzywej'], po=d['Linia po skoku krzywej'],
                   Ep_B=d['Punkt zrzutowany na krzywą'][0], Ik_B=d['Punkt zrzutowany na krzywą'][1],
                   Ib_B=d['Punkt przecięcia linii rzutowanej z linią bazową'][1])

def linia(p):  # (E1,I1,E2,I2) -> slope, intercept
    a = (p[3] - p[1]) / (p[2] - p[0]); return a, p[1] - a * p[0]

def wczytaj(path):
    E, I = [], []
    for ln in open(path, encoding='utf-8-sig'):
        t = ln.split()
        if len(t) == 2:
            try: E.append(float(t[0])); I.append(float(t[1]))
            except ValueError: pass
    return np.array(E), np.array(I)

nb = json.load(open(os.path.join(HERE, 'PeakWise_CV_Analyzer.ipynb'))); ns = {}
exec(''.join(nb['cells'][1]['source']), ns); analizuj = ns['analizuj_plik']

wyn = []
for s in slajdy():
    sub, grp, nm = FOLDER[s['seria']]
    folder = os.path.join(DATA, sub, grp, nm.format(L=s['lit']))
    fs = sorted([f for f in glob.glob(folder + '/*') if os.path.isfile(f) and not f.endswith('.png')],
                key=lambda f: (len(os.path.basename(f)), f))
    f = fs[-1]                                   # ba(3) = skan 4
    E, I = wczytaj(f)
    imax = int(np.argmax(E))
    Ef, If = (E[:imax + 1], I[:imax + 1]) if s['proc'] == 'anodowy' else (E[imax:], I[imax:])
    a1, b1 = linia(s['skok']); a2, b2 = linia(s['po']); ab, bb = linia(s['baz'])
    Ex = (b2 - b1) / (a1 - a2)                   # przecięcie stycznych
    k = int(np.argmin(abs(Ef - Ex))); Ep = Ef[k]; Ik = If[k]; Ib = ab * Ep + bb
    Ip_B = s['Ik_B'] - s['Ib_B']; Ip_odt = Ik - Ib
    w = analizuj(open(f, 'rb').read(), os.path.basename(f))
    pk = w['pik_a'] if s['proc'] == 'anodowy' else w['pik_c']; sfx = 'a' if s['proc'] == 'anodowy' else 'c'
    auto = {k2: pk[f'Ip_{sfx}{k2}'] * 1e-9 for k2 in ('', '_max', '_krzywa_x', '_styczne')}
    E_auto = pk[f'E_{sfx}_styczne']
    r = dict(el=f"{s['seria']} {s['lit']}", proc=s['proc'][:4], plik=os.path.basename(f), Ex=Ex, Ep_B=s['Ep_B'], Ep_odt=Ep,
             Ip_B=Ip_B, Ip_odt=Ip_odt, Ik_B=s['Ik_B'], Ik_odt=Ik, Ib_B=s['Ib_B'], Ib_odt=Ib,
             E_auto=E_auto, **{'auto' + k2: v for k2, v in auto.items()}, ksztalt=pk['ksztalt'], metoda=pk['metoda'])
    wyn.append(r)

u = 1e6
print('%-20s %-4s | Ep_B    Ep_odt   E_auto  | Ip_B    Ip_odt  d%%   | auto    d%%   | krzywa@x d%%  | styczne d%%  | kształt' % ('elektroda', 'pik'))
for r in wyn:
    d = lambda x: 100 * (x - r['Ip_B']) / abs(r['Ip_B'])
    print('%-20s %-4s | %7.4f %7.4f %7.4f | %6.3f %6.3f %+5.1f | %6.3f %+5.1f | %6.3f %+5.1f | %6.3f %+5.1f | %s' % (
        r['el'], r['proc'], r['Ep_B'], r['Ep_odt'], r['E_auto'], r['Ip_B'] * u, r['Ip_odt'] * u, d(r['Ip_odt']),
        r['auto'] * u, d(r['auto']), r['auto_krzywa_x'] * u, d(r['auto_krzywa_x']), r['auto_styczne'] * u, d(r['auto_styczne']), r['ksztalt']))
for nazwa, klucz in [('odtworzenie z kotwic', 'Ip_odt'), ('auto (raportowane)', 'auto'), ('auto krzywa@x', 'auto_krzywa_x'), ('auto styczne', 'auto_styczne')]:
    for proc in ('anod', 'kato'):
        e = [abs(r[klucz] - r['Ip_B']) / abs(r['Ip_B']) * 100 for r in wyn if r['proc'] == proc]
        b = [(r[klucz] - r['Ip_B']) / abs(r['Ip_B']) * 100 for r in wyn if r['proc'] == proc]
        print('%-22s %s: śr %.2f%%  med %.2f%%  max %.2f%%  bias %+.2f%%' % (nazwa, proc, np.mean(e), np.median(e), max(e), np.mean(b)))
print('\nRozjazd kotwic: |Ep_B - Ep_odt| max %.4f V; |Ik_B-Ik_odt| max %.3f µA; |Ib_B-Ib_odt| max %.3f µA' % (
    max(abs(r['Ep_B'] - r['Ep_odt']) for r in wyn), max(abs(r['Ik_B'] - r['Ik_odt']) for r in wyn) * u, max(abs(r['Ib_B'] - r['Ib_odt']) for r in wyn) * u))
import csv
out = os.path.join(HERE, 'wyniki_analizy', 'walidacja_kotwice_bartka_20260822.csv')
with open(out, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(wyn[0].keys())); w.writeheader(); w.writerows(wyn)
print('zapisano', out)
