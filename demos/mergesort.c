#include <stdio.h>
#include <stdlib.h>

#define TAM 15

void merge(int arr[],int ini, int meio, int fim){
	int p1, p2, tamanho,*aux, i,j,k;
	p1=ini;
	p2=meio+1;
	tamanho = fim-ini+1;
	aux = (int*) malloc(tamanho*sizeof(int));
	
	if(aux!=NULL){
		for(i=0; i<tamanho; i++){
			if(p1!=-1 && p2!=-1){
				if(arr[p1]<=arr[p2]){
					if(p1!=-1){
						aux[i]=arr[p1];
						p1++;
						if(p1>meio)
							p1=-1;	
					}
				}else{
					if(p2!=-1){
						aux[i]=arr[p2];
						p2++;
						if(p2>fim)
							p2=-1;
					}
				}
			}else
				if(p1==-1){
					aux[i]=arr[p2];		
					p2++;		
				}else{
					aux[i]=arr[p1];		
					p1++;
				}
		}
		for(j=0, k=ini; j<tamanho; j++, k++)
			arr[k]=aux[j];
	}
	free(aux);
	aux=NULL;
}

void mergeSort(int arr[], int ini,int fim){
	if(ini<fim){	
		int meio = (int)(ini+fim)/2;
		mergeSort(arr, ini, meio);
		mergeSort(arr, meio+1, fim);	
		merge(arr, ini, meio, fim);
	}	
	return;
}

int main(){
	int arr[TAM] = {6, 3, 17, 54, 33, 12, 78, 1, 4, 22, 56, 34, 2, 65, 43};	
	mergeSort(arr, 0, TAM-1);		
	return 0;
}
