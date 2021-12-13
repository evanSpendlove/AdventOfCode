def m(n,e):
    y,d=n[-1],{n[i]:i+1 for i in range(len(n)-1)}
    for t in range(len(n), e): d[y],y = t,t-d.get(y, t)
    return y
l=[0,1,4,13,15,12,16];print(m(l,2020),m(l,3*10**7))
