import numpy as np, wave
sr=44100; dur=34; n=sr*dur; t=np.arange(n)/sr
out=np.zeros(n)
bpm=100; beat=60/bpm
def note(f): return 440*2**((f-69)/12)
chords=[[60,64,67,72],[55,59,62,67],[57,60,64,69],[53,57,60,65]]  # C G Am F
bar=beat*4
for i in range(int(dur/bar)+1):
    s=int(i*bar*sr); e=min(n,int((i+1)*bar*sr)+sr//4)
    if s>=n: break
    tt=np.arange(e-s)/sr; env=np.minimum(1,tt/0.4)*np.exp(-tt*0.25)
    for m in chords[i%4]:
        f=note(m); out[s:e]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt)+0.15*np.sin(2*np.pi*f*1.003*tt))
    f=note(chords[i%4][0]-24)
    out[s:e]+=0.12*env*np.sin(2*np.pi*f*tt)
    # arpeggio
    for k in range(8):
        a=int((i*bar+k*beat/2)*sr)
        if a>=n: break
        L=min(int(0.35*sr),n-a); ta=np.arange(L)/sr
        f=note(chords[i%4][k%4]+12)
        out[a:a+L]+=0.04*np.exp(-ta*9)*np.sin(2*np.pi*f*ta)
rng=np.random.default_rng(1)
for k in range(int(dur/beat)):
    a=int(k*beat*sr)
    if a<sr*1.5: continue
    L=int(0.25*sr); ta=np.arange(L)/sr; L=min(L,n-a); ta=ta[:L]
    out[a:a+L]+=0.35*np.exp(-ta*18)*np.sin(2*np.pi*(50+90*np.exp(-ta*30))*ta)
    h=int(a+beat/2*sr); Lh=min(int(0.05*sr),n-h)
    if Lh>0: out[h:h+Lh]+=0.03*rng.standard_normal(Lh)*np.exp(-np.arange(Lh)/sr*80)
def whoosh(at,a=0.25):
    s=int((at-0.5)*sr); L=int(0.9*sr); x=rng.standard_normal(L)
    x=np.convolve(x,np.ones(30)/30,'same'); env=np.sin(np.pi*np.arange(L)/L)**2
    out[s:s+L]+=a*x*env*4
def boom(at,a=0.6):
    s=int(at*sr); L=int(1.2*sr); ta=np.arange(L)/sr
    out[s:s+L]+=a*np.exp(-ta*4)*np.sin(2*np.pi*(45+60*np.exp(-ta*8))*ta)
    out[s:s+L]+=0.08*np.exp(-ta*3)*np.sin(2*np.pi*1568*ta)
for at in [5,11,16.5,23,28.5]: whoosh(at)
for at in [0.7,8.25,20.85,30.2]: boom(at)
fade=np.ones(n); fe=int(2*sr); fade[-fe:]=np.linspace(1,0,fe)
out*=fade; out/=np.max(np.abs(out))*1.15
d=(out*32767).astype(np.int16)
w=wave.open('music.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(d.tobytes()); w.close()
