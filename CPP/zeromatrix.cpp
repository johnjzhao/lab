#include<iostream>

using namespace std;

void nullifyRow(int ** matrix, int N, int row){
    for (int j = 0; j < N; j++){
        matrix[row][j] = 0;
    }
}

void nullifyCol(int ** matrix, int M, int col){
    for (int i = 0; i < M; i++){
        matrix[i][col] = 0;
    }
}

void nullifyMatrix(int ** matrix, int M, int N){
    bool firstRow = false;

    for(int i = 0; i < N; i++){
        if (matrix[0][i] == 0){
            firstRow = true;
            break;
        }
    }

    for (int i = 1; i < M; i++){
        bool nullifyThisRow = false;
        for (int j = 0; j < N; j++){
            if (matrix[i][j] == 0){
                matrix[0][j] = 0;
                nullifyThisRow = true;
            }
        }
        if (nullifyThisRow)
            nullifyRow(matrix, N, i);
    }

    for (int j = 0; j < N; j++){
        if (matrix[0][j] == 0){
            nullifyCol(matrix, M, j);
        }
    }

    if (firstRow){
        nullifyRow(matrix, N, 0);
    }
}

void printMatrix( int ** matrix, int M, int N){
    for (int i = 0; i < M; i++){
        for (int j = 0; j < N; j++){
            cout << matrix[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

int main(){
    int M, N;
    cout << "Enter number of rows:";
    cin >> M;
    cout << "Enter number of cols:";
    cin >> N;
    int ** matrix = new int*[M];
    for ( int i =0; i < M; ++i ) {
        matrix[i] = new int[N];
    }
    cout << "Provide M x N matrix \n";
    for ( int i = 0; i < M; ++i ) {
        for ( int j = 0; j < N; ++j ) {
            cin >> matrix[i][j];
        }
    }

    cout << "Matrix Before:\n";
    printMatrix(matrix, M, N);
    nullifyMatrix(matrix, M, N);
    cout << "Matrix After:\n";
    printMatrix(matrix, M, N);
    return 0;
}
