import json, os, glob, re
HERE=os.path.dirname(os.path.abspath(__file__))
math={}; why={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out5","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and a.get("math_plain"):
                math[str(g)]={"tags":a.get("math_tags") or [], "plain":a["math_plain"]}
                if a.get("why_math"): why[str(g)]=a["why_math"]
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
# de-jargon cleanup on plain + why
subs=[(r'\bembeddings?\b','numeric fingerprints'),(r'\bvectors?\b','lists of numbers'),(r'\bgradients?\b','slope'),
      (r'\bLLMs?\b','AI language systems'),(r'\blarge language models?\b','AI language systems'),(r'\bneural networks?\b','systems that learn from examples'),
      (r'\bentropy\b','how much surprise'),(r'\bsoftmax\b','share-of-total weighting'),(r'\btransformers?\b','learned language systems'),
      (r'\blatent\b','hidden'),(r'\bmatrix\b','grid of numbers'),(r'\bvariance\b','spread of error'),(r'\bconvex\b','bowl-shaped')]
n=0
for d in (math,why):
    for k in list(d):
        v=d[k]; s=v["plain"] if isinstance(v,dict) else v
        keys=('plain',) if isinstance(v,dict) else (None,)
        if isinstance(v,dict):
            for pat,rep in subs:
                t=re.sub(pat,rep,v["plain"],flags=re.I)
                if t!=v["plain"]: n+=1; v["plain"]=t
        else:
            for pat,rep in subs:
                t=re.sub(pat,rep,d[k],flags=re.I)
                if t!=d[k]: n+=1; d[k]=t
json.dump(math, open(os.path.join(HERE,"data","math.json"),"w"), indent=1)
json.dump(why, open(os.path.join(HERE,"data","whymath.json"),"w"), indent=1)
from collections import Counter
tc=Counter(t for v in math.values() for t in v["tags"])
al=' '.join(list((v['plain'] for v in math.values()))+list(why.values()))
resid=[w for w in ['embedding','vector','gradient',' llm','neural network','entropy','softmax','transformer','matrix','tensor'] if re.search(r'\b'+w+r'\b',al,re.I)]
print(f"math {len(math)}, why {len(why)}, cleaned {n}, bad {bad}, residual {resid or 'CLEAN'}")
print("=== math-idea frequency ===")
for t,cn in tc.most_common(): print(f"  {cn:>4}  {t}")
