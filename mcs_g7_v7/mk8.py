b=open("body.md").read()
def rep(old,new,cnt=1):
    global b
    assert b.count(old)>=1,old[:60]
    b=b.replace(old,new,cnt)

# title / abstract
rep('title: "Universal Practices, Heterogeneous Associations, Portable Models? Monitoring, Targets and Incentives in Seven G7 Economies"',
    'title: "National Culture and Management Control Practices: Evidence on Adoption, Performance Associations and Predictive Portability across G7 Economies"')
rep("version 7","version 8")
import re
new_abs='''abstract: |
  Management-practice evidence is often read as universal, and differences between countries are often attributed to national culture. We ask what national culture can and cannot explain, separating three notions: universality of practices, of associations with performance, and predictive portability. Using World Bank Enterprise Surveys for seven G7 economies (6,316 establishments) and three observable management-control practices (monitoring, targets and target-linked bonuses), we find marked differences in adoption (target-linked bonuses: 36% in Italy, 76% in the United Kingdom). Incentives and monitoring are associated with higher sales per employee (about 22% and 13%); targets are not. The incentives association ranges from about 66% in Canada to 5% in France but is fragile under wild cluster bootstrap and weights. A common model is not detectably improved on out of sample by national slopes, which bound any cultural moderation. Exploratory comparisons with Hofstede's dimensions, with seven countries, do not support a simple individualism or masculinity reading. Associations are cross-sectional, not causal, and predictive portability is not organisational transfer.
---'''
b=re.sub(r"abstract: \|\n.*?\n---",lambda m:new_abs,b,count=1,flags=re.S)
rep("**Keywords:** management-control practices;","**Keywords:** national culture; Hofstede; management-control practices;")

# intro: culture paragraph inserted before 'We examine the three notions'
rep("We examine the three notions with World Bank Enterprise Surveys",
"""Differences between countries are often attributed to national culture. Hofstede's dimensions (1980, 2001) offer a way to formulate expectations: acceptance of hierarchy and avoidance of uncertainty may shape how monitoring and targets are used, and individualism and masculinity how rewards are received. These are theoretical expectations, not established effects, and national scores are not measures of the culture of the establishments surveyed. With seven countries, culture can be examined only exploratorily. The article therefore asks three questions: (RQ1) whether cultural dimensions are associated with the adoption of control practices; (RQ2) whether they help interpret the heterogeneity of practice–performance associations; and (RQ3) whether cultural information could improve the predictive portability of models, a question we can bound but not fully answer with the present data.

We examine the three notions with World Bank Enterprise Surveys""")
rep("A secondary contribution concerns management control:","Secondary contributions concern national culture, for which we state what seven countries can and cannot support, and management control:")

# framework: new 2.2 culture, renumber
rep("## 2.2 From transfer to institutionalisation","""## 2.2 National culture as a contextual explanation

Hofstede (1980, 2001) characterises national cultures by dimensions, of which four are relevant to the three practices. Power distance (PDI), the acceptance of unequal power, may shape the acceptability of monitoring and of targets set from above; uncertainty avoidance (UAI), the preference for rules and procedures, may favour monitoring and targets; individualism (IDV) and masculinity (MAS), the emphasis on individual achievement and competition, may make individual rewards more or less effective (Table C1). These links are hypotheses to examine, not effects established here. They face three objections that the design must respect. National scores are not measures of the values of the employees or managers of the establishments surveyed, and moving from national scores to explanations of organisational behaviour has been criticised (McSweeney, 2002); differences between countries may also reflect labour regulation, sector structure, pay practices or questionnaire wording rather than culture (Harrison & McKinnon, 1999); and with seven countries each dimension takes only seven values.

**Table C1.** Hofstede dimensions, expected mechanism and practice concerned (theoretical expectations, not tested effects).

| Dimension | Expected mechanism | Practice concerned |
|:--|:--|:--|
| Power distance (PDI) | Acceptance of hierarchy and of control exercised by superiors | Monitoring, targets |
| Individualism (IDV) | Importance of autonomy and individual rewards | Incentives |
| Uncertainty avoidance (UAI) | Preference for rules, procedures and reduced uncertainty | Monitoring, targets |
| Masculinity (MAS) | Valuation of competition, achievement and rewards | Incentives |

## 2.3 From transfer to institutionalisation""")
rep("## 2.3 Implications for control mechanisms","## 2.4 Implications for control mechanisms")
rep("which are not measures of institutions or culture.","which are not measures of institutions or culture; culture enters only through the exploratory comparison of Section 6.9. Culture, institutionalisation and control mechanisms are linked in the framework of this article as: national culture, adoption and institutionalisation of practices, associations with performance, and implications for management control. Institutionalisation is not measured by WBES and is proposed as a mechanism, not tested.")
rep("Sections 2.3 and 7.3","Sections 2.4 and 7.3")

