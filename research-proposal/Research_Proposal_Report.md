# Machine Learning-Based Reconstruction and Cross-Ocean Validation of Missing Planktonic Foraminiferal Abundance Data

**Research Proposal Report**

| | |
|---|---|
| **Candidate** | R. Ranjith Kumar (Roll No. 22JE0757) |
| **Supervisor** | Dr. Ajoy Kumar Bhaumik |
| **Research area** | Micropalaeontology · Palaeoceanography · Machine Learning |
| **Study interval** | approximately 0–7 Ma, subject to dataset availability |
| **Training data** | published, openly licensed PANGAEA foraminiferal records |
| **External test data** | independent Atlantic and Indian Ocean datasets supplied by the supervisor |
| **Proposed duration** | 8 months (August – March) |

---

## 1. Introduction

### 1.1 Background

Deep-sea sediments accumulate slowly and more or less continuously, and in doing so they preserve one of the few archives from which the state of the ocean before the instrumental era can be reconstructed quantitatively. Among the fossils contained in these sediments, foraminifera are the most widely used. They are unicellular marine protists that secrete a calcareous test, and they occur in two ecologically distinct groups: planktonic species, which live in the upper water column, and benthic species, which live at or within the sea floor. Because the tests of both groups are preserved in sediment in large numbers and can be identified to species level, a single sediment core yields a stratigraphically ordered sequence of quantitative biological census data (Hemleben, Spindler and Anderson, 1989).

The palaeoceanographic value of planktonic foraminifera follows from their ecology. The distribution of individual species in the modern ocean is governed by sea-surface temperature, water-column stratification, salinity and nutrient supply, so the *composition* of a fossil assemblage — the relative proportion of each species in a sample — carries information about the surface conditions under which that assemblage lived. This principle is the basis of quantitative palaeoceanography: assemblage census counts are converted into estimates of past surface conditions using transfer functions and analogue techniques, an approach introduced by Imbrie and Kipp (1971) and refined extensively since (Kučera, 2007). Benthic foraminiferal assemblages, usually analysed together with stable carbon and oxygen isotope measurements on their tests, are used in a parallel way to infer deep-water mass properties and ventilation.

The practical output of this work is highly standardised in form. A micropalaeontological study of a core produces a table in which each row is a sediment sample, identified by depth below sea floor and, where an age model exists, by numerical age; and each column is a species, an isotopic parameter, or a derived index. The entries are counts, relative abundances (percentages of the counted assemblage) or concentrations. Because several hundred specimens are conventionally identified per sample from a standard size fraction, a single record commonly contains thousands of individual numerical observations distributed across tens of species.

Over the past two decades these tables have become openly available rather than remaining in appendices. PANGAEA, the Data Publisher for Earth and Environmental Science, archives such datasets with persistent DOIs, machine-readable parameter definitions and site metadata (Diepenbroek *et al.*, 2002). This has changed how micropalaeontological data can be used: records produced for one study at one site can, in principle, be pooled across sites and re-analysed at a scale that no single laboratory could generate. The scientific relevance of the present proposal begins here. The analyses that these records exist to support — time-series and spectral analysis of abundance variation, ordination of assemblages, calibration of transfer functions, and multi-site synthesis — all assume a numerically complete data matrix. Where the matrix is incomplete, the analysis cannot simply proceed with the gaps left in place.

### 1.2 Research context

The material of this study is the population of published, openly licensed tabular foraminiferal records held on PANGAEA, with a training base drawn from the western North Atlantic and an external test set drawn from independent Atlantic and Indian Ocean sites.

A representative and well-documented example is the record of Nishi, Norris and Okada (2000), which reports relative abundances of planktonic foraminifera from ODP Hole 164-997A on the Blake Ridge (31.84° N, 75.47° W; 2,770 m water depth). The dataset comprises 56 parameters covering 51 species across 91 samples — approximately 5,005 individual data points — and spans the latest Pliocene to Holocene (approximately the last 2.15 Ma). Its structure is typical of the class of data this research addresses: wide (many species columns), short (fewer than a hundred samples), and unevenly populated, because most species are not present, or not reported, in every sample. Complementary records from the same broad region extend the available material both in time and in parameter type. Bhaumik, Gupta and Thomas (2011) published a benthic foraminiferal and stable carbon isotope record from the Blake Outer Ridge covering approximately the last 7 Ma; Lutz (2011) published planktonic foraminiferal data from ODP Hole 172-1063A on the Blake–Bahama Outer Ridge; and Chaisson, Poli and Thunell (2002) published stable isotope data together with planktonic foraminiferal composition from ODP Site 172-1056. Together these constitute a compatible set of western North Atlantic records that share a broad geographic setting and a common data model, while differing in site, water depth, time span and the specific parameters reported.

Three characteristics of this material define the technical problem. First, the records are *heterogeneous*: taxonomic nomenclature, units (counts, percentages, concentrations), age conventions (ka or Ma, and different underlying timescales), size fractions and missing-value conventions differ between authors, so records cannot be concatenated without deliberate harmonisation. Second, they are *sparse in a structured way*: an empty cell may mean that the species was genuinely absent from the counted assemblage, that it was present but not distinguished by that author, that it fell below a reporting threshold, or that the sample was not analysed for that parameter at all. These are different conditions with different implications, and they are frequently encoded identically. Third, they are *small*: a few tens to a few hundred samples per site is normal, which places the problem firmly in the small-to-medium tabular data regime rather than the large-sample regime in which most modern machine-learning practice is developed.

Current practice for handling incomplete micropalaeontological tables is largely informal. Samples containing missing entries are deleted from the analysis, gaps are filled by linear interpolation along the depth or age axis, or absent entries are set to zero on the assumption that they represent true absences. General-purpose statistical imputation methods exist and are mature — multiple imputation by chained equations (van Buuren and Groothuis-Oudshoorn, 2011) and random-forest imputation (Stekhoven and Bühlmann, 2012) are standard in other data-intensive disciplines — but they are seldom applied to, and have not been systematically evaluated on, published foraminiferal census data.

In parallel, machine learning has entered micropalaeontology decisively, but along a different route. Johansen and Sørensen (2020) demonstrated transfer-learning-based detection and classification of foraminifera from microscope images; Johansen *et al.* (2021) extended this to instance segmentation; and Karaderi *et al.* (2021) showed that deep metric learning can classify planktic foraminifera and encode morphological similarity. This body of work targets the *acquisition* stage of the workflow — turning specimens into identifications — and demonstrates convincingly that learned models can handle foraminiferal data. It does not address the *tabular* records that acquisition produces, and it does not address what happens to those records once they are published with gaps in them.

