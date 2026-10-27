# GenAI architectural studio review: research data

Data accompanying **Design judgment in GenAI architectural studios: A critical scoping review of anticipatory visualization and premature finalization**.

**Author:** Gönenç Kurpınar, Department of Architecture, İzmir Institute of Technology, Türkiye.  
**Dataset version:** 1.0, 27 October 2026.  
**Repository:** https://github.com/gkurpinar/aiarchietcuralstudio  
**Contact:** gonenckurpinar@iyte.edu.tr

This package contains the frozen report-level data used in the current manuscript. It covers **59 reports**, **472 charting cells** (59 reports × eight fields), and **472 component assessments** (59 reports × C1–C8). The main analysis concerns architectural studio or workshop studies containing student data. Other background references are not counted as included reports.

## Start here

`review_data.xlsx` provides six filterable reading sheets: Charting, Strategies, Reports, Strategy evidence, Field definitions, and Strategy definitions. The CSV files retain normalized records and additional source and review information. The workbook is a frozen reading copy, not a live analysis model; edit the CSVs and rerun the script if conducting a new analysis.

CSV files use UTF-8 with a byte-order mark for Excel compatibility. Boolean values are `true` or `false`. Empty cells mean an optional value was not recorded, not zero or a negative finding. Multi-valued analytical fields use JSON arrays inside quoted CSV cells. The two wide reading tables use semicolon-separated labels.

## Files and units

| File | One row represents | Purpose |
|---|---|---|
| `data/reports.csv` | One included report (59) | Bibliography, public links, stable IDs and discovery group |
| `data/charting_wide.csv` | One report (59) | Readable view of the eight charting fields |
| `data/charting_cells.csv` | One report × charting field (472) | Coverage, missingness and links to assessments |
| `data/charting_assignments.csv` | One saved report–field–value assignment (1,332) | Substantive categories and original reporting markers |
| `data/components_wide.csv` | One report (59) | Readable C1–C8 status overview |
| `data/component_assessments.csv` | One report × component (472) | Use, linked outcomes, evidence types, rationale, limitations and locations |
| `data/review_provenance.csv` | One original assessment proposal (1,805) | Earlier approval, current decisions and origin metadata |
| `data/source_locations.csv` | One recorded evidence pointer (3,167) | Source IDs and page, line or offset locations |
| `data/sources.csv` | One preserved PDF or text source (164) | Source types and hashes; multiple versions may belong to one report |
| `data/claim_evidence_metadata.csv` | One claimed-benefit or claimed-risk assignment | Epistemic classification where recorded, with specific audit qualifications |
| `data/report_analysis_membership.csv` | One report (59) | Eligibility for complete-field benefit/risk comparisons |
| `schema/` | Field, component, category or column definition | Terminology, joins and input hashes |
| `search/` | Search event or selection-flow item | Exact saved queries, search provenance and Figure 1 counts |
| `analysis/` | Descriptive comparison | Frozen benefit-risk, risk-component and selected triple tables |
| `analysis/reproduced/` | Summary generated from the public CSVs | Coverage, categories, C1–C8, evidence types, pairs, activities and years |

Join report-level tables on `report_id`. Join assessment details to evidence pointers and approval metadata on `proposal_id`. Join a pointer to its preserved-source metadata on `source_id` or `pdf_source_id`. Source files are not included; page locators and public bibliography links allow readers with access to consult the publications. A pointer can be repeated across assignments, so pointers are not independent observations.

## Charting and terminology

The current manuscript uses CH1 AI tool, CH2 Design stage, CH3 Output type, CH4 Claimed benefit, CH5 Claimed risk, CH6 Student role, CH7 Instructor role, and CH8 AI modality. Internal field IDs are retained for traceability. In particular, internal **CH013** was previously displayed as **CH9** and is now displayed as **CH8**. This is a display change, not an additional field. The previously removed education-context field is not reinstated.

`PREMATURE_PRODUCTIZATION` is a legacy category key. Its current public label is **Premature finalization**. Do not treat these as two categories. Counts are unique-report counts, not sums of `stored_weight`; that field is preserved only as source metadata.

The recorded statuses `NOT_CHARTED`, `NOT_MENTIONED`, `NOT_SPECIFIED`, `NOT_DISCUSSSED` and an empty cell are preserved separately. They are not interchangeable evidence that a phenomenon was absent. `NOT_CHARTED` does not establish that the original publication lacked the information. Substantive values determine the descriptive category counts. P057's risk field contains both `AUTHORSHIP_AMBIGUITY` and `NOT_MENTIONED`; its authorship value is retained and the conflict is flagged.

