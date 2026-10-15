from heapq import*
input();a=[-x for x in map(int,input().split())];heapify(a)
while len(a)>1:
    y=heappop(a);x=heappop(a)
    if x!=y:heappush(a,y-x)
print(-a[0] if a else 0)