### 1.3 Motivation

The position can be stated as a short progression. It is established that planktonic foraminiferal assemblages carry quantitative information about past ocean conditions, and that a large volume of such data is openly published in a reusable tabular form. It is also established that machine-learning models can perform demanding recognition tasks on foraminiferal material, and, separately, that supervised regression and imputation methods perform well on tabular data in other fields.

What follows from this combination is not yet established. The tabular records are treated as raw source data to be read, not as training material from which the statistical structure of an assemblage might be learned; the informal gap-filling procedures actually used are not benchmarked against each other or against alternatives; and, most consequentially, there is no evidence about whether a model that reconstructs missing values well within the dataset it was trained on continues to do so on a core it has never seen. This last point matters more in geoscience than in most application domains, because samples from a single core are autocorrelated in time, share a single analyst, laboratory protocol and size fraction, and reflect one regional oceanographic setting. A model evaluated by randomly holding out rows from such a dataset is being asked an easy question, and may return an optimistic answer that does not survive contact with a new site or a new ocean basin.

The need, therefore, is for a controlled and honestly validated assessment: whether missing quantitative observations in published foraminiferal records can be reconstructed accurately enough to be scientifically usable, how that accuracy behaves as the amount of missing data increases, which algorithms are dependable at this data scale, and whether performance transfers to genuinely independent records. This proposal addresses that need. Its formal statement of the research gap is developed in Section 3, after the relevant literature has been examined.

---

## 2. Literature Survey

The literature relevant to this proposal falls into four connected bodies of work: the palaeoceanographic framework that gives foraminiferal abundance data their meaning; the published tabular datasets that constitute the empirical material; computational and machine-learning approaches applied so far in micropalaeontology; and the wider methodological literature on missing data and on validating models built from spatially structured data. Each is examined below in terms of what was done, what was found, what is useful for the present work, and what limitation remains.

### 2.1 Planktonic foraminifera as palaeoceanographic proxies: the scientific framework

The interpretative framework for foraminiferal census data was established by work linking assemblage composition to surface-ocean conditions. Imbrie and Kipp (1971) formalised the transfer-function approach, in which a statistical relationship is calibrated between modern assemblage composition and modern hydrographic variables and then applied to fossil assemblages to reconstruct past conditions. Subsequent decades of ecological and taxonomic work, synthesised by Hemleben, Spindler and Anderson (1989) and reviewed in a palaeoceanographic context by Kučera (2007), established the biological basis for that relationship: species have distinct depth habitats, temperature tolerances and seasonal preferences, and assemblage composition therefore varies systematically along oceanographic gradients.

Two consequences of this framework are directly useful here. First, a fossil assemblage is not a random collection of independent species counts; it is a structured, internally correlated object in which species co-occur in predictable combinations. That internal structure is precisely what a supervised model could learn in order to estimate an unobserved abundance from the observed remainder of the same assemblage. Second, the framework establishes the standard against which any reconstruction must be judged. The purpose of these data is quantitative environmental inference, so a reconstruction is adequate only if the reconstructed record supports the same inference as the complete record would — a stricter criterion than minimising an error metric.

The limitation of this body of work, from the present perspective, is that it assumes complete assemblage data as its starting point. It specifies what the data mean, but offers no procedure for what to do when part of the assemblage matrix is absent.

### 2.2 Published tabular abundance and isotope datasets: the empirical evidence base

A substantial body of published, openly licensed records provides the material for this study. Nishi, Norris and Okada (2000) reported planktonic foraminiferal relative abundances from ODP Hole 164-997A on the Blake Ridge, a compact record of 51 species across 91 samples spanning the latest Pliocene to Holocene. Lutz (2011) published a compatible planktonic foraminiferal dataset from ODP Hole 172-1063A on the Blake–Bahama Outer Ridge. Bhaumik, Gupta and Thomas (2011) reported benthic foraminiferal assemblages together with stable carbon isotope data from the Blake Outer Ridge across approximately the last 7 Ma, demonstrating the palaeoceanographic value of long, continuous records for tracking deep-water conditions. Chaisson, Poli and Thunell (2002) contributed stable isotope measurements and planktonic foraminiferal composition from ODP Site 172-1056, adding a further western North Atlantic record in which assemblage and geochemical parameters occur together in the same table.

Collectively these studies establish that rich, openly published abundance, age and isotope records exist across multiple North Atlantic sites, that they are consistent enough in structure to be considered jointly, and that they cover a time span compatible with the approximately 0–7 Ma interval of interest. They also establish, in the case of Bhaumik, Gupta and Thomas (2011) and Chaisson, Poli and Thunell (2002), that geochemical parameters are available alongside assemblage data in at least some records, which is relevant to the construction of predictor variables.

The limitation these studies share is one of use rather than of quality. In the subsequent literature they function as raw source data — cited, read, and interpreted — but they have not been treated as training material from which the statistical structure of foraminiferal assemblages might be learned, nor has the incompleteness of their data matrices been treated as a problem worth solving systematically. The datasets themselves are the evidence that the gap identified in Section 3 exists in practice and not merely in principle.

### 2.3 Computational and machine-learning approaches in micropalaeontology

Machine learning has been applied to foraminifera with clear success, but on a consistent class of problems. Johansen and Sørensen (2020) applied transfer learning to microscope images of foraminifera, showing that pre-trained convolutional networks can detect and classify specimens without the very large annotated datasets such models normally require. Johansen *et al.* (2021) advanced this to instance segmentation, separating individual specimens within an image and delineating their outlines, which is the harder task required for automated counting. Karaderi *et al.* (2021) took a different approach, using deep metric learning to embed specimen images in a similarity space, thereby classifying planktic foraminifera while also representing morphological relationships between taxa rather than only assigning discrete labels.

What this work found is that the identification bottleneck in micropalaeontology is tractable by machine learning, and that models can capture morphological information at a level useful for taxonomy. What it contributes here is both practical and rhetorical: it establishes methodological precedent for machine learning in this discipline, and it identifies image-based specimen recognition as the settled frontier of that effort.

Its limitation, stated plainly, is that all of it operates upstream of the tabular record. These methods generate or replicate identifications; they take no position on the completeness, consistency or reusability of the abundance tables that identifications eventually become. Once a record is published with missing entries, none of these approaches offers any means of addressing them.