# hypotheses
rep("- **Boundary statement.**","""- **Cultural expectations (exploratory; seven countries).** **HC1.** Adoption of monitoring and targets is positively related to PDI and UAI, and adoption of incentives to IDV and MAS. **HC2.** The cross-country association of incentives with productivity is positively related to IDV and MAS. **HC3.** A model that includes cultural information improves out-of-sample prediction over the common model.
- **Boundary statement.**""")
rep("**Central question.** Do monitoring, target setting and incentives show the same adoption, the same associations with performance and the same predictive portability across seven advanced economies?",
"**Central question.** To what extent does national culture explain cross-country differences in the adoption and performance associations of management-control practices, and can cultural information improve the portability of models? Because the answer first requires establishing whether monitoring, target setting and incentives show the same adoption, associations and portability across seven advanced economies, the empirical work is organised by the three levels below.")
rep("Institutional moderation by national characteristics (a model with MCS × Z_c) cannot be estimated with seven countries; it is nested in a model with country-specific slopes, which therefore bounds what any such interaction could add.",
"A model with practice × cultural-dimension interactions (MCS × Z_c) cannot be estimated reliably with seven countries, since each dimension has seven values; it is nested in the national-slope model N1, which therefore bounds what any cultural moderation could add. Cultural hypotheses are examined by rank correlations at country level and are not confirmatory.")

# empirical strategy
rep("## 5.3 Level 3: predictive portability","""## 5.3 Cultural reading (exploratory)

Hofstede scores are the published national scores of Hofstede (2001) as reproduced on the Hofstede Insights country-comparison site [verify scores and date against the database used]. Country-level adoption rates (Table 2) and country-specific incentives coefficients (Table 5) are related to the relevant dimensions by Spearman rank correlations, with leave-one-country-out ranges. No p-values are reported, because seven observations cannot support them; results are descriptive and are presented to show how fragile a cultural reading would be. A meta-regression of the country coefficients on a dimension, weighted by their sampling variances, is [TO COMPLETE: to be estimated and reported with confidence intervals, in the case of incentives only].

## 5.4 Level 3: predictive portability""")
rep("## 5.2 Level 2: associations","## 5.2 Level 2: associations")

