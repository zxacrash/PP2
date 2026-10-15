from heapq import*
n,x=map(int,input().split());a=[-v for v in map(int,input().split())];heapify(a);r=0
for _ in range(x):
    k=-heappop(a);r+=k
    if k>1:heappush(a,1-k)
print(r)