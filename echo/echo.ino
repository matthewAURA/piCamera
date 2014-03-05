
short count;
short parts[8];
int result;


  

void waitForSerial(){
  while (Serial.available() == 0){} 
}


void setup() {
  Serial.begin(9600);
  digitalWrite(13,LOW);
}

void loop() {
  if (Serial.available() > 0){
    char incoming = Serial.read();
    count = 0;
    Serial.write(incoming);
    if (incoming == 'i'){
      waitForSerial();
      count = Serial.read();
      for (int i=0;i<count;i++){
       waitForSerial();
       parts[i] = Serial.read();
      } 
      result = 0;
      //Put the parts together
      for (int i=0;i<count;i++){
        result += parts[i] << (8*i);
      }     
      Serial.print(result);
    }
  
  }
}
