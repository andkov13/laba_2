import BFS
import RBFS
from stringcolor import * 

for i in range(20):
    res, dpth, time = BFS.attempt()
    print(f'{cs(( "SUCCESS" if res != None else "FAIL   "), ("green" if res else "red")).bold()} | {cs("DPTH", "blue").bold()}: {dpth} \t| {cs("TIME", "pink").bold()}: {time}');

print("---------------------------------------------------------------------------------------------------------------------------------");

for i in range(20):
    res, dpth, time = RBFS.attempt()
    print(f'{cs(( "SUCCESS" if res != None else "FAIL   "), ("green" if res else "red")).bold()} | {cs("DPTH", "blue").bold()}: {dpth} \t| {cs("TIME", "pink").bold()}: {time}');
