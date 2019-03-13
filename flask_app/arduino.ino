#define RELAY1  6
#define RELAY2  7
#define RELAY3  8
#define RELAY4  9

float vout = 0.0;
float vin = 0.0;
float R1 = 29900.0; //
float R2 = 7510.0; //
int value = 0;

bool RELAY1_status = 1;
bool RELAY2_status = 1;
bool RELAY3_status = 1;
bool RELAY4_status = 1;

void setup() {
    // put your setup code here, to run once:
    Serial.begin( 9600 );  
    pinMode(RELAY1, OUTPUT);
    pinMode(RELAY2, OUTPUT);
    pinMode(RELAY3, OUTPUT);
    pinMode(RELAY4, OUTPUT);

    //digitalWrite( RELAY1, LOW); // ON
    //digitalWrite( RELAY2, LOW); // ON
    //digitalWrite( RELAY3, LOW); // ON
    //digitalWrite( RELAY4, LOW); // ON


}

void loop() {

    
    // put your main code here, to run repeatedly:
    // wait until the serial connection is open
    while (Serial.available() == 0){
    
    int value = analogRead(A1);
    //Serial.println(value);
    float v = value*((5.0*(R1+R2))/(1023.0*R2));

   
    float average = 0;
    for(int i = 0; i < 1000; i++) {
        average = average + (.0264 * analogRead(A0) -13.51);//for the 5A mode,
        //   average = average + (.049 * analogRead(A0) -25);// for 20A mode
        // average = average + (.742 * analogRead(A0) -37.8);// for 30A mode
    }
    Serial.print(v,2);
    Serial.print(",");
    Serial.print(average,2);
    Serial.print(RELAY1_status);
    Serial.print(RELAY2_status);
    Serial.print(RELAY3_status);
    Serial.print(RELAY4_status);
    }

    //read from the serial connection; the - '0' 
    //is to cast the values as the int and not the ASCII code
    int COM_value = Serial.read() - '0';
    Serial.println(COM_value); //print to the console for testing
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
    } else if (COM_value == RELAY3) {
        if (RELAY3_status) {
            digitalWrite( RELAY3, HIGH); // OFF
            RELAY3_status = 0;
        } else {
            digitalWrite( RELAY3, LOW); // ON
            RELAY3_status = 1;
        }
    } else if (COM_value == RELAY4){
        if (RELAY4_status) {
            Serial.println("Received a 9- OFF");
            digitalWrite( RELAY4, HIGH); // OFF
            RELAY4_status = 0;
        } else {
            Serial.println("Received a 9- ON");
            digitalWrite( RELAY4, LOW); // ON
            RELAY4_status = 1;
        }
    }
    /*
    value = analogRead(analogInput);
    vout = (value * 5.0) / 1024.0; // see text
    vin = vout / (R2/(R1+R2));
    */

}
