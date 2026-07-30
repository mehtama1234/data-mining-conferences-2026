import json, os, glob, re
HERE=os.path.dirname(os.path.abspath(__file__))
dw={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out6","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and a.get("deep_why"): dw[str(g)]=a["deep_why"]
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
subs=[(r'\bembeddings?\b','numeric fingerprints'),(r'\bvectors?\b','lists of numbers'),(r'\bgradients?\b','the downhill direction'),
 (r'\btokens?\b','words'),(r'\badapters?\b','small add-on modules'),(r'\blow[- ]rank\b','compact'),(r'\bdimensions?\b','features'),
 (r'\battention (patterns?|mechanisms?|weights?)\b','focus'),(r'\battention\b','focus'),(r'\bfrozen\b','fixed'),(r'\bfine[- ]?tun\w*\b','adjust'),
 (r'\bhyper[- ]?parameters?\b','settings'),(r'\blogits?\b','raw scores'),(r'\bkernels?\b','similarity function'),(r'\bmanifolds?\b','surface'),
 (r'\bregulari[sz]\w*\b','keeping it simple'),(r'\bposteriors?\b','updated chance'),(r'\bpriors?\b','starting guess'),(r'\bstochastic\b','random'),
 (r'\bconvex\b','bowl-shaped'),(r'\bnon-convex\b','rugged'),(r'\btensors?\b','number grids'),(r'\bLLMs?\b','AI language systems'),
 (r'\blarge language models?\b','AI language systems'),(r'\bneural networks?\b','systems that learn from examples'),(r'\bentropy\b','how much surprise'),
 (r'\bsoftmax\b','share-of-total weighting'),(r'\btransformers?\b','learned language systems'),(r'\blatent\b','hidden'),(r'\bmatrix\b','grid of numbers'),(r'\bvariance\b','spread of error')]
n=0
for k in dw:
    for pat,rep in subs:
        t=re.sub(pat,rep,dw[k],flags=re.I)
        if t!=dw[k]: n+=1; dw[k]=t
json.dump(dw, open(os.path.join(HERE,"data","deepwhy.json"),"w"), indent=1)
al=' '.join(dw.values())
banned=['embedding','vector','tensor','gradient','matrix','token','adapter','low-rank','attention','logit','manifold','eigen','softmax','entropy','regulariz','hyperparameter','frozen','fine-tun','posterior','stochastic','convex','latent','neural network',' llm','kernel','variance']
resid={b:len(re.findall(r'\b'+b+r'\b',al,re.I)) for b in banned if re.search(r'\b'+b+r'\b',al,re.I)}
wc=sum(len(v.split()) for v in dw.values())//max(len(dw),1)
print(f"deepwhy {len(dw)} papers, cleaned {n}, avg {wc} words, bad {bad}, residual {resid or 'CLEAN'}")
