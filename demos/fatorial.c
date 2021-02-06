int fatRecur(int n){
  if(n <= 1){
    return 1;
  }else{
    return n * fatRecur(n - 1); 
  } 
}

int fatIter(int n){
  int res = 1;
  for (int i = 1; i <= n; i++){
    res = res*i; 
  }
  return res;   
}

int main(void){
  int fat;
  while(1){
    fat = fatRecur(7);  
    fat = fatIter(7); 
  }
  return 0;
}