### 2.4 Missing-data treatment and validation design for structured tabular data

The statistical treatment of missing data is a mature field with a formal foundation. Rubin (1976) established the classification of missingness mechanisms — missing completely at random (MCAR), missing at random (MAR) and missing not at random (MNAR) — and showed that the validity of any imputation depends on which mechanism applies; Little and Rubin (2019) provide the standard modern treatment. Two practical methods dominate application: multiple imputation by chained equations (van Buuren and Groothuis-Oudshoorn, 2011), which models each incomplete variable conditionally on the others, and random-forest imputation (Stekhoven and Bühlmann, 2012), which is non-parametric, handles mixed data types and performs well without distributional assumptions. On the supervised side, the algorithms proposed for this study are all well characterised: random forests (Breiman, 2001) are robust with limited sample sizes and yield interpretable variable importances; support vector regression (Smola and Schölkopf, 2004) is effective when the number of predictors is large relative to the number of samples; and regularised gradient boosting as implemented in XGBoost (Chen and Guestrin, 2016) is a consistently strong performer on tabular problems.

A second and equally important methodological literature concerns how such models should be evaluated when the data are not independent. Roberts *et al.* (2017) showed that for data with temporal, spatial or hierarchical structure, random cross-validation systematically overestimates predictive performance, because training and test partitions drawn at random share the very dependence structure the model is credited with having learned; they recommend blocked or grouped validation schemes in which whole spatial or temporal units are held out. This finding is directly applicable to foraminiferal records, which are simultaneously time series (samples ordered by depth and age within a core) and spatially grouped (samples clustered within sites and basins, sharing analytical practice).

A further consideration specific to this data type is that relative abundances are compositional: the species proportions within a sample are constrained to a constant sum. Aitchison (1986) established that such data violate the assumptions of standard multivariate statistics, and that predicting one component without regard to the constraint can produce results that are numerically reasonable but internally inconsistent.

The limitation of this literature is that it is generic. It specifies the correct framework, the appropriate algorithms and the correct validation design, but it has not been instantiated on published micropalaeontological census data, whose particular combination of small sample size, high dimensionality, zero-inflation, compositional closure and ambiguous missing-value coding is not represented in the datasets on which these methods are normally demonstrated.

### 2.5 Recent developments and synthesis

The most recent contributions in this space — Johansen and Sørensen (2020), Johansen *et al.* (2021) and Karaderi *et al.* (2021) — confirm that the current direction of travel in AI-assisted micropalaeontology is towards richer image-based analysis: from classification to segmentation to learned morphological similarity. Over the same period, the tabular data holdings on PANGAEA have continued to grow, with records such as those of Lutz (2011) and Bhaumik, Gupta and Thomas (2011) added as openly citable datasets. Methodologically, the recognition that spatially and temporally structured data require blocked validation (Roberts *et al.*, 2017) has become established practice in ecological and environmental modelling.

These three developments have not yet been brought together. The image-based work does not extend to the tabular records; the growing tabular archive is not being used as training material; and the validation standard now expected in adjacent environmental disciplines has not been applied to reconstruction of micropalaeontological data, because no such reconstruction has been systematically attempted. The gap that follows from this synthesis is set out in Section 3.

---

## 3. Research Gap

### 3.1 What is already established

The literature supports four secure statements. Planktonic foraminiferal assemblage composition is an internally structured, environmentally controlled quantity from which past surface-ocean conditions can be inferred (Imbrie and Kipp, 1971; Kučera, 2007). Extensive tabular records of that composition, together with associated age, depth and stable isotope parameters, are openly published, citable and technically reusable (Nishi, Norris and Okada, 2000; Chaisson, Poli and Thunell, 2002; Bhaumik, Gupta and Thomas, 2011; Lutz, 2011). Machine learning is demonstrably capable on foraminiferal material, at least for image-based recognition tasks (Johansen and Sørensen, 2020; Johansen *et al.*, 2021; Karaderi *et al.*, 2021). And the statistical machinery required to model and impute incomplete tabular data, together with the validation designs appropriate to spatially structured data, is mature and well documented (Rubin, 1976; Breiman, 2001; Smola and Schölkopf, 2004; Chen and Guestrin, 2016; Roberts *et al.*, 2017; Little and Rubin, 2019).

### 3.2 What remains unresolved

**(i) A methodological gap: reconstruction of tabular records has not been attempted.** Existing artificial-intelligence work on foraminifera is directed at images — detection, classification and segmentation of specimens (Johansen and Sørensen, 2020; Johansen *et al.*, 2021; Karaderi *et al.*, 2021). No comparable effort addresses missing quantitative values in the tabular records that specimen identification produces. The consequence is that the informal procedures actually used to close gaps in published records — listwise deletion, linear interpolation, zero substitution — remain unbenchmarked: their error characteristics are unknown, and there is no evidence as to whether a model that exploits the correlation structure of an assemblage would do better or worse. The unresolved question is whether the internal statistical structure of a foraminiferal assemblage is strong enough to support quantitative reconstruction of an unobserved abundance at all.

**(ii) An application gap: the published archive is not used as training material.** The PANGAEA records identified in Section 2.2 are extensive, harmonisable and openly licensed, and they are routinely used as data sources for interpretation. They have not been used as training data for reconstruction. The consequence is that a growing body of openly published quantitative micropalaeontological data remains under-exploited, and that gaps in legacy records continue to be resolved by discarding samples — an approach that removes real observations in order to compensate for absent ones, and that becomes increasingly costly as more records are combined in multi-site syntheses. The unresolved question is whether a model trained across several published records can recover values well enough to restore those records to analysable, continuous form.

**(iii) A generalisation gap: performance under random hold-out has not been tested against spatially independent validation.** Where predictive models are built on geoscientific data, the standard evaluation is a random train–test split. Roberts *et al.* (2017) established that this is systematically optimistic for data with temporal, spatial or hierarchical structure — exactly the structure of core-based micropalaeontological records, in which adjacent samples are autocorrelated and all samples from a site share an analyst, a laboratory protocol, a size fraction and a regional oceanographic setting. The consequence is that a reconstruction model reported as accurate under random hold-out could nonetheless fail on a core from a different site or ocean basin, and the failure would be invisible in the reported metrics. The unresolved question is how large the difference between random-split and site- or basin-level performance actually is for this class of data, and therefore whether reconstruction is transferable or only ever site-specific.

