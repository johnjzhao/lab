#include <iostream>
#include <string>
#include <vector>

using namespace std;

int n, m, k;
const static int MAX_M = 52*52;

inline int fourMin(int a, int b, int c, int d){
    return min(a, min(b, min(c, d)));
}

void  CoinontheTable(int m, int k, vector<string> board){

    vector<vector<vector<int>>>
        tbl(n, vector<vector<int>>(m, vector<int>(k+1, -1)));
    if (0 == m || 0 == n || k < 0){
        cout<<-1;
    }
    tbl[0][0][0] = 0;
    for (int i = 1; i <= k; i++){
        for (int r = 0; r <= i && r < n; r++){
            for (int c = 0; c <= i && c < m; c++){
                if (r + c > i || i % 2 != (r+c) %2){
                     tbl[r][c][i] = -1;
                     //return;
                }
                int down=MAX_M, up =MAX_M, left=MAX_M, right=MAX_M;
                if (r > 0 && -1 != tbl[r-1][c][i-1] && board[r-1][c] != '*'){
                    down = tbl[r-1][c][i-1];
                    if (board[r-1][c] != 'D') down++;
                }
                if (c > 0 && -1 != tbl[r][c-1][i-1] && board[r][c-1] != '*'){
                    right = tbl[r][c-1][i-1];
                    if (board[r][c-1] != 'R') right++;
                }
                if (r+1 < n && -1 != tbl[r+1][c][i-1] && board[r+1][c] != '*'){
                    up = tbl[r+1][c][i-1];
                    if (board[r+1][c] != 'U') up++;
                }
                if (c+1 < m && -1 != tbl[r][c+1][i-1] && board[r][c+1] != '*'){
                     left = tbl[r][c+1][i-1];
                    if (board[r][c+1] != 'L') left++;
                }
                tbl[r][c][i] = fourMin(left, right, up, down);
                if (MAX_M == tbl[r][c][i]) tbl[r][c][i] = -1;
            }
        }
    }
    int ans = MAX_M;
    for (int r = 0; r < n; r++){
        for (int c = 0 ; c < m; c++){
            if ('*' == board[r][c]){
                for (int i = 0; i <= k; i++){
                    if (-1 != tbl[r][c][i])
                        ans = min(ans, tbl[r][c][i]);
                }
                break;
            }
        }
    }
    if (MAX_M == ans) cout<<-1;
    else cout<<ans;
    cout<<endl;

}

int main(){
    cin >> n >> m >> k;

    vector<string> board(n);
    for (int i = 0; i < n; i++) {
        cin >> board[i];
    }

    CoinontheTable(m, k, board);

    return 0;
}
