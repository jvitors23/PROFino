#include <stdio.h>
#include <stdlib.h>
#define TAM 15
void troca(int arr[], int i, int j){
	int temp = arr[i];
	arr[i] = arr[j];
	arr[j]=temp;
}
int menorArr(int arr[], int ini, int fim){
	int menor = arr[ini];
	int indice = ini;
	for(int i = ini; i<fim; i++){
		if(arr[i]<=menor){
			menor = arr[i];
			indice = i;
		}		
	}	
	return indice;	
}
void selectionSort(int arr[], int ini,int fim){
	if(ini<fim){
		int menor = menorArr(arr, ini, fim);
		troca(arr, menor, ini);
		ini++;
		selectionSort(arr, ini, fim);		
	}	
	return;
}
int main(){	
	int arr[TAM] = {6, 3, 17, 54, 33, 12, 78, 1, 4, 22, 56, 34, 2, 65, 43};	
	selectionSort(arr, 0, TAM-1);		
  return 0;
}