### 3.3 Statement of the central research gap

No study has established whether missing quantitative observations in published tabular planktonic foraminiferal records can be reconstructed by machine learning to a scientifically usable accuracy, how that accuracy depends on the proportion of missing data and on the choice of algorithm, or — critically — whether performance measured by random hold-out within a training dataset is retained when the model is applied to genuinely independent cores from other ocean basins.

---

## 4. Problem Statement

Published micropalaeontological and palaeoceanographic datasets on PANGAEA frequently contain missing quantitative observations. This incompleteness is a substantive obstacle rather than a formatting inconvenience, because the analyses these records support — continuous time-series analysis, assemblage ordination, transfer-function calibration and multi-site synthesis — require numerically complete matrices. The procedures currently used to resolve the problem either discard information or impose assumptions about the shape of the missing data that have never been tested against known values.

The limitation in current knowledge is twofold. First, it is not established that the correlation structure within and between foraminiferal records is sufficient to support quantitative reconstruction of a withheld abundance value, nor which class of model does so most reliably at the sample sizes typical of these datasets. Second, and more consequentially for the credibility of any such method, it is not established that reconstruction performance measured on randomly withheld rows of a training dataset carries over to an independent core, because the standard random-split evaluation is optimistic for data that are autocorrelated in depth and grouped by site.

This matters because the value of a reconstruction method lies entirely in its application to records the model has not seen. A method validated only on random hold-outs would appear successful while offering no assurance that a reconstructed value in a new core is meaningful — and reconstructed values, once inserted into a published record, propagate into every downstream palaeoceanographic interpretation drawn from it.

What must therefore be investigated is whether machine learning can reconstruct missing planktonic foraminiferal observations accurately enough to be scientifically usable, and whether that accuracy holds when the model is tested on genuinely independent ocean-basin data. Three research questions follow directly:

- **RQ1.** How accurately can machine-learning models reconstruct missing planktonic foraminiferal abundance values, and how does accuracy degrade as the proportion of missing data increases from 10 % to 40 %?
- **RQ2.** Which algorithm performs most reliably for this task on the small-to-medium tabular datasets characteristic of published geological records?
- **RQ3.** Does performance measured under random hold-out transfer to genuinely independent, cross-ocean datasets?

---

## 5. Objectives

The overall aim of this research is to develop and externally validate a machine-learning workflow that reconstructs missing planktonic foraminiferal abundance data from published records, and to establish whether that workflow generalises across independent ocean basins. Four specific objectives follow.

**Objective 1 — To compile and harmonise a reproducible, machine-learning-ready dataset** from published PANGAEA planktonic and benthic foraminiferal records, resolving inconsistencies in species nomenclature, measurement units, age conventions, sampling metadata and missing-value coding.

**Objective 2 — To develop and benchmark machine-learning regression and imputation models** — linear regression as a baseline, random forest, support vector regression and XGBoost — under controlled missing-data scenarios of 10 %, 20 %, 30 % and 40 %, evaluated using MAE, RMSE and R².

**Objective 3 — To evaluate model generalisation** by directly comparing performance under random hold-out validation against performance under site- and ocean-based external validation, and to quantify the difference between them.

**Objective 4 — To test the final model on independent Indian Ocean and Atlantic Ocean datasets** and to interpret the results in a palaeoceanographic context, identifying the conditions under which reconstruction is reliable and those under which it is not.

**Table 1 — Traceability of research gap, objectives, methodology and expected outcome**

| Gap component (§3.2) | Objective | Methodology section | Expected outcome |
|---|---|---|---|
| (ii) Application gap | O1: Compile and harmonise | 6.1, 6.2, 6.3 | Documented, reproducible ML-ready dataset and taxonomic lookup table |
| (i) Methodological gap | O2: Develop and benchmark models | 6.4, 6.5, 6.6 | Comparative benchmark of model accuracy against missingness rate |
| (iii) Generalisation gap | O3: Compare validation regimes | 6.7 | Quantified difference between random and spatially blocked validation |
| (iii) Generalisation gap + interpretation | O4: External test and interpretation | 6.7, 6.8, 6.9 | Cross-basin transfer assessment and palaeoceanographic interpretation |

---

## 6. Methodology

### Workflow overview

```
   ┌──────────────────────────────────────────────────────────────┐
   │  1. DATASET DISCOVERY & ACQUISITION                    (6.1) │
   │     PANGAEA records, ~0–7 Ma; supervisor-supplied             │
   │     Indian Ocean / Atlantic sets quarantined as external test │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  2. HARMONISATION & QUALITY CONTROL                    (6.2) │
   │     species names · units · age scales · missing-value codes  │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  3. EXPLORATORY & MICROPALAEONTOLOGICAL ANALYSIS       (6.3) │
   │     distributions · correlation · missingness structure       │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  4. TARGET & PREDICTOR PREPARATION                     (6.4) │
   │     target abundance variables · assemblage, stratigraphic    │
   │     and geographic predictors · transformations               │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  5. CONTROLLED MISSING-DATA MASKING                    (6.5) │
   │     10 % · 20 % · 30 % · 40 % withheld, repeated               │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  6. MODEL DEVELOPMENT                                  (6.6) │
   │     baseline · linear regression · RF · SVR · XGBoost         │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  7. DUAL VALIDATION + EXTERNAL TEST                    (6.7) │
   │     random hold-out │ site/basin hold-out │ unseen basins      │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  8. INTERPRETATION                                     (6.8) │
   │     feature importance · error structure · geological meaning │
   └──────────────────────────┬───────────────────────────────────┘
                              ↓
   ┌──────────────────────────────────────────────────────────────┐
   │  9. FINAL OUTPUTS                                      (6.9) │
   │     dataset · code · benchmark · reconstructed records        │
   └──────────────────────────────────────────────────────────────┘
```

Stages 5 and 7 carry the methodological novelty of the study and are treated in correspondingly greater detail below.

### 6.1 Data acquisition

**Sources.** All training data will be obtained from PANGAEA, using parameter- and keyword-based searches for planktonic and benthic foraminiferal abundance records associated with ODP and DSDP holes, filtered to the approximate interval 0–7 Ma. The four records identified in the literature survey form the initial core of the compilation: Nishi, Norris and Okada (2000), Chaisson, Poli and Thunell (2002), Bhaumik, Gupta and Thomas (2011) and Lutz (2011). Additional records will be added where they satisfy the inclusion criteria below, with the search documented so that the compilation is reproducible.

