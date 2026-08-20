"""Walidacja analizatora HURNY vs ręczna tabela Bartka (45 elektrod × 4 skany = 184 pliki).

Użycie:
    uv run --with matplotlib --with scipy --with pandas --with ipython --with openpyxl \
        python walidacja_vs_tabela_bartka.py [SETUP.py] [--skan ostatni|pierwszy|srednia]

SETUP.py = plik z kodem komórki SETUP notebooka (domyślnie wyciągany z HURNY_CV_Analyzer.ipynb).
Tabela: dane_wyniki/FDM SPE EXPERIMENTS (1).xlsx — 1 wiersz = 1 elektroda (skan 4 wg Bartka).
Skan: 'ostatni' = plik ba(3), 'pierwszy' = plik ba, 'srednia' = średnia z 4 plików.
"""
import sys, os, glob, json, warnings, argparse
import numpy as np, openpyxl
warnings.filterwarnings('ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data', 'SPE iterations')
TABELA = os.path.join(HERE, 'data', 'FDM SPE EXPERIMENTS.xlsx')

ap = argparse.ArgumentParser()
ap.add_argument('setup', nargs='?', default=None)
ap.add_argument('--skan', default='ostatni', choices=['ostatni', 'pierwszy', 'srednia'])
ap.add_argument('--csv', default=None, help='zapisz wyniki per elektroda')
args = ap.parse_args()

if args.setup:
    kod = open(args.setup).read()
else:
    nb = json.load(open(os.path.join(HERE, 'ElectroLab_CV_Analyzer.ipynb')))
    kod = ''.join(nb['cells'][1]['source'])
ns = {}
exec(kod, ns)
analizuj_plik = ns['analizuj_plik']


def folder_dla(arkusz, row):
    """Wiersz tabeli → folder elektrody. Zwraca None dla wierszy bez danych."""
    D, H, L, lit = row['D'], row['H'], row['L'], row['lit']
    if arkusz == 'Diameter (2)':
        sub = {1: '1mm', 2: '2mm', 3: '3mm (original version)', 4: '4mm'}[int(D)]
        nazwa = f'{int(D)} mm {lit}'
        if int(D) == 2: nazwa = nazwa.lower()
        if lit == 'E': nazwa = '3 mm E (insted of B)'
        return os.path.join(DATA, 'WE', sub, nazwa)
    if arkusz == 'Height (2)':
        if abs(H - 0.08) < 1e-6: return None          # duplikat 3 mm
        h = f'{H:.2f}'.replace('.', ',')
        return os.path.join(DATA, 'LEYER HEIGHT', h, f'{h} {lit}')
    if arkusz == 'Lenght (2)':
        if abs(L - 14.39) < 1e-6: return None         # duplikat 3 mm
        l = f'{L:.2f}'.replace('.', ',')
        return os.path.join(DATA, 'contact lenght', l, f'{l} {lit}')
    return None


def pliki_elektrody(folder):
    fs = [f for f in glob.glob(os.path.join(folder, '*')) if os.path.isfile(f) and not f.endswith('.png')]
    # kolejność skanów: 'ba', 'ba(1)', 'ba(2)', 'ba(3)' (albo 'ba (0)'..'ba (3)')
    return sorted(fs, key=lambda f: (len(os.path.basename(f)), f))


def fnum(v):
    try: return float(v)
    except (TypeError, ValueError): return None


wb = openpyxl.load_workbook(TABELA, data_only=True)
wiersze = []
for ws in wb.worksheets:
    if ws.title not in ('Diameter (2)', 'Height (2)', 'Lenght (2)'): continue
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None or not isinstance(r[0], (int, float)): continue
        lit = (str(r[10]).strip() if r[10] else None)
        if not lit or lit not in ('A','B','C','E') or fnum(r[4]) is None: continue
        row = dict(arkusz=ws.title, L=fnum(r[2]), H=fnum(r[3]), D=fnum(r[4]),
                   IOX=fnum(r[6]), IRED=fnum(r[7]), dEp=fnum(r[8]), lit=lit)
        if row['IOX'] is None and row['IRED'] is None: continue
        folder = folder_dla(ws.title, row)
        if folder is None: continue
        if not os.path.isdir(folder):
            print('BRAK FOLDERU', folder); continue
        row['folder'] = folder
        wiersze.append(row)

