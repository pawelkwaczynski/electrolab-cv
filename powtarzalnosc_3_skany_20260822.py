"""Powtarzalność Ip automatu na skanach 2-4 (ba(1), ba(2), ba(3)) per elektroda; skan 1 osobno jako kondycjonowanie.
Bartek do statystyki bierze 3 ostatnie skany. Wyjście: wyniki_analizy/powtarzalnosc_3_skany_20260822.csv + md."""
import os, glob, json, warnings, csv
import numpy as np
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, 'SPE iterations')
nb = json.load(open(os.path.join(HERE, 'PeakWise_CV_Analyzer.ipynb'))); ns = {}
exec(''.join(nb['cells'][1]['source']), ns); analizuj = ns['analizuj_plik']
rows = []
for folder in sorted(glob.glob(os.path.join(DATA, '*', '*', '*'))):
    if not os.path.isdir(folder): continue
    fs = sorted([f for f in glob.glob(folder + '/*') if os.path.isfile(f) and not f.endswith('.png')], key=lambda f: (len(os.path.basename(f)), f))
    if len(fs) < 2: continue
    w = []
    for f in fs:
        try: w.append(analizuj(open(f, 'rb').read(), os.path.basename(f)))
        except Exception as e: w.append(None)
    def seria(k, pole):
        return [x[k][pole] * 1e-3 if x and x.get(k) and x[k].get(pole) is not None else np.nan for x in w]  # µA
    ipa, ipc = seria('pik_a', 'Ip_a'), seria('pik_c', 'Ip_c'); dep = [x['delta_Ep'] if x and x.get('delta_Ep') is not None else np.nan for x in w]
    def st(v):
        v = np.array(v[1:], float); v = v[~np.isnan(v)]
        return (np.mean(v), np.std(v, ddof=1) if len(v) > 1 else np.nan, 100 * np.std(v, ddof=1) / abs(np.mean(v)) if len(v) > 1 else np.nan, len(v))
    ma, sa, ca, na = st(ipa); mc, sc, cc, nc = st(ipc)
    rel = os.path.relpath(folder, DATA)
    rows.append(dict(elektroda=rel, n_plikow=len(fs),
        Ipa_s1=ipa[0], Ipa_s2=ipa[1] if len(ipa) > 1 else np.nan, Ipa_s3=ipa[2] if len(ipa) > 2 else np.nan, Ipa_s4=ipa[-1], Ipa_sr234=ma, Ipa_sd=sa, Ipa_cv_pct=ca,
        Ipc_s1=ipc[0], Ipc_s4=ipc[-1], Ipc_sr234=mc, Ipc_sd=sc, Ipc_cv_pct=cc,
        dEp_s1=dep[0], dEp_s4=dep[-1], drift_a_s1_vs_s4_pct=100 * (ipa[0] - ipa[-1]) / abs(ipa[-1]) if not np.isnan(ipa[0]) else np.nan,
        drift_a_s2_vs_s4_pct=100 * (ipa[1] - ipa[-1]) / abs(ipa[-1]) if len(ipa) > 1 and not np.isnan(ipa[1]) else np.nan))
out = os.path.join(HERE, 'wyniki_analizy', 'powtarzalnosc_3_skany_20260822.csv')
with open(out, 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); wr.writeheader(); wr.writerows(rows)
cva = np.array([r['Ipa_cv_pct'] for r in rows], float); cvc = np.array([r['Ipc_cv_pct'] for r in rows], float)
d1 = np.array([r['drift_a_s1_vs_s4_pct'] for r in rows], float); d2 = np.array([r['drift_a_s2_vs_s4_pct'] for r in rows], float)
print(f'elektrod: {len(rows)}')
print('CV%% Ip_a skany 2-4: mediana %.2f, śr %.2f, max %.2f (n=%d)' % (np.nanmedian(cva), np.nanmean(cva), np.nanmax(cva), np.sum(~np.isnan(cva))))
print('CV%% Ip_c skany 2-4: mediana %.2f, śr %.2f, max %.2f (n=%d)' % (np.nanmedian(cvc), np.nanmean(cvc), np.nanmax(cvc), np.sum(~np.isnan(cvc))))
print('dryf Ip_a skan1 vs skan4: mediana %+.1f%%, śr %+.1f%%, zakres %+.1f..%+.1f' % (np.nanmedian(d1), np.nanmean(d1), np.nanmin(d1), np.nanmax(d1)))
print('dryf Ip_a skan2 vs skan4: mediana %+.1f%%, śr %+.1f%%' % (np.nanmedian(d2), np.nanmean(d2)))
print('\nNajgorsza powtarzalność (CV% Ip_a > 3):')
for r in sorted(rows, key=lambda r: -(r['Ipa_cv_pct'] if not np.isnan(r['Ipa_cv_pct']) else 0))[:8]:
    print('  %-45s Ip_a s1..s4: %s  CV %.1f%%  Ip_c CV %.1f%%' % (r['elektroda'], ' '.join('%.2f' % v for v in (r['Ipa_s1'], r['Ipa_s2'], r['Ipa_s3'], r['Ipa_s4'])), r['Ipa_cv_pct'], r['Ipc_cv_pct']))
print('zapisano', out)