**Inclusion criteria.** A dataset will be admitted if it provides (i) quantitative species-level abundance data or compatible quantitative parameters, rather than qualitative presence/absence; (ii) sample-level depth below sea floor and, where available, numerical age; (iii) documented site metadata including latitude, longitude and water depth; and (iv) an open licence and a citable DOI.

**External test data.** Independent Indian Ocean and Atlantic Ocean datasets supplied by the supervisor will be reserved as an entirely unseen external test set. These data will not be inspected, summarised or used in any development decision until model development is complete and frozen. This provides two levels of externality: the independent Atlantic dataset tests transfer to a new site within a broadly familiar basin, while the Indian Ocean dataset tests transfer to a different ocean basin altogether.

**Scope condition.** Availability of the supervisor-supplied external datasets is a stated dependency of this proposal rather than an assumption. Should they prove unavailable or unsuitable, Objective 4 will be addressed using a substitute external test constructed from PANGAEA records held out at the site level from the outset and quarantined under the same conditions. This preserves the logic of external validation, although with a smaller geographic contrast, and the reduced scope would be reported explicitly.

**Expected format.** PANGAEA records are distributed as tab-delimited text files with a structured metadata header. Each will be parsed into a table of samples (rows) against parameters (columns), with the metadata header retained as record-level provenance.

### 6.2 Data preparation and pre-processing

Because the compilation draws on records produced independently by different authors, harmonisation is not a preliminary formality but a substantive component of the work, and it is the step on which the validity of everything downstream depends.

**Provenance retention.** Dataset DOI, site, hole, latitude, longitude and water depth will be attached to every sample as explicit fields. These are required later to define grouped validation partitions, and losing them during concatenation would make spatially blocked validation impossible.

**Taxonomic harmonisation.** Species names will be reconciled to a single accepted list, resolving synonyms, abbreviations and differences in the level of taxonomic splitting between authors. Open nomenclature (`cf.`, `aff.`, `sp.`) and grouped taxa (for example, colour varieties reported jointly by one author and separately by another) will be handled by an explicit rule: where one record splits a taxon that another lumps, the split categories will be summed to the coarser common level, so that comparability is achieved by deliberate loss of resolution rather than by silent mismatch. Every mapping decision will be recorded in a version-controlled lookup table published with the dataset.

**Unit and age harmonisation.** Counts, relative abundances and concentrations will be converted to a common quantitative basis, with the original unit retained as a field. Ages reported in ka and Ma will be converted to a single numeric scale, and both stratigraphic depth and age will be retained, since depth defines within-core ordering while age permits cross-core comparison.

**Missing-value semantics.** Empty cells will be classified, as far as the source documentation allows, into (a) true absence from the counted assemblage, which is a structural zero and a valid observation; (b) not reported or not distinguished by that author; (c) below a stated counting or reporting threshold; and (d) parameter not measured for that sample. Only categories (b)–(d) constitute missing data for the purposes of this study. Conflating category (a) with the others would systematically corrupt both the training targets and the evaluation, and separating them is therefore treated as a quality-control requirement rather than a refinement.

**Quality control.** Checks will include duplicate sample detection, physically impossible values (negative abundances, percentages exceeding 100), row-sum closure checks on relative abundance data, monotonicity of depth and age within each core, and screening for outliers that indicate transcription errors rather than genuine variation.

**Scaling.** Predictors will be standardised for scale-sensitive learners (linear regression, support vector regression); tree-based models require no scaling, and scaling parameters will be fitted on training partitions only, never on the full dataset, to prevent information leakage.

**Data structures.** Two representations will be maintained: a long-format tidy table (one row per sample–parameter observation) for provenance and filtering, and a wide sample × species matrix for modelling.

### 6.3 Exploratory and micropalaeontological analysis

This stage characterises the data as a geological object before any model is fitted, and its findings determine several modelling decisions.

**Distributional structure.** Species abundance distributions will be examined for zero-inflation and right-skew, both of which are expected in assemblage data where most species are rare and a few dominate. The proportion of samples in which each species is reported will determine which taxa have sufficient coverage to serve as modelling targets.

**Missingness structure.** Missingness will be quantified per species, per sample and per site, and its pattern examined for systematic structure — in particular, whether the probability that a value is missing is related to the magnitude of that value. If rare taxa are systematically less often reported, real missingness is not missing at random in Rubin's (1976) sense, and this has direct consequences for how the masking experiment (Section 6.5) should be interpreted. This diagnosis will be made explicitly rather than assumed.

**Assemblage structure.** Correlation between species abundances, and between abundances and stratigraphic or geochemical parameters, will be examined, and ordination (principal component or correspondence analysis) used to identify the dominant assemblage gradients. This establishes whether the internal structure that reconstruction depends upon is in fact present and how strong it is. Diversity and dominance indices will be computed per sample as summary descriptors.

**Between-site comparability.** Assemblage composition will be compared between sites to assess how similar the training records are to one another. This is directly relevant to Objective 3: if the sites are compositionally near-identical, a site-level hold-out is a weaker test than it appears; if they differ substantially, cross-site transfer is a demanding test and results should be interpreted accordingly.

**Stratigraphic continuity.** Sample spacing, temporal resolution and the presence of hiatuses will be documented per record, since these govern how informative neighbouring samples are and therefore how strong an interpolation baseline can be expected to be.

### 6.4 Target and predictor variable preparation

**Target variables.** The primary targets are the relative abundances of planktonic foraminiferal species that are reported with sufficient coverage across multiple sites to permit training and evaluation. Where the harmonised dataset supports it, other compatible quantitative variables may also be treated as targets. Species with very sparse coverage will be excluded from the target set but retained as predictors, since they still carry assemblage information.

**Predictor variables.** For a given target, predictors will comprise: the abundances of the other species recorded in the same sample, which express assemblage context; stratigraphic variables (depth below sea floor, numerical age); site-level geographic variables (latitude, longitude, water depth); and, where available in the same record, stable isotope parameters, which are present in the datasets of Chaisson, Poli and Thunell (2002) and Bhaumik, Gupta and Thomas (2011). Where isotope data are not reported in the same table as the assemblage data, the feature set will be restricted to assemblage, stratigraphic and geographic variables rather than joined speculatively across records.