print(f'Elektrod w tabeli z danymi: {len(wiersze)}  | skan: {args.skan}')
out = []
n_plikow = 0; crashe = 0
for row in wiersze:
    fs = pliki_elektrody(row['folder'])
    if args.skan == 'ostatni': fs = fs[-1:]
    elif args.skan == 'pierwszy': fs = fs[:1]
    wy = []
    for f in fs:
        n_plikow += 1
        try:
            wy.append(analizuj_plik(open(f, 'rb').read(), os.path.basename(f)))
        except Exception as e:
            crashe += 1; print('CRASH', f, e)
    def sr(klucz_pik, pole):
        v = [w[klucz_pik][pole] for w in wy if w.get(klucz_pik) and w[klucz_pik].get(pole) is not None]
        return float(np.mean(v)) * 1e-9 if v else None
    def sr_top(pole):
        v = [w[pole] for w in wy if w.get(pole) is not None]
        return float(np.mean(v)) if v else None
    rec = dict(row)
    rec.update(
        Ipa=sr('pik_a', 'Ip_a'), Ipa_max=sr('pik_a', 'Ip_a_max'), Ipa_krzywa_x=sr('pik_a', 'Ip_a_krzywa_x'), Ipa_styczne=sr('pik_a', 'Ip_a_styczne'),
        Ipc=sr('pik_c', 'Ip_c'), Ipc_max=sr('pik_c', 'Ip_c_max'), Ipc_krzywa_x=sr('pik_c', 'Ip_c_krzywa_x'), Ipc_styczne=sr('pik_c', 'Ip_c_styczne'),
        dEp_auto=sr_top('delta_Ep'), n=len(wy),
        ksztalt_a='/'.join(w['pik_a']['ksztalt'] for w in wy if w.get('pik_a') and 'ksztalt' in w['pik_a']),
        ksztalt_c='/'.join(w['pik_c']['ksztalt'] for w in wy if w.get('pik_c') and 'ksztalt' in w['pik_c']),
    )
    out.append(rec)


def blad(pole_auto, pole_ref):
    e = []
    for r in out:
        a, b = r.get(pole_auto), r.get(pole_ref)
        if a is None or b is None or b == 0: continue
        e.append(abs(a - b) / abs(b))
    return (100 * np.mean(e), 100 * np.median(e), len(e)) if e else (None, None, 0)


print(f'Plików: {n_plikow}, crashe: {crashe}')
print('%-22s %8s %8s %4s' % ('wariant', 'śr.błąd', 'mediana', 'n'))
for lab, a, b in [('Ip_a (raportowane)', 'Ipa', 'IOX'), ('Ip_a maksimum', 'Ipa_max', 'IOX'),
                  ('Ip_a krzywa@x', 'Ipa_krzywa_x', 'IOX'), ('Ip_a styczne', 'Ipa_styczne', 'IOX'),
                  ('Ip_c (raportowane)', 'Ipc', 'IRED'), ('Ip_c maksimum', 'Ipc_max', 'IRED'),
                  ('Ip_c krzywa@x', 'Ipc_krzywa_x', 'IRED'), ('Ip_c styczne', 'Ipc_styczne', 'IRED'),
                  ('ΔEp', 'dEp_auto', 'dEp')]:
    m, md, n = blad(a, b)
    print('%-22s %7.1f%% %7.1f%% %4d' % (lab, m, md, n) if m is not None else '%-22s brak' % lab)

# bias (znak): czy zaniżamy czy zawyżamy
for lab, a, b in [('Ip_a', 'Ipa', 'IOX'), ('Ip_c', 'Ipc', 'IRED')]:
    d = [(r[a] - r[b]) / abs(r[b]) for r in out if r.get(a) is not None and r.get(b)]
    print('bias %s: %+.1f%% (auto − Bartek)/|Bartek|' % (lab, 100 * np.mean(d)))

# per seria
print('\nPer arkusz (Ip_a / Ip_c średni błąd):')
for ark in ('Diameter (2)', 'Height (2)', 'Lenght (2)'):
    sub = [r for r in out if r['arkusz'] == ark]
    ea = [abs(r['Ipa'] - r['IOX']) / abs(r['IOX']) for r in sub if r.get('Ipa') and r.get('IOX')]
    ec = [abs(r['Ipc'] - r['IRED']) / abs(r['IRED']) for r in sub if r.get('Ipc') and r.get('IRED')]
    print('  %-14s %5.1f%% (n=%d) / %5.1f%% (n=%d)' % (ark, 100 * np.mean(ea), len(ea), 100 * np.mean(ec) if ec else float('nan'), len(ec)))

print('\nNajgorsze elektrody (|błąd| Ip_a lub Ip_c > 15 %):')
for r in out:
    ea = abs(r['Ipa']-r['IOX'])/abs(r['IOX']) if r.get('Ipa') and r.get('IOX') else 0
    ec = abs(r['Ipc']-r['IRED'])/abs(r['IRED']) if r.get('Ipc') and r.get('IRED') else 0
    if max(ea, ec) > 0.15:
        print('  %-32s Ip_a %6.2f vs %6.2f µA (%+5.0f%%)  Ip_c %6.2f vs %6.2f µA (%+5.0f%%)  %s %s' % (
            os.path.basename(r['folder']), (r['Ipa'] or 0)*1e6, (r['IOX'] or 0)*1e6, 100*((r['Ipa'] or 0)-(r['IOX'] or 0))/abs(r['IOX'] or 1),
            (r['Ipc'] or 0)*1e6, (r['IRED'] or 0)*1e6, 100*((r['Ipc'] or 0)-(r['IRED'] or 1))/abs(r['IRED'] or 1), r['ksztalt_a'], r['ksztalt_c']))

if args.csv:
    import csv
    with open(args.csv, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=[k for k in out[0].keys() if k != 'folder'] + ['folder'])
        w.writeheader(); w.writerows(out)
    print('zapisano', args.csv)
