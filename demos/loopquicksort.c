#include <stdio.h> 
#include <stdlib.h>
#define TAM 15
int particiona(int arr[],int ini, int fim){
	int pivot = arr[fim], i=ini, j=fim;	
	while(i<j){		
		while(arr[i] < pivot)
			i++;		
		while(arr[j]>=pivot && j>=ini)
			j--;			
		if(i<j){
			int temp;
			temp = arr[i];
			arr[i]=arr[j];
			arr[j]=temp;
		}	
	}
	arr[fim]=arr[i]; arr[i]=pivot;	
	return i;
}
void quickSort(int arr[], int ini,int fim){
	if(ini<fim){	
		int pivot = particiona(arr, ini, fim);
		quickSort(arr, ini, pivot-1);
		quickSort(arr, pivot+1, fim);			
	}	
}
int main(){	
	int arr[TAM] = {6, 3, 17, 54, 33, 12, 78, 1, 4, 22, 56, 34, 2, 65, 43};	
	while(1){
    quickSort(arr, 0, TAM-1);		
  }
  return 0;
}



