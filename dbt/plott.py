import matplotlib.pyplot as plt
import sys
import string
import numpy
from matplotlib.backends.backend_pdf import PdfPages
from itertools import chain
from matplotlib.patches import Polygon


#maxi = lambda v: max(enumerate(v), opeator.itemgetter(1))

SSTART = 1
NSSTART = 15
SEQ = "QKLVFFAEDVGSNKGAIIGLMVGGVVIATVIVITLVMLKKK"
NSEQ = [e[1]+str(e[0]) for e in enumerate(SEQ, NSSTART)]
SINON = 25.0 #SINO for 1 - i.e. not broaded
SINOC = 75.0 #SINO for 1 - i.e. not broaded

PERPAGE = 5


NCcorr = [1,2]

def kk(ss):
    s = ss[0]
    ai = s.split('-')[0]
    if ai[0] not in string.digits:
        ai = ai[1:]
    return int(ai)-2

def aa(ss):
    s = ss[0]
    ai = s.split('-')[1]
    ai = ai.split('/')[0]
    ai = ''.join([l for l in ai if not l.isdigit()])
    return ai

if len(sys.argv) != 2:
    print("Invalid cmd")
    sys.exit(0)

data = []

with open(sys.argv[1]) as f:
    for l in f.readlines():
        t = l.split()
        d = [t[0]]
        nss = map(float, t[1:])
        ns = nss
        #ns = map(lambda x: x[0]*x[1], zip(nss, NCcorr))
        d+= map(lambda x: x*1.0, ns)
        if d[0][-1] != 'N':
            d[1] = min(d[1]*2,0.920)
        data.append(d)


ORDER = {'H':0, 'HA':1, 'HB':2, 'HG':3, 'HD':4, 'HE':5}
AC = {'H':'black', 'HA':'r', 'HB':'b', 'HG':'g', 'HD':'y', 'HE':'y'}
AD = {'H': 0,  'HA':0.1, 'HB':0.2, 'HG':0.3, 'HD':0.4, 'HE':0.45}
GREEK = {'H':r'$H_N$', 'HA':r'$H_\alpha$', 'HB':r'$H_\beta$', 'HG':r'$H_\gamma$',
          'HD':r'$H_\delta$', 'HE':r'$H_\epsilon$'}
def aac(ss):
    a = aa(ss)
    return AC[a]

data.sort(key=kk)
data = [d for d in data if kk(d) != 2]
#data.sort(key = lambda x: x[0][1:])
#data = data[:5]
pp = PdfPages(sys.argv[1]+".pdf")

ylim = max(chain(*[d[1:] for d in data]))
fig = plt.figure(figsize=(8.3, 1./3*11.7))
ax = fig.add_subplot(111)
#fig, ax = plt.subplots()

def kkz(ss):
    t = kk(ss)
    t += AD[aa(ss)]
    return t

dd = zip(map(kk, data), map(lambda d: d[1], data))
#dd = sorted(dd,key = lambda x: x[1], reverse=True)
dd = zip(*dd)
#ax.bar(dd[0], dd[1])

#POLYGON
xx = zip(map(aa, data), map(kk, data), map(lambda d: d[1], data))
mx = []
mn = []

for i in range(SSTART, SSTART+len(SEQ)):
    l = [x[2] for x in xx if x[1] == i]
    if l:
        mx.append((i, max(l)))
    l = [x[2] for x in xx if x[1] == i]
    if l:
        mn.append((i, min(l)))
mn.reverse()
mm = mx+mn

pol = plt.Polygon(mm, closed = True, fill = True, color='grey', alpha=0.3)
ax.add_patch(pol)

#DOTS
err = [(2-s)/SINON if len(a) == 1 else (2-s)/SINOC for a,s in zip(map(aa, data), dd[1])]
ax.scatter(dd[0], dd[1], s=25, c=map(aac,data), lw=0)
ax.errorbar(dd[0], dd[1], yerr = err,  marker=None, fmt=None, ecolor='black')

#LEGENG
arts = []
labs = []
for n, c in sorted(AC.items(), key=lambda x: ORDER[x[0]]):
    arts.append(plt.Line2D((0,0), (0,0), color = c, marker='o', linestyle = ''))
    labs.append(GREEK[n])
    ax.legend(arts, labs, loc=4, prop={'size':10}, numpoints=1)
#for a, o in zip(map(aa, data), sl):
#    plt.setp(o, color=AC[a])



#ax.bar(map(kk, data), map(lambda d: d[1], data))
plt.ylim(0.0, 1.25)
plt.xlim(SSTART-0.5, SSTART+len(SEQ)+3)
ax.grid()
plt.xticks(0.0+ numpy.array(range(SSTART, SSTART + len(SEQ))))
ax.set_xticklabels(NSEQ, rotation=45, fontsize = 6)
plt.savefig("1.png", dpi=600)
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

