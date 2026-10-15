from heapq import*
q,k=map(int,input().split());h=[];s=0
for _ in range(q):
    c=input().split()
    if c[0]=="print":print(s)
    else:
        n=int(c[1]);s+=n;heappush(h,n)
        if len(h)>k:s-=heappop(h)