**Derived features.** A small number of interpretable sample-level descriptors will be derived: assemblage diversity, dominance, and the number of taxa reported. No ecological grouping of species beyond that supported by published sources will be imposed.

**Transformations.** Because relative abundances are proportions bounded between 0 and 1 and are typically right-skewed, a logit or arcsine-square-root transformation will be evaluated for the target variable, with predictions back-transformed before error metrics are computed so that errors are reported in the original units.

**Compositional constraint.** Relative abundances within a sample are subject to constant-sum closure (Aitchison, 1986). Predicting a single component independently can therefore yield a value that is individually plausible but inconsistent with the remainder of the assemblage. Two treatments will be compared: direct prediction with a post-hoc consistency check on the reconstructed sample total, and prediction in a log-ratio transformed space that respects the closure constraint. Whichever is adopted, the closure diagnostic will be reported alongside the standard error metrics.

**Site identity.** The site identifier will be used strictly as a grouping key for validation and never as a predictor, to prevent the model from learning site membership directly. Because latitude, longitude and water depth can encode site identity implicitly, two model variants will be trained — one including geographic predictors and one excluding them — and their relative transfer performance compared. This distinguishes a model that has learned assemblage structure from one that has learned where each core is.

### 6.5 Controlled missing-data experiment design

The core experimental design creates missing values whose true values are known, so that reconstruction error can be measured directly.

**Reference matrix.** A densely observed sub-matrix will be extracted from the harmonised dataset — samples and species with high reporting coverage — to serve as ground truth. All masking is applied to this complete reference, so that every prediction can be compared with an observed value.

**Primary scenario (MCAR).** Values will be withheld completely at random at four rates: 10 %, 20 %, 30 % and 40 %. Each rate will be repeated over multiple random seeds (of the order of twenty), and results reported as mean and standard deviation across repetitions, so that the reported degradation curve reflects a distribution rather than a single draw.

**Secondary scenarios.** Two additional masking regimes will be run at the same rates to test whether conclusions drawn under MCAR are robust to more realistic missingness. In the first, values are withheld with a probability that increases as abundance decreases, approximating the tendency of rare taxa to go unreported (an MNAR-like condition). In the second, contiguous stratigraphic intervals are masked as blocks, mimicking the way real gaps occur in cores and removing the assistance that immediately adjacent samples would otherwise provide. These scenarios are secondary to the primary MCAR design and are reported separately.

### 6.6 Model development

Four model families will be trained on identical inputs and evaluated under identical conditions, together with baselines that represent current practice.

**Baselines.** Two baselines establish the standard that a machine-learning model must beat to be worth adopting: (a) column mean or median substitution, and (b) linear interpolation along the depth or age axis within each core, which is the informal procedure most commonly used in practice. A model that fails to outperform stratigraphic interpolation has no practical claim, and reporting this comparison is essential to an honest benchmark.

**Statistical reference model.** Multiple linear regression provides a transparent, low-variance reference and indicates how much of the reconstruction problem is linear.

**Machine-learning models.**
- *Random forest* (Breiman, 2001): an ensemble of decision trees that captures non-linear relationships and interactions, is comparatively robust at small sample sizes, and yields variable-importance measures that support the interpretation stage.
- *Support vector regression* (Smola and Schölkopf, 2004): effective where the number of predictors approaches or exceeds the number of samples, as is typical of wide, short assemblage matrices; requires standardised inputs and careful tuning of the kernel, the regularisation parameter and the insensitivity margin.
- *XGBoost* (Chen and Guestrin, 2016): regularised gradient boosting, a consistently strong performer on tabular data and able to exploit weaker predictor–target relationships than a random forest of comparable size.

**Established imputation comparators.** Because the task is formally an imputation problem, iterative imputation methods will be included as comparators — chained-equations imputation (van Buuren and Groothuis-Oudshoorn, 2011) and random-forest imputation (Stekhoven and Bühlmann, 2012) — so that any advantage claimed for the supervised approach is measured against the established alternatives rather than only against naive baselines.

**Hyperparameter optimisation.** Hyperparameters will be selected by grid or randomised search using grouped cross-validation *within the training partition only*, with sites as groups. Search spaces will cover, for the random forest, the number of trees, maximum depth and minimum samples per leaf; for support vector regression, kernel choice and the regularisation and margin parameters; and for XGBoost, learning rate, tree depth, subsampling fraction and regularisation terms. Under no circumstances will the test partitions influence model or hyperparameter selection.

**Implementation.** The workflow will be implemented in Python using pandas, scikit-learn (Pedregosa *et al.*, 2011) and XGBoost, with fixed random seeds, pinned package versions and version-controlled scripts, so that every reported result can be regenerated from the published dataset.

### 6.7 Validation

Validation is the component that distinguishes this study from a conventional benchmarking exercise, and the partitions are therefore defined explicitly.

**Partition definitions.**
- **Training data** — samples used to fit model parameters.
- **Validation data** — samples used to select hyperparameters and make development decisions, drawn from the training pool using `GroupKFold` with site as the grouping variable, so that no site appears in both fitting and selection folds.
- **Test data** — samples used once, after development is frozen, to estimate generalisation. Three test regimes are applied.

**Test regime A — random hold-out.** Rows are withheld at random from the pooled training dataset. This reproduces standard practice and serves as the optimistic reference point, not as the headline result.

**Test regime B — site and basin hold-out.** Whole sites are withheld in a leave-one-site-out design, and where the compilation permits, whole basins. This is the scientifically meaningful test, because the intended application is a core the model has never seen.

**Test regime C — external test.** The supervisor-supplied Indian Ocean and Atlantic datasets, quarantined throughout development, are evaluated once. Repeating this evaluation after further tuning would convert it into a validation set and destroy its status as an unbiased estimate; it will therefore be run once, and the result reported whatever it shows.

**Why spatial independence matters.** Samples within a core are autocorrelated in depth and time, and share an analyst, a laboratory protocol, a size fraction and a single regional oceanographic setting. Under random splitting, a withheld sample almost always has near-neighbours from the same core in the training set, so the model can succeed by exploiting local continuity rather than any transferable relationship — an optimism that is well documented for spatially and temporally structured data (Roberts *et al.*, 2017). Grouped hold-out removes that assistance and measures what the model has actually learned about assemblage structure.

**Evaluation metrics.**

