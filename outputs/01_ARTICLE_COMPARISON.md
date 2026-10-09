# 01 - How the three articles complement one another

All statements below come from the PDFs in `data/raw/`; page numbers are PDF pages (identical to printed pages) and are machine-verified in `01_ARTICLE_EXTRACTION.xlsx` (sheet `Page_verification`).

## 1. What each article actually does

| | Phan (2026), *Discover Sustainability* | Sime & Tadesse (2025), *J. Innovation & Entrepreneurship* | Adewumi & Zhang (2026), *J. Cleaner Production* |
|---|---|---|---|
| Question | Do green economy practices (GEP) raise the probability of product/process innovation? (p.2, H1 p.5) | Does innovation (product, process, R&D) change labour productivity and employment of different worker groups? (p.3) | Does employee education condition the financial payoff of green innovation (GI)? (p.2; H1-H2 p.3) |
| Role of innovation | **Outcome** (h1 product, h5 process; Table 1 p.7) | **Treatment** (dummy and 0-10 dose; p.15) | **Mechanism/explanatory** (GI count, sector-standardised; Eq. 1 p.4) |
| Outcomes | Innovation (binary) | Sales per worker and employment by worker category (p.15) | Sales growth, profit growth, gross margin (p.4, Table 2 p.6) |
| Data | WBES Green Economy module, 42 countries 2018-2023, N=18,860 (p.5); includes Morocco (n=195, p.8), not Korea | WBES pseudo-panel, 9 African countries, N=2,923 (p.11) | WBES 2018-2019, 42 countries, N=8,941 (p.4) |
| Method | Logit (odds ratios), country/year/industry FE, country-clustered SE (p.7) | Propensity-score matching (ATT) and dose-response (pp.11-15) | OLS, 2SLS with a region-standardised R&D instrument, control function, PSM (pp.5-10) |
| Headline result | +1 GEP -> odds of product innovation x1.157, process x1.194 (Table 6, p.10) | Innovation raises employment of several segments but lowers productivity of most (production workers excepted) (abstract p.1; conclusion p.24) | 2SLS: GI -> sales growth 0.111***, GI x education -0.053* (Table 4, p.7) |
| Causal status | Cross-sectional associations; authors admit causality is not established (p.15) | Selection on observables (CIA, common support; p.12) | Instrumental variables, but exclusion restriction is contestable (p.5) |

## 2. How they complement each other (actual, not assumed)

* **Phan -> D4 and the innovation measures.** Provides the exact WBES items for product and process innovation (h1, h5) and shows that green *practices* are associated with innovation. It supplies the environmental dimension and a documented operationalisation, but treats green practice as a *cause of innovation*, not as an inclusive-growth outcome.
* **Sime & Tadesse -> D1/D2 and labour segmentation.** Its distinctive contribution is that innovation can raise employment while lowering productivity, and that effects differ by worker group. It supplies the productivity (sales per worker) and employment logic and warns against treating "growth" as one thing.
* **Adewumi & Zhang -> D1 and the human-capital/D3 link.** Supplies a three-year sales-growth definition (p.4), a green-innovation measure and the claim that returns to green innovation depend on workforce education. This is the only article that relates a *workforce-composition* variable to firm performance.

Complementarity in one sentence: Phan explains *where innovation comes from* (green practice), Sime & Tadesse shows *what innovation does to jobs and productivity*, and Adewumi & Zhang shows *that the payoff depends on the workforce*.

## 3. What the articles do NOT do (limits of the overlap)

* None of the three measures **inclusive growth**; none builds a multidimensional or composite index; none studies **Morocco and Korea together**; none has a digitalization variable beyond a website covariate (Sime & Tadesse own_web, p.16).
* None observes **growth of female or low-skilled employment**; Sime & Tadesse analyse employment *levels* by category.
* Their data are **different waves/modules**: Phan's Green Economy module (BMGc23a-j, 2018-2023) and Adewumi & Zhang's ten green-investment items are not in the 2023/2024 Morocco/Korea files (Phase 3, class E).
* Causal identification is weak or contestable in all three (cross-sectional logit; PSM on observables; IV with a debatable exclusion restriction).

## 4. Our proposed theoretical integration (ours, not the articles')

The following mapping is our own proposal and is tested for feasibility, not asserted:

| Our dimension | Source of inspiration | Feasible in Morocco 2023 / Korea 2024? |
|---|---|---|
| D1 Economic growth | Adewumi & Zhang (sales growth); Sime & Tadesse (productivity) | Yes (class B; nominal, differing windows) |
| D2 Employment growth | Sime & Tadesse (employment) | Yes (class B; total only) |
| D3 Social inclusion | Sime & Tadesse (worker categories); Adewumi & Zhang (education) | Only as composition at one date (female share, low-skilled share of production workers); education index not reproducible |
| D4 Environmental | Phan (GEP); Adewumi & Zhang (GI) | Two practice items only (ge8d, ge7); the GEP/GI items are absent |
| Innovation, digitalization | Phan (h1, h5), Sime & Tadesse | Explanatory variables: product and process innovation (class A); digitalization only a website proxy (class C) |

Deviations from the source articles are listed in `07_RESEARCH_REPORT.md` (section "Methodological deviations").
