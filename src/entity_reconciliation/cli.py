import argparse
from pathlib import Path
import pandas as pd
from .matcher import reconcile

def main():
    p=argparse.ArgumentParser(); p.add_argument('--master',required=True); p.add_argument('--input',required=True); p.add_argument('--output',required=True); p.add_argument('--exceptions',required=True); p.add_argument('--threshold',type=float,default=88); p.add_argument('--margin',type=float,default=5)
    a=p.parse_args(); master=pd.read_csv(a.master).fillna('').to_dict('records'); rows=pd.read_csv(a.input).fillna('').to_dict('records')
    result=pd.DataFrame(reconcile(rows,master,a.threshold,a.margin)); Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.exceptions).parent.mkdir(parents=True,exist_ok=True)
    result.to_csv(a.output,index=False); result[result.status!='MATCHED'].to_csv(a.exceptions,index=False); print(f'Processed {len(result)} rows; matched={(result.status=="MATCHED").sum()}; exceptions={(result.status!="MATCHED").sum()}')

if __name__ == "__main__": main()