| Metric | Definition | What it captures |
|---|---|---|
| MAE | Mean absolute error between predicted and withheld values | Typical error magnitude, in original abundance units; robust to outliers |
| RMSE | Root mean squared error | Error magnitude with additional weight on large errors |
| R² | Proportion of variance in withheld values explained | Whether the model outperforms predicting the mean |
| Bias | Mean signed error | Systematic over- or under-prediction, invisible to MAE and RMSE |
| Skill score | Relative improvement in RMSE over the interpolation baseline | Whether the model beats current practice |

Metrics will be reported for each model, at each missingness rate, under each test regime, with dispersion across repetitions and folds. Errors will additionally be stratified by abundance class, since a low average error dominated by abundant species may conceal poor performance on rare taxa.

**The generalisation gap.** The difference in each metric between test regime A and test regimes B and C is the quantity that answers RQ3 and Objective 3, and it will be reported as a primary result rather than as a supplementary observation.

**Leakage control.** Train, validation and test separations are made at the site or dataset level throughout. All preprocessing steps that learn from data — scaling parameters, transformation parameters, feature selection, imputation of predictors — are fitted within training folds and applied to held-out data, never fitted on the pooled dataset.

### 6.8 Interpretation

Model output is treated as evidence to be interpreted, not as a result in itself.

**Feature importance and attribution.** Impurity-based and permutation importances will be computed for the tree-based models, supplemented by Shapley-value attribution (Lundberg and Lee, 2017) for individual predictions. The question asked of these results is geological: does the model rely on co-occurring species within the same assemblage, which would indicate that it has learned ecologically coherent structure, or on stratigraphic position and geographic coordinates, which would indicate that it has learned where and when each sample came from? The comparison between the geography-inclusive and geography-free model variants (Section 6.4) provides a direct test of this distinction.

**Error structure.** Errors will be analysed by species abundance class, by stratigraphic interval and by site. Reconstruction is expected to be least reliable for rare and low-abundance taxa, where the signal-to-noise ratio in the counted assemblage is lowest, and this expectation will be tested rather than assumed. Intervals with elevated error will be examined against documented features of the record — hiatuses, changes in sample spacing, preservation quality — so that error is explained rather than merely reported.

**Effect on downstream inference.** Because the problem statement asks whether reconstruction is accurate enough to be *scientifically usable*, error metrics alone are insufficient. Summary quantities of palaeoceanographic interest — assemblage diversity curves, dominant ordination axes, abundance time series of key taxa — will be computed from the complete reference record and again from the masked-and-reconstructed record, and compared. This determines whether reconstruction preserves the geological signal at the level at which it is actually interpreted.

**Uncertainty.** Prediction uncertainty will be characterised through the spread of ensemble predictions and through the distribution of errors across masking repetitions, and reported alongside every reconstructed value. Where the external test indicates poor transfer, this will be stated as a finding about the limits of the method rather than attributed to properties of the test data.

**Palaeoceanographic framing.** Results will be interpreted against the established understanding of assemblage–environment relationships summarised in Section 2.1, and against the characteristics of the source records, so that conclusions about where reconstruction succeeds are expressed in terms of the geology and not only in terms of the algorithm.

### 6.9 Final outputs

1. **A harmonised, documented, machine-learning-ready dataset** compiled from published PANGAEA records, released with the taxonomic and unit lookup tables and full provenance to each source DOI (Objective 1).
2. **A reproducible code repository** containing the harmonisation, masking, modelling and validation pipeline, with pinned dependencies and fixed seeds (Objectives 1–4).
3. **A comparative benchmark** presented as tables and degradation curves of MAE, RMSE and R² against missingness rate for each model and each test regime, identifying which algorithms are dependable on small-to-medium geological tabular data (Objective 2).
4. **A quantified generalisation assessment**, contrasting random hold-out with site- and basin-level validation and with the unseen external test, expressed as the generalisation gap for each model (Objectives 3 and 4).
5. **Reconstructed abundance series** for the study records, each accompanied by an uncertainty estimate and a flag distinguishing observed from reconstructed values.
6. **Practical recommendations**, stating the conditions — missingness rate, taxon abundance, degree of geographic extrapolation — under which reconstruction of legacy foraminiferal records can be considered scientifically usable, and the conditions under which it should not be attempted.
7. **A thesis** and a manuscript prepared for submission.

### 6.10 Scope conditions, assumptions and risk management

| Condition or risk | Consequence if unaddressed | Mitigation |
|---|---|---|
| Availability of supervisor-supplied external datasets | Objective 4 cannot be completed as specified | Substitute external test from site-level quarantined PANGAEA records; reduced geographic contrast reported explicitly (§6.1) |
| Small sample size per record | Unstable estimates, over-fitting | Repeated masking with multiple seeds; grouped cross-validation; preference for regularised and ensemble models; dispersion reported with every metric |
| Real missingness may be MNAR while masking is MCAR | Benchmark optimistic relative to real-world use | Abundance-dependent and block masking scenarios (§6.5); missingness mechanism diagnosed in EDA (§6.3) |
| Compositional closure of relative abundances | Internally inconsistent reconstructions | Log-ratio-space modelling and closure diagnostics (§6.4) |
| Subjectivity in taxonomic harmonisation | Non-reproducible dataset; hidden systematic error | Published lookup table, lumping-to-coarser-level rule, version control (§6.2) |
| Structural zeros conflated with missing values | Corrupted training targets and misleading metrics | Explicit missing-value semantics classification (§6.2) |

### 6.11 Expected outcomes and research significance

The expected outcome is a reproducible machine-learning workflow for reconstructing missing quantitative foraminiferal observations from published PANGAEA data, together with a comparative benchmark identifying which approaches are most reliable at this data scale, and a generalisation assessment stronger than random train–test splitting alone can provide. The contribution is intended to be dual: a practical data-analysis method that increases the usability of an existing open archive, and a geological assessment of where such reconstruction can be trusted and where uncertainty remains. It is emphasised that these are anticipated outcomes of the proposed work; no performance level is claimed in advance, and a finding that reconstruction does not transfer across basins would itself be a substantive and reportable result.

---

## 7. Timeline

The proposed programme runs over eight months, from August to March. Phases overlap where the work genuinely permits it: interpretation continues alongside the early stages of writing, and literature review is maintained at low intensity throughout rather than being closed after Month 2. The two most demanding phases — model development and the validation programme — are allocated the largest contiguous blocks, reflecting the fact that the masking experiment must be repeated across four missingness rates, multiple seeds, three masking regimes and several model families.

**Table 2 — Research schedule**

