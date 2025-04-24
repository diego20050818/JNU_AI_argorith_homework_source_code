
from rich import print as rprint
def solveNQueens(n: int) -> list[list[str]]:
    result = []
    col = [0]*n

    def valid(r,c):
        for R in range(r):
            C =  col[R]
            if r + c == R + C or r - c == R - C:
                return False
        return True

    def dfs(r,s):
        if r == n:
            result.append(['.'*c + 'Q' + '.'*(n-c-1) for c in col])
            return
        for c in s:
            if valid(r,c):
                col[r] = c
                dfs(r+1,s-{c})
    
    dfs(0,set(range(n)))
    return result

if __name__ == '__main__':
    n = 4
    result = solveNQueens(n)
    for index,i in enumerate(result):
        print(f"\n第{index}个情况：\n")
        for j in i:
            rprint(j)
            

