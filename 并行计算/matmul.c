#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
int isPrint = 0;

void printMatrix(int* A, int M, int N)
{
	if (isPrint == 0) return;
	int i, j, k;
	k = 0;
	for (i = 0; i < M; i++)
	{
		for (j = 0; j < N; j++)
		{
			printf("%d ", A[k++]);
		}
		printf("\n");
	}
	return;
}

void initialize_Matrix(int* A, int* B, int M, int L, int N) {
	int i, j, k;
	printf("Initializing matrix A: ");
	printf("%d rows * %d cols\n", M, L);
	for (i = 0; i < M; i++)
		for (j = 0; j < L; j++)
		{
			k = i * L + j;
			*(A + k) = i + j;
		}
	printMatrix(A, M, L);
	printf("\n");

	printf("Initializing matrix B: ");
	printf("%d rows * %d cols\n", L, N);
	for (i = 0; i < L; i++)
		for (j = 0; j < N; j++)
		{
			k = i * N + j;
			*(B + k) = i - j;
		}
	printMatrix(B, L, N);
	printf("\n");
	return;
}

int main(int argc, char** argv)
{
	time_t t1, t2;
	int* A, * B, * C;
	int i, j, k, ia, ib, ic;
	int M = atof(argv[1]);
	int L = atof(argv[2]);
	int N = atof(argv[3]);
	isPrint = atof(argv[4]);

	// initialize Matrix A and B
	A = (int*)malloc(sizeof(int) * M * L);
	B = (int*)malloc(sizeof(int) * L * N);
	C = (int*)malloc(sizeof(int) * M * N);
	initialize_Matrix(A, B, M, L, N);

	t1 = time(NULL);

	// matmul
	ia = 0;
	ic = 0;
	for (i = 0; i < M; i++)
	{
		for (j = 0; j < N; j++)
		{
			ib = j;
			C[ic] = 0;
			for (k = 0; k < L; k++)
			{
				C[ic] += A[ia+k] * B[ib];
				ib += N;
			}
			ic++;
		}
		ia += L;
	}

	t2 = time(NULL);

	printf("Matrix C: ");
	printf("%d rows * %d cols\n", M, N);
	printMatrix(C, M, N);
	printf("\n");

	printf("total time: %ld sec\n", t2 - t1);
	printf("\n");
	//printf("C[3]=%d", C[3]);
	printf("\n");
	return 0;
}