

int teste2(int a){

  for (int i = 0; i < 150; i++){
    for (int j = 0; j < 10000; j++)  {
      for (int k = 0; k < 10000; k++)  {
        a = i+j+k;
      }
    }
  }

  return a;
  
}

int teste1(int tot){
  int a;
  for (int i = 0; i < 10000; i++)  {
    for (int j = 0; j < 10000; j++)  {
      for (int k = 0; k < 10000; k++)  {
        a = i+j+k;
      }
    }
  }
  teste2(a);


  tot = tot - a;

  return tot; 
}

// int main(void){ 
//   int tot;
//   for (int i = 0; i < 10; i++) {
//     int a = teste();
//     tot = a;
//     tot = tot - 2700;
//   }

//   return 0;
// }


int main(void){ 
  int tot = 0;
  while(1) {
    int a = teste1(tot);
    tot = a;
    tot = tot - 2700;

    if(tot < 0){
      tot = 0;
    }
  }
  
  return 0;
}