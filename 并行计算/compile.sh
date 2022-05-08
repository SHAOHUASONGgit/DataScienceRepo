#!/bin/sh
clear

M=200
L=40000
N=300
isPrint=0
nThread=4

echo "serial"
g++  matmul.c -o matmul.out
./matmul.out ${M} ${L} ${N} ${isPrint}

echo "nThread=" ${nThread}
g++ -fopenmp matmul_OMP.c -o matmul_OMP.out
./matmul_OMP.out ${M} ${L} ${N} ${isPrint} ${nThread}


echo "nThread= 8"
g++ -fopenmp matmul_OMP.c -o matmul_OMP_8.out
./matmul_OMP_8.out ${M} ${L} ${N} ${isPrint} 8

