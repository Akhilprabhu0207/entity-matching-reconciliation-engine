from dataclasses import dataclass
from rapidfuzz import fuzz, process
from .normalize import normalize_id, normalize_text

@dataclass(frozen=True)
class MatchResult:
    source_name: str
    matched_name: str | None
    master_id: str | None
    method: str
    score: float
    runner_up_score: float
    status: str
    reason: str

def match_row(row: dict, master: list[dict], threshold: float=88.0, margin: float=5.0) -> MatchResult:
    src_name=row.get('name',''); src_isin=normalize_id(row.get('isin')); src_cusip=normalize_id(row.get('cusip'))
    if src_isin:
        hits=[m for m in master if normalize_id(m.get('isin'))==src_isin]
        if len(hits)==1:
            m=hits[0]; return MatchResult(src_name,m['name'],m['master_id'],'ISIN',100,0,'MATCHED','exact_isin')
        if len(hits)>1: return MatchResult(src_name,None,None,'ISIN',100,100,'REVIEW','duplicate_isin_in_master')
    if src_cusip:
        hits=[m for m in master if normalize_id(m.get('cusip'))==src_cusip]
        if len(hits)==1:
            m=hits[0]; return MatchResult(src_name,m['name'],m['master_id'],'CUSIP',100,0,'MATCHED','exact_cusip')
        if len(hits)>1: return MatchResult(src_name,None,None,'CUSIP',100,100,'REVIEW','duplicate_cusip_in_master')
    names=[normalize_text(m['name']) for m in master]; query=normalize_text(src_name)
    candidates=process.extract(query,names,scorer=fuzz.WRatio,limit=2)
    if not candidates: return MatchResult(src_name,None,None,'NONE',0,0,'UNMATCHED','empty_master')
    best_name,best_score,best_idx=candidates[0]; runner=candidates[1][1] if len(candidates)>1 else 0; m=master[best_idx]
    if best_score>=threshold and best_score-runner>=margin:
        return MatchResult(src_name,m['name'],m['master_id'],'NAME_FUZZY',float(best_score),float(runner),'MATCHED','name_above_threshold')
    return MatchResult(src_name,None,None,'NAME_FUZZY',float(best_score),float(runner),'REVIEW' if best_score>=threshold else 'UNMATCHED','ambiguous_or_low_confidence')

def reconcile(rows, master, threshold=88.0, margin=5.0):
    return [match_row(r,master,threshold,margin).__dict__ for r in rows]
