#include<iostream>

using namespace std;

void transpose(int **matrix, int N)
{
    for( int i = 0; i < N; ++i ) {
        for( int j = i+1; j < N; ++j ) {
            if ( i != j ) {
                swap(matrix[i][j], matrix[j][i]);
            }
        }
    }
}

void reverse( int * row, int N ) {
    for ( int i = 0; i < N/2; ++i ) {
        swap(row[i], row[N-i-1]);
    }
}

void rotate1(int ** matrix, int N) {
    //transpose matrix
    transpose(matrix, N);
    // reverse each row
    for ( int i = 0; i < N; ++i ) {
        reverse(matrix[i], N);
    }
}

void rotate2( int ** matrix, int N ) {
    for( int i = 0; i < N/2; ++i ) {
        for( int j = i; j < N-i-1; ++j ) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[j][N-i-1];
                matrix[j][N-i-1] = matrix[N-i-1][N-j-1];
                matrix[N-i-1][N-j-1]= matrix[N-j-1][i];
                matrix[N-j-1][i] = temp;
        }
    }
}

void printMatrix( int ** matrix, int N) {
    for ( int i = 0; i < N; ++i ) {
        for( int j = 0; j < N; ++j ) {
            cout << matrix[i][j] << "\t";
        }
        cout << endl;
    }
}

int main() {
    int N;
    cout << "Enter N for NxN matrix:";
    cin >> N;
    int ** matrix = new int*[N];
    for ( int i = 0; i < N; ++i ) {
        matrix[i] = new int[N];
    }

    for ( int i = 0; i < N; ++i) {
        for ( int j = 0; j < N; ++j ) {
            cout<<"\nArr["<<i<<"]["<<j<<"]=  ";
            cin >> matrix[i][j];
        }
    }

    cout << "Rotated matrix by 90 (clockwise):\n";
    rotate1(matrix, N);
    printMatrix(matrix, N);

    cout << "Rotated matrix again by 90(anticlockwise):\n";
    rotate2(matrix, N);
    printMatrix(matrix, N);
    return 0;
}
