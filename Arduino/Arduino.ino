char data;
const int BUZZER = 2;
const int LED_GREEN = 4;
const int LED_RED = 5;


void setup() {
  Serial.begin(9600);
  pinMode(BUZZER,OUTPUT); // BUZZER
  pinMode(LED_GREEN,OUTPUT); // LED GREEN (SUCCESS)
  pinMode(LED_RED,OUTPUT); // LED RED (FAILURE)

}

void loop() {
  if (Serial.available() > 0){
    data = Serial.read();
    if (data == '1'){
      digitalWrite(BUZZER,HIGH);
      delay(100);
      digitalWrite(BUZZER,LOW);
    }
    else if (data == '2'){
      digitalWrite(LED_GREEN,HIGH);
      delay(400);
      digitalWrite(LED_GREEN,LOW);
    }
    else if (data == '3'){
      digitalWrite(LED_RED,HIGH);
      delay(100);
      digitalWrite(LED_RED,LOW);
    }
  }
else{
  Serial.println("NO INFORMATION RECEIVING");
  delay(200);
}
}
