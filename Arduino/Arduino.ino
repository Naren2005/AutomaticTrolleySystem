char data;

void setup() {
  Serial.begin(9600);
  pinMode(2,OUTPUT); // BUZZER
  pinMode(4,OUTPUT); // LED GREEN (SUCCESS)
  pinMode(5,OUTPUT); // LED RED (FAILURE)

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
      delay(100);
      digitalWrite(4,LOW);
    }
    else if (data == '3'){
      digitalWrite(5,HIGH);
      delay(100);
      digitalWrite(5,LOW);
    }
  }
else{
  Serial.println("NO INFORMATION RECEIVING");
  delay(200);
}
}
