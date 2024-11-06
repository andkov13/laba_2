import BFS
import RBFS
from stringcolor import * 

def stringify (data: list[list[int]]):
    for i in range(len(data)):
        for l in range(len(data[i])):
            yield str(data[i][l])


for i in range(20):
    res, sm, dpth, time = BFS.attempt()
    print(f'{cs(( "SUCC" if res != None else "FAIL"), ("green" if res else "red")).bold()} {"".join(stringify(sm))} | {cs("DPTH", "blue").bold()}: {dpth} \t| {cs("TIME", "pink").bold()}: {time}');

print("---------------------------------------------------------------------------------------------------------------------------------");

for i in range(20):
    res, sm, dpth, time = RBFS.attempt()
    print(f'{cs(( "SUCC" if res != None else "FAIL"), ("green" if res else "red")).bold()} {"".join(stringify(sm))} | {cs("DPTH", "blue").bold()}: {dpth} \t| {cs("TIME", "pink").bold()}: {time}');
