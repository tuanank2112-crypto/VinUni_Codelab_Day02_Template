"""Evaluate authored fixture extraction, NOT Gemini quality, using pairwise metrics."""
import itertools
import json
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'starter-code'))
from incident_engine import propose_groups

data = json.loads((root / 'data/scenario.json').read_text())
truth = {t['id']: t['synthetic_cause'] for t in json.loads((root / 'data/ground-truth.json').read_text())}
output = propose_groups(data['tickets'], data['topology'], data['fixture_extractions'])
predicted = {tuple(sorted(pair)) for g in output['groups'] for pair in itertools.combinations(g['ticket_ids'], 2)}
positive = {pair for pair in itertools.combinations(sorted(truth), 2) if truth[pair[0]] == truth[pair[1]]}
tp, fp, fn = len(predicted & positive), len(predicted - positive), len(positive - predicted)
result = {'mode': 'offline_fixture_not_llm', 'ticket_count': len(truth),
          'tp': tp, 'fp': fp, 'fn': fn, 'precision': tp/(tp+fp) if tp+fp else None,
          'recall': tp/(tp+fn) if tp+fn else None,
          'false_positive_pairs': sorted(predicted - positive),
          'missed_pairs': sorted(positive - predicted),
          'note': 'Manual/urgent tickets count as ungrouped; labels never provided to grouping engine.'}
(root / 'results/group-evaluation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