| Activity | Aug | Sep | Oct | Nov | Dec | Jan | Feb | Mar |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Literature review and topic finalisation | ■ | ■ | ▫ | ▫ | ▫ | ▫ | ▫ | ▫ |
| PANGAEA dataset search and download | ■ | ■ | | | | | | |
| Data cleaning and harmonisation | | ■ | ■ | ▫ | | | | |
| Exploratory analysis and missing-data masking | | | ■ | ■ | ▫ | | | |
| Machine-learning model development | | | | ■ | ■ | ■ | | |
| Validation and external test | | | | | ▫ | ■ | ■ | |
| Geological interpretation | | | | | | ▫ | ■ | ■ |
| Thesis writing and revision | | | ▫ | ▫ | ▫ | ▫ | ■ | ■ |

■ principal activity  ▫ secondary or continuing activity

**Table 3 — Phase milestones and deliverables**

| Phase | Months | Objective served | Milestone deliverable |
|---|---|---|---|
| I. Literature and data assembly | Aug – Sep | O1 | Documented search protocol; downloaded record set with provenance |
| II. Harmonisation and quality control | Sep – Nov | O1 | Harmonised ML-ready dataset and published taxonomic lookup table |
| III. Exploratory analysis and masking design | Oct – Dec | O1, O2 | EDA report; missingness diagnosis; validated masking framework |
| IV. Model development | Nov – Jan | O2 | Trained baseline, LR, RF, SVR and XGBoost models with tuning records |
| V. Validation programme | Dec – Feb | O2, O3, O4 | Benchmark tables; generalisation-gap results; single external test result |
| VI. Interpretation | Jan – Mar | O4 | Feature-importance and error analysis; downstream-inference comparison |
| VII. Writing and submission | Oct – Mar | All | Thesis draft, revision, final submission and defence |

The schedule assumes that the external test datasets become available no later than the start of Month 5 (December), since the external evaluation cannot begin until model development is complete and frozen. If they are delayed beyond that point, the contingency described in Section 6.1 will be invoked at that time rather than at the end of the programme, so that Objective 4 remains achievable within the eight-month period.

---

## 8. References

Aitchison, J. (1986) *The Statistical Analysis of Compositional Data*. London: Chapman and Hall.

Bhaumik, A.K., Gupta, A.K. and Thomas, E. (2011) 'Late Neogene benthic foraminifera and stable carbon isotope record of the Blake Outer Ridge', *PANGAEA*. Available at: https://doi.org/10.1594/PANGAEA.775833.

Breiman, L. (2001) 'Random forests', *Machine Learning*, 45(1), pp. 5–32.

Chaisson, W.P., Poli, M.-S. and Thunell, R.C. (2002) 'Stable isotope record and composition of planktonic foraminifera from ODP Site 172-1056', *PANGAEA*. Available at: https://doi.org/10.1594/PANGAEA.741050.

Chen, T. and Guestrin, C. (2016) 'XGBoost: a scalable tree boosting system', in *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*. New York: ACM, pp. 785–794.

Diepenbroek, M., Grobe, H., Reinke, M., Schindler, U., Schlitzer, R., Sieger, R. and Wefer, G. (2002) 'PANGAEA — an information system for environmental sciences', *Computers & Geosciences*, 28(10), pp. 1201–1212.

Hemleben, C., Spindler, M. and Anderson, O.R. (1989) *Modern Planktonic Foraminifera*. New York: Springer-Verlag.

Imbrie, J. and Kipp, N.G. (1971) 'A new micropaleontological method for quantitative paleoclimatology: application to a late Pleistocene Caribbean core', in Turekian, K.K. (ed.) *The Late Cenozoic Glacial Ages*. New Haven: Yale University Press, pp. 71–181.

Johansen, T.H. and Sørensen, S.A. (2020) 'Towards detection and classification of microscopic foraminifera using transfer learning', *arXiv preprint* arXiv:2001.04782.

Johansen, T.H., Sørensen, S.A., Møllersen, K. and Godtliebsen, F. (2021) 'Instance segmentation of microscopic foraminifera', *arXiv preprint* arXiv:2105.14191.

Karaderi, T. *et al.* (2021) 'Visual microfossil identification via deep metric learning', *arXiv preprint* arXiv:2112.09490.

Kučera, M. (2007) 'Planktonic foraminifera as tracers of past oceanic environments', in Hillaire-Marcel, C. and de Vernal, A. (eds.) *Proxies in Late Cenozoic Paleoceanography*. Developments in Marine Geology, vol. 1. Amsterdam: Elsevier, pp. 213–262.

Little, R.J.A. and Rubin, D.B. (2019) *Statistical Analysis with Missing Data*. 3rd edn. Hoboken, NJ: Wiley.

Lundberg, S.M. and Lee, S.-I. (2017) 'A unified approach to interpreting model predictions', in *Advances in Neural Information Processing Systems 30*, pp. 4765–4774.

Lutz, B.P. (2011) '(Appendix A5) Planktonic foraminifera of ODP Hole 172-1063A', *PANGAEA*. Available at: https://doi.org/10.1594/PANGAEA.774582.

Nishi, H., Norris, R.D. and Okada, H. (2000) 'Relative abundance of planktonic foraminifers in ODP Hole 164-997A sediments', *PANGAEA*. Available at: https://doi.org/10.1594/PANGAEA.804482.

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M. and Duchesnay, É. (2011) 'Scikit-learn: machine learning in Python', *Journal of Machine Learning Research*, 12, pp. 2825–2830.

Roberts, D.R., Bahn, V., Ciuti, S., Boyce, M.S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J.J., Schröder, B., Thuiller, W., Warton, D.I., Wintle, B.A., Hartig, F. and Dormann, C.F. (2017) 'Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure', *Ecography*, 40(8), pp. 913–929.

Rubin, D.B. (1976) 'Inference and missing data', *Biometrika*, 63(3), pp. 581–592.

Smola, A.J. and Schölkopf, B. (2004) 'A tutorial on support vector regression', *Statistics and Computing*, 14(3), pp. 199–222.

Stekhoven, D.J. and Bühlmann, P. (2012) 'MissForest — non-parametric missing value imputation for mixed-type data', *Bioinformatics*, 28(1), pp. 112–118.

van Buuren, S. and Groothuis-Oudshoorn, K. (2011) 'mice: multivariate imputation by chained equations in R', *Journal of Statistical Software*, 45(3), pp. 1–67.
