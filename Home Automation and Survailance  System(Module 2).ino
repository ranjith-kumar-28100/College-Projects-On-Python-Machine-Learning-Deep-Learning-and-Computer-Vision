
int state=0;
void setup() {
  pinMode(13, OUTPUT);
}
void loop() {
  if(Serial.available() >0)
    {
        state = Serial.read()- '0';
        if (state == 1)
        {
          digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)                           
        }
        while(Serial.available()>0)
        {
          serial.read();      
        }
      }
    }
  