## Components and evidence

The qualifying rules for C1–C8 appear in `schema/components.csv` and in the workbook. Each report–component cell has one of four statuses:

| Stored status | Meaning |
|---|---|
| `implemented_with_benefit` | The activity was used and a component-linked favorable consequence was reported |
| `implemented_without_benefit` | The activity was used, but a component-linked favorable consequence was not established; this is not evidence of ineffectiveness |
| `recommended_only` | The activity was proposed without qualifying implementation in the reviewed account |
| `not_identified` | No qualifying activity was identified under the component definition; this is not proof of absence |

Outcome valence is recorded separately as positive, mixed, negative, null, or not evaluated. There are 113 cells with a linked favorable consequence, including 72 positive-only and 41 mixed cells. Across all 472 cells there are also eight negative, one null and 350 not-evaluated classifications. Mixed outcomes remain visible.

Evidence types can overlap. The component evidence includes 98 cells associated with process/artifact observations, 35 with participant perceptions, and three with comparative outcomes. These correspond to **39, 14 and three distinct reports**, respectively. A linked benefit is not an isolated causal effect of the strategy. The existence of a diary, critique or representation is not itself evidence of improved agency.

## Denominators and interpretation

Whole-corpus percentages use **59 reports**. Benefits and risks may be multi-valued, so category percentages need not total 100%. Reports with substantive entries in CH1–CH8 number **59, 58, 58, 59, 54, 57, 51 and 55**, respectively.

The retained benefit-risk and risk-component comparisons use **54 reports** with eligible risk information. P072, P207, P231, P235 and U072 are excluded from those comparisons. A conditional percentage such as `percent_y_given_x` is `100 × joint_n / x_n`. It describes reporting patterns, not participant prevalence, the probability of experiencing a risk, or the effectiveness of mitigation. Counts of reports do not guarantee independent student cohorts; related programme/cohort publications remain distinct reports.

Premature-finalization classifications concern source-stated risks and interpretations. The four-report risk set includes a less-direct warning in P070, identified in its audit metadata. It must not be represented as four observed premature-finalization episodes. Benefits, risks and component presence in the same report do not establish a causal sequence. The selected triples were specified within a retrospective exploratory analysis; the filename does not imply preregistration. No inferential tests are included in this package.

## Review provenance and limitations

The exported classifications include AI-origin analytical proposals and earlier author bulk acceptance. The current decision snapshot contains 20 accepted charting proposals; this is a distinct record from prior approvals and does not imply individual rereading of all 1,805 proposals. Of the 472 component records, 360 retain earlier bulk-acceptance metadata and 112 do not contain that prior-approval metadata. The absence of a current decision does not erase an earlier acceptance. Original proposal status, prior approval and current decision are therefore separate columns.

Text-match verification means a saved passage was matched to a source; it does not establish semantic support or independent human confirmation. Blank attestation fields mean no explicit attestation was stored. The export preserves these boundaries rather than upgrading the evidence status.

Bibliographic presentation follows the current manuscript. No new complete DOI audit was performed for this export. For P051, an older stored DOI conflicts with the current hosted-preprint reference. Its DOI is left blank, its current public link is retained, and the issue is recorded in `metadata_note`.

## Reproduce the tables

With Python 3.9 or later, run:

```sh
python scripts/reproduce_tables.py
```

No additional packages or source PDFs are needed. The script reconstructs the descriptive tables from the public CSVs and checks all 405 retained benefit-risk and risk-component matrix cells. It writes `analysis/reproduced/validation.json`. It does not modify the primary data, run statistical inference, or reclassify any source.

`manifest_sha256.csv` identifies the files in this release. `schema/input_hashes.csv` records the frozen internal export inputs by filename and hash, without distributing those private working files. Search input hashes are documented separately in `search/`.

## Access, citation and rights

Use `CITATION.cff` for author and version information. The repository is available at https://github.com/gkurpinar/aiarchietcuralstudio. No dataset DOI has been assigned. Copyrighted source PDFs, full-text extracts, raw Scopus exports, institutional-session links and local computer paths are excluded. See `LICENSE_NOTICE.md` for rights status.
