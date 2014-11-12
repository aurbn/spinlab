import matplotlib.pyplot as plt
import sys
import string
from matplotlib.backends.backend_pdf import PdfPages
from itertools import chain

SEQ = "GSQKLVFFAEDVGSNKGAIIGLMVGGVVIATVIVITLVMLKKK"
NSEQ = [e[1]+str(e[0]) for e in enumerate(SEQ, 1)]

PERPAGE = 5
NCcorr = [1, 2 ]



def kk(ss):
    s = ss[0]
    ai = s.split('-')[0]
    if ai[0] not in string.digits:
        ai = ai[1:]
    return int(ai)

if len(sys.argv) != 2:
    print("Invalid cmd")
    sys.exit(0)

data = []
with open(sys.argv[1]) as f:
    for l in f.readlines():
        t = l.split()
        d = [t[0]]
        nss = map(float, t[1:])
        ns = map(lambda x: x[0]*x[1], zip(nss, NCcorr))
        d+= map(lambda x: x*1.0/ns[0], ns)
        data.append(d)

data.sort(key=kk)
#data.sort(key = lambda x: x[0][1:])
#data = data[:5]
pp = PdfPages(sys.argv[1]+".pdf")

ylim = max(chain(*[d[1:] for d in data]))
fig = plt.figure(figsize=(8.3, 1./3*11.7))
ax = fig.add_subplot(111)
ax.bar(map(kk, data), map(lambda d: d[2], data))
plt.ylim(0.0, 1.3)
ax.grid()
plt.xticks(range(1,len(SEQ)+ 1))
ax.set_xticklabels(NSEQ, rotation=45, fontsize = 6)
pp.savefig(fig)

pp.close()
sys.exit(0)
#fig = plt.figure(figsize=(8.3, len(data)*11.7/7))
for i, d in enumerate(data):
    if i%PERPAGE == 0 :
        fig = plt.figure(figsize=(8.3, 1*11.7))
    plt.subplot(PERPAGE, 1, i%PERPAGE+1)
    plt.text(2.5, 0.9, d[0])
    plt.grid(True)
    plt.plot(d[1:], "o-")
    plt.ylim(0,ylim)
    if i%PERPAGE == PERPAGE-1:
        pp.savefig(fig)

#fig.savefig(sys.argv[1]+".pdf")
pp.close()
#plt.show()

