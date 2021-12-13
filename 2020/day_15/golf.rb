n=$<.read.split(',').map &:to_i
z,e,y,d=2019,3*10**7,n[-1],{}
(0..5).each{|i|d[n[i]]=i+1}
(7...e).each{|t|d[y],y=t,t-d.fetch(y,t);z=y if t==z}
p z,y
