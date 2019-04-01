#define RELAY1  6 // modem
#define RELAY2  7 // analog streamer

/*
A0-current - 12v junction box
A1-v1 - 12v
A2-v2 - 5v
A3-v3 - pc 20v
A4-v4 - 12v
*/

float vout = 0.0;
float vin = 0.0;
float R1 = 29900.0;
float R2 = 7905.26;
//float R2 = 7510.0/.95;
int value = 0;

bool RELAY1_status = 0;
bool RELAY2_status = 0;

void setup() {
    // put your setup code here, to run once:
    Serial.begin( 9600 );  
    pinMode(RELAY1, OUTPUT);
    pinMode(RELAY2, OUTPUT);
    //pinMode(RELAY3, OUTPUT);
    //pinMode(RELAY4, OUTPUT);

    digitalWrite( RELAY1, HIGH); // OFF
    digitalWrite( RELAY2, HIGH); // OFF
    //digitalWrite( RELAY3, LOW); // ON
    //digitalWrite( RELAY4, LOW); // ON


}

void loop() {

    
    // put your main code here, to run repeatedly:
    // wait until the serial connection is open
    while (Serial.available() == 0){
    
    int value1 = analogRead(A1);
    int value2 = analogRead(A2);
    int value3 = analogRead(A3);
    int value4 = analogRead(A4);
    //Serial.println(value);
    float v1 = value1*((5.0*(R1+R2))/(1023.0*R2));
    float v2 = value2*((5.0*(R1+R2))/(1023.0*R2));
    float v3 = value3*((5.0*(R1+R2))/(1023.0*R2));
    float v4 = value4*((5.0*(R1+R2))/(1023.0*R2));

   
    float average = 0;
    for(int i = 0; i < 1000; i++) {
        average = average + (.0264 * analogRead(A0) -13.51);//for the 5A mode,
        //average = average + (.049 * analogRead(A0) -25);// for 20A mode
        // average = average + (.742 * analogRead(A0) -37.8);// for 30A mode
    }
    Serial.print(abs(average/1000),2);
    Serial.print(",");
    Serial.print(v1,2);
    Serial.print(",");
    Serial.print(v2,2);
    Serial.print(",");
    Serial.print(v3,2);
    Serial.print(",");
    Serial.print(v4,2);
    Serial.print(",");
    Serial.print(RELAY1_status);
    Serial.print(",");
    Serial.println(RELAY2_status);
    }

    //read from the serial connection; the - '0' 
    //is to cast the values as the int and not the ASCII code
    int COM_value = Serial.read() - '0';
    //Serial.println(COM_value); //print to the console for testing
    if (COM_value == RELAY1) {
        if (RELAY1_status) {
            digitalWrite( RELAY1, HIGH); // OFF
            RELAY1_status = 0;
        } else {
            digitalWrite( RELAY1, LOW); // ON
            RELAY1_status = 1;
        }
    } else if (COM_value == RELAY2) {
        if (RELAY2_status) {
            digitalWrite( RELAY2, HIGH); // OFF
            RELAY2_status = 0;
        } else {
            digitalWrite( RELAY2, LOW); // ON
            RELAY2_status = 1;
        }
    }
    /*
    value = analogRead(analogInput);
    vout = (value * 5.0) / 1024.0; // see text
    vin = vout / (R2/(R1+R2));
    */

}