# results: add 6.9 before Discussion
rep("# 7. Discussion","""## 6.9 Exploratory cultural reading (Table C2)

*Adoption (HC1).* Across the seven countries, the adoption of target-linked bonuses is positively rank-related to individualism (ρ = 0.64; leave-one-out range 0.43 to 0.77), as expected, and not related to masculinity (ρ = −0.20; −0.64 to 0.17). The adoption of monitoring is negatively rank-related to uncertainty avoidance (ρ = −0.64; −1.00 to −0.43), the opposite of the expectation, and weakly to power distance (−0.25); targets show no clear relation (ρ = 0.11 with PDI, −0.13 with UAI). Adoption rates are confounded by size composition (Section 6.1), and these figures are not tests.

*Associations (HC2).* The incentives coefficients are not related to individualism (ρ = 0.25; leave-one-out range −0.09 to 0.43) or masculinity (ρ = 0.09; −0.46 to 0.41); the highest-masculinity country, Japan (MAS = 95), has one of the lowest coefficients (0.082), and Canada (IDV = 80), with the highest coefficient (0.509), is not the most individualist country (United States, IDV = 91, 0.154). The only moderate relation concerns power distance (ρ = −0.59; −0.81 to −0.35), and uncertainty avoidance to a lesser degree (ρ = −0.39; −0.54 to −0.09): countries with lower power distance show larger incentives coefficients. This relation was not hypothesised for incentives and rests on seven points, among which France (PDI = 68, coefficient 0.048) weighs heavily. For monitoring and targets, rank correlations between coefficients and PDI or UAI are not interpretable: the coefficients are statistically homogeneous across countries (I² = 5% and 0%, Table 5), so their ordering reflects estimation noise (for example ρ = 0.85 between targets and PDI). HC2 is not supported, and a simple reading in which cultures that value competition or individual rewards show stronger incentive–performance associations is not borne out.

*Prediction (HC3).* The national-slope model N1 contains any model with a cultural moderator, and N1 is not detectably better than the common model P1 (Section 6.6); the oracle gain of 0.0028 therefore also bounds what cultural information could add through slopes. [TO COMPLETE: out-of-sample comparison of a cultural model (practice × one dimension) against P1, N1 and HB, folds identical to Table 9.]

**Table C2.** Hofstede scores (published national scores), incentives–productivity coefficient (Table 5) and adoption of target-linked bonuses (Table 2), by country.

| Country | PDI | IDV | MAS | UAI | Incentives coefficient | Bonuses (%) |
|:--|--:|--:|--:|--:|--:|--:|
| Canada | 39 | 80 | 52 | 48 | 0.509 | 63 |
| Italy | 50 | 76 | 70 | 75 | 0.360 | 36 |
| Germany | 35 | 67 | 66 | 65 | 0.225 | 59 |
| United Kingdom | 35 | 89 | 66 | 35 | 0.202 | 76 |
| United States | 40 | 91 | 62 | 46 | 0.154 | 67 |
| Japan | 54 | 46 | 95 | 92 | 0.082 | 54 |
| France | 68 | 71 | 43 | 86 | 0.048 | 48 |

# 7. Discussion""")

# discussion: 7.2 add culture; 7.4 add
rep("## 7.3 Contribution to management control","""## 7.3 What national culture can and cannot explain

The cultural reading is weaker than the question suggests. The expectation that individualist or masculine cultures show stronger incentive–performance associations is not supported, and the one moderate relation, with power distance, was not predicted and rests on seven points. Even if it held, three objections limit its meaning: national scores are not measures of the values of the establishments surveyed (McSweeney, 2002); country differences may reflect labour regulation, sector structure, pay practices or item wording; and the heterogeneity to be explained is itself statistically fragile (Holm-adjusted bootstrap p = 0.105). The data therefore do not show that culture explains differences in associations, and they do not show that it does not. Establishing a moderating role would require many more countries with the same items and multilevel models; Section 10 describes that extension. What the present results do contribute is a bound: because national slopes do not detectably improve prediction, there is little predictive gain for cultural information to capture at this sample size.

## 7.4 Contribution to management control""")
rep("## 7.4 What cannot be concluded","## 7.5 What cannot be concluded")
rep("That each country needs its own set of management-control practices or models, or that contexts are irrelevant, is not established;","That culture explains the cross-country differences, that each country needs its own set of management-control practices or models, or that contexts are irrelevant, is not established;")

# contributions
rep("3. **Secondary contribution: a bridge to management control.**","3. **Secondary contribution: what a cultural reading can support.** With seven countries, expectations drawn from Hofstede's dimensions are not supported for incentives, and any cultural moderation is bounded by the national-slope model; the article states what a credible test would require.\n4. **Secondary contribution: a bridge to management control.**")
rep("# 9. Managerial and policy implications","# 9. Managerial and policy implications")

# limitations & future research
rep("(viii) The literature review","(viii) Hofstede scores are historical national indicators, not measures of the culture of the establishments surveyed or of 2024–2025, and cultural analyses rest on seven observations. (ix) The literature review")
rep("**Future research.** Measure integration","**Future research.** Extend the analysis to several dozen WBES countries, after verifying that the same monitoring, target and bonus items are available, with multilevel models in which cultural dimensions are country-level moderators and uncertainty about country slopes is propagated. Measure integration")

# references
rep("Holm, S. (1979).","Hofstede, G. (1980). *Culture's consequences: International differences in work-related values*. Sage.\n\nHofstede, G. (2001). *Culture's consequences: Comparing values, behaviors, institutions and organizations across nations* (2nd ed.). Sage.\n\nHolm, S. (1979).")
open("body8.md","w").write(b)
