# Kit de double codage : mode d'emploi

## Fichiers
- `coder1_codes.csv` : le codage d'origine (premier codeur), 144 phrases, 163 codes.
- `coder2_blind_sentences.csv` : les 144 mêmes phrases, **sans codes**, à donner au second codeur.
- `kappa.py` : calcule le kappa de Cohen par dimension (contrôle, capacité dynamique, face OIPT), globalement et par catégorie.

## Procédure
1. Ouvrir une **session vierge** (nouveau LLM, sans historique) ou confier le fichier à un second codeur humain.
2. Coller le prompt ci-dessous, puis le contenu de `coder2_blind_sentences.csv`.
3. Enregistrer la réponse sous `coder2_codes.csv` (mêmes colonnes que `coder1_codes.csv`).
4. Lancer : `python kappa.py coder1_codes.csv coder2_codes.csv`
5. Seuils usuels : κ ≥ 0,61 accord substantiel, κ ≥ 0,81 accord presque parfait (Landis et Koch, 1977). En dessous de 0,61 : discuter les désaccords, préciser les règles, recoder.
6. Rapporter dans la méthode : κ par dimension, procédure de résolution des désaccords, et le fait que la décision d'inclusion (phrase codée ou non) n'est pas couverte par ce test (voir limite ci-dessous).

**Limite :** le kit ne contient que les 144 phrases retenues par le premier codeur. Pour tester aussi la décision d'inclusion, il faut fournir au second codeur les 366 phrases non méthodologiques (fichier non disponible ici).

---

## Prompt pour le second codeur (à coller tel quel)

You are the second coder in a systematic literature review on AI, management control systems (MCS) and organisational change. Code each sentence independently. Do not try to guess any previous coding.

For each sentence, identify every management control the sentence is about, and code it on three independent dimensions.

**1. control** (Malmi & Brown, 2008, MCS as a package), one of:
- `Planning`: action planning, long-range planning, budgets as plans, forecasting, resource allocation.
- `Cybernetic`: budgets as targets, financial and non-financial measurement, performance monitoring, KPIs, reporting, variance analysis, diagnostic and interactive control systems (Simons).
- `Reward`: rewards, compensation, incentives.
- `Administrative`: organisation design and structure, governance, policies and procedures, roles, tasks, responsibilities and competences of controllers, standardisation, centralisation, boundary systems (Simons).
- `Cultural`: values, beliefs, norms, symbols, clans, identity, acceptance, epistemic cultures, belief systems (Simons).
- `Unspecified MC`: the sentence refers to management control or management accounting in general without saying which control.

**2. capability** (Teece, 2007), what the control does in the sentence:
- `Sensing`: detecting, monitoring, scanning, producing or analysing information and signals.
- `Seizing`: mobilising, deciding, adopting, accepting, committing resources, coordinating a response.
- `Transforming`: reconfiguring, redesigning, changing roles, structures, routines or the control itself.

**3. face** (Organisational Information Processing Theory, Galbraith, 1973):
- `IPC` (information-processing capacity): the control processes information; it is a capacity that AI expands.
- `IPR` (information-processing requirement): the control must adapt or absorb new demands; it is the object of change.

**Rules**
- Face and capability are determined by what the control does in the sentence, never by the type of control.
- A sentence may receive several codes (one row per control).
- Code only sentences that concern a control; if a sentence concerns no control, output no row for it.

**Output format:** CSV only, with this header and one row per code:
`sentence_id,control,capability,face`
