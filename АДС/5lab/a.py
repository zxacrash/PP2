from heapq import*
input();a=list(map(int,input().split()));heapify(a);r=0
while len(a)>1:
    s=heappop(a)+heappop(a);r+=s;heappush(a,s)
print(r)