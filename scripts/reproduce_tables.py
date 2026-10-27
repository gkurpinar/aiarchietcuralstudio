"""Reproduce report-level descriptive tables. Python 3.9+, standard library only.

Run from any directory: python scripts/reproduce_tables.py
This script reads the CSV tables and writes summaries under analysis/reproduced/.
It checks the retained benefit-risk and risk-component matrices without running
inferential tests or changing classifications. No source PDF is required.
"""
from pathlib import Path
import csv
import json
import math
from collections import Counter, defaultdict
from itertools import combinations

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'analysis/reproduced'
OUT.mkdir(exist_ok=True)
def read(name):
    with (ROOT / name).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))
def write(name, rows):
    with (OUT/name).open('w', encoding='utf-8-sig', newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def pct(n,d):
    return 100*n/d if d else None

reports=read('data/reports.csv'); universe={r['report_id'] for r in reports}; N=len(universe)
assert N==len(reports)==59
cells=read('data/charting_cells.csv')
assessments=read('data/component_assessments.csv')
assert len(cells)==len(assessments)==472
assert len({(r['report_id'],r['source_field_id']) for r in cells})==472
assert len({(r['report_id'],r['component_id']) for r in assessments})==472
fields=read('schema/charting_fields.csv'); categories=read('schema/categories.csv')
field_names={r['source_field_id']:r for r in fields}
cnames={r['component_id']:r['component_name'] for r in read('schema/components.csv')}
sets=defaultdict(set)
for r in read('data/charting_assignments.csv'):
    assert r['report_id'] in universe
    if r['is_substantive']=='true':
        sets[(r['source_field_id'],r['category_key'])].add(r['report_id'])
summary=[]
for r in categories:
    if r['is_sentinel']=='true': continue
    ids=sets[(r['source_field_id'],r['category_key'])]
    summary.append(dict(manuscript_field_code=r['manuscript_field_code'],source_field_id=r['source_field_id'],
        category_key=r['category_key'],category_label=r['category_label'],report_count=len(ids),
        corpus_denominator=N,percent_of_reports=pct(len(ids),N),report_ids=json.dumps(sorted(ids))))
write('charting_summary.csv',summary)
coverage=[]
for f in fields:
    ids=set().union(*(v for (fid,key),v in sets.items() if fid==f['source_field_id']))
    coverage.append(dict(manuscript_field_code=f['manuscript_field_code'],field_name=f['field_name'],
        reports_with_substantive_entries=len(ids),total_reports=N,percent_of_reports=pct(len(ids),N)))
write('field_coverage.csv',coverage)
assert [r['reports_with_substantive_entries'] for r in coverage]==[59,58,58,59,54,57,51,55]

statuses=['implemented_with_benefit','implemented_without_benefit','recommended_only','not_identified']
valences=['positive','mixed','negative','null','not_evaluated']
used=defaultdict(set)
component_rows=[]
for cid in cnames:
    rows=[r for r in assessments if r['component_id']==cid]
    assert len(rows)==N
    sc=Counter(r['status'] for r in rows); vc=Counter(r['outcome_valence'] for r in rows)
    used[cid]={r['report_id'] for r in rows if r['implemented']=='true'}
    assert len(used[cid])==sc[statuses[0]]+sc[statuses[1]]
    out=dict(component_id=cid,component_name=cnames[cid],total_reports=N,implemented_n=len(used[cid]),
        implemented_percent=pct(len(used[cid]),N))
    for k in statuses+valences:
        n=sc[k] if k in statuses else vc[k]
        out[k+'_n']=n; out[k+'_percent']=pct(n,N)
    component_rows.append(out)
write('component_summary.csv',component_rows)
assert sum(r['implemented_with_benefit_n'] for r in component_rows)==113
assert sum(r['implemented_n'] for r in component_rows)==265
types=defaultdict(list)
for r in assessments:
    for t in json.loads(r['benefit_evidence_types']): types[t].append(r)
evidence=[]
for t,rows in sorted(types.items()):
    ids={r['report_id'] for r in rows}
    evidence.append(dict(evidence_type=t,component_cells_n=len(rows),distinct_reports_n=len(ids),
        report_denominator=N,report_percent=pct(len(ids),N),report_ids=json.dumps(sorted(ids)),
        note='Types overlap; component cells and distinct reports are different counting units.'))
write('component_evidence_counts.csv',evidence)
pairs=[]
for a,b in combinations(cnames,2):
    joint=used[a]&used[b]; union=used[a]|used[b]
    pairs.append(dict(component_a=a,component_b=b,a_n=len(used[a]),b_n=len(used[b]),joint_n=len(joint),
        corpus_denominator=N,joint_percent=pct(len(joint),N),jaccard=len(joint)/len(union) if union else None,
        joint_report_ids=json.dumps(sorted(joint))))
write('component_pairs.csv',pairs)
activities=[]
for c in categories:
    if c['source_field_id']!='CH003' or c['is_sentinel']=='true': continue
    ids=sets[('CH003',c['category_key'])]
    for cid in cnames:
        joint=ids&used[cid]
        activities.append(dict(activity_key=c['category_key'],activity_label=c['category_label'],component_id=cid,
            activity_reports_n=len(ids),joint_n=len(joint),percent_of_activity_reports=pct(len(joint),len(ids)),
            joint_report_ids=json.dumps(sorted(joint))))
write('activity_component.csv',activities)
years=Counter(int(r['year']) for r in reports)
write('report_years.csv',[dict(year=k,report_count=v,percent_of_reports=pct(v,N)) for k,v in sorted(years.items())])
assert dict(years)=={2022:3,2023:2,2024:8,2025:16,2026:30}

members=read('data/report_analysis_membership.csv')
eligible={r['report_id'] for r in members if r['benefit_field_eligible']=='true' and r['risk_field_eligible']=='true'}
assert len(eligible)==54
checks=0
def check_matrix(path,mode):
    global checks
    for row in read(path):
        if mode=='benefit_risk':
            x=sets[('CH005',row['benefit_key'])]&eligible; y=sets[('CH006',row['risk_key'])]&eligible
        else:
            x=sets[('CH006',row['risk_key'])]&eligible; y=used[row['component_id']]&eligible
        joint=x&y
        assert int(row['eligible_N'])==len(eligible)
        assert int(row['x_n'])==len(x) and int(row['y_n'])==len(y) and int(row['joint_n'])==len(joint)
        assert set(json.loads(row['joint_report_ids']))==joint
        for key, expected in [('percent_y_given_x',pct(len(joint),len(x))),('percent_x_given_y',pct(len(joint),len(y))),
            ('joint_percent_eligible',pct(len(joint),len(eligible))),('lift',len(joint)*len(eligible)/(len(x)*len(y)) if x and y else None)]:
            assert (row[key]=='' and expected is None) or (expected is not None and math.isclose(float(row[key]),expected,rel_tol=1e-12,abs_tol=1e-12)),(path,key,row)
        checks+=1
check_matrix('analysis/benefit_risk_matrix.csv','benefit_risk')
check_matrix('analysis/risk_component_matrix.csv','risk_component')
assert checks==405
result=dict(status='passed',reports=N,charting_cells=len(cells),component_assessments=len(assessments),
    risk_analysis_reports=len(eligible),retained_matrix_cells_recomputed=checks,
    interpretation='Descriptive report-level presence and linked evidence; no student-level effect or causal efficacy estimate.')
(OUT/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
