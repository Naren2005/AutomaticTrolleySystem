char data;

void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT);
  pinMode(4,OUTPUT);

}

void loop() {
  if (Serial.available() > 0){
    data = Serial.read();
    if (data == '1'){
      digitalWrite(2,HIGH);
      Serial.write("Transmitting HIGH");
      delay(100);
      digitalWrite(2,LOW);
      Serial.write("Trasmitting LOW");
    }
    else if (data == '2'){
      digitalWrite(4,HIGH);
      delay(300);
      digitalWrite(4,LOW);
    }
  }
else{
  Serial.println("NO INFORMATION RECEIVING");
  delay(200);
}
}
