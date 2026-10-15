from heapq import*
n,m=map(int,input().split());a=list(map(int,input().split()));heapify(a);r=0
while a[0]<m:
    if len(a)<2:r=-1;break
    heappush(a,heappop(a)+2*heappop(a));r+=1
print(r)