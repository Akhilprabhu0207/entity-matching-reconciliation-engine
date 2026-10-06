from entity_reconciliation.matcher import match_row
MASTER=[{'master_id':'1','name':'Vanguard S&P 500 ETF','isin':'US9229083632','cusip':'922908363'},{'master_id':'2','name':'Microsoft Corporation','isin':'US5949181045','cusip':'594918104'}]
def test_isin_is_deterministic():
    r=match_row({'name':'anything','isin':'US9229083632'},MASTER)
    assert r.status=='MATCHED' and r.method=='ISIN' and r.score==100
def test_fuzzy_match():
    r=match_row({'name':'Microsft Corp'},MASTER)
    assert r.status=='MATCHED' and r.method=='NAME_FUZZY'
def test_unknown_is_exception():
    r=match_row({'name':'ZZZZZZZZZZ'},MASTER)
    assert r.status in {'REVIEW','UNMATCHED'}
def test_duplicate_identifier_review():
    m=MASTER+[{'master_id':'3','name':'Duplicate','isin':'US9229083632','cusip':''}]
    assert match_row({'name':'x','isin':'US9229083632'},m).status=='REVIEW'
