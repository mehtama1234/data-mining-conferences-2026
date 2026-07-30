import json, os, glob, re
HERE=os.path.dirname(os.path.abspath(__file__))
plain={}; bad=[]
for f in sorted(glob.glob(os.path.join(HERE,"data","out2","b*.json"))):
    try:
        for a in json.load(open(f)):
            g=a.get("gid")
            if isinstance(g,int) and a.get("plain_problem"):
                plain[str(g)]={"p":a["plain_problem"],"a":a.get("plain_approach","")}
    except Exception as e: bad.append((os.path.basename(f),str(e)[:40]))
# safe de-jargon cleanup for residual leaks
subs=[(r'\bembeddings?\b','numeric fingerprints'),(r'\bLLMs?\b','AI language systems'),
      (r'\blarge language models?\b','AI language systems'),(r'\bRAG\b','look-it-up-first answering'),
      (r'\bGNNs?\b','connection-learning systems'),(r'\bgraph neural networks?\b','connection-learning systems'),
      (r'\bcontrastive\b','learn-by-comparison'),(r'\btransformers?\b','learned language systems'),
      (r'\bmultimodal\b','text-and-image'),(r'\bfederated\b','privacy-preserving')]
n=0
for g,v in plain.items():
    for key in ('p','a'):
        t=v[key]
        for pat,rep in subs:
            t2=re.sub(pat,rep,t,flags=re.I)
            if t2!=t: n+=1; t=t2
        v[key]=t
json.dump(plain, open(os.path.join(HERE,"data","plain.json"),"w"), indent=1)
badw=['embedding','tensor','gradient','latent','diffusion','transformer','contrastive','gnn','self-supervised','rag',' llm','multimodal','federated','retrieval-augmented']
al=' '.join((v['p']+' '+v['a']).lower() for v in plain.values())
print(f"plain: {len(plain)} papers, cleaned {n} spots, bad {bad}")
print("residual jargon:", {b:al.count(b) for b in badw if b in al} or "CLEAN")
