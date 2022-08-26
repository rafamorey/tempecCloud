#include "FS.h"
#include "SD.h"
#include <SPI.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <BluetoothSerial.h>

BluetoothSerial SerialBT;
File DATA;


/*----------SENSOR DE TEMPERATURA----------*/
/*ESPACIOS DE EEPROM
 * 100 = SETPOINT;
 * 110 = HISTERISIS;
 * 120 = INTERVALO DE LECTURA;
 * 130 = UNIDAD
*/
#define ONE_WIRE_BUS 5
#define OUT_COOL 32
#define OUT_HEAT 33
#define EEPROM_SETPOINT 205
#define EEPROM_HISTENEG 215
#define EEPROM_HISTEPOS 225
#define EEPROM_ILECTURA 235
#define EEPROM_METRICA 245
/*
 * RESISTENCIA PULL-UP  DISTANCIA DEL CABLE (METROS)
 *          4,7 kΩ            De 0 m a 5 m
 *          3,3 kΩ            De 5 m a 10 m
 *          2,2 kΩ            De 10 m a 20 m
 *          1,2 kΩ            De 20 m a 50 m
 */
 boolean HEATING = false;
 boolean COOLING = false;
/*-----------------------------------------*/

/*----------WIFI Y BLUETOOTH----------*/
/*POSIBLE LOGICA DE FUNCIONAMIENTO PARA EL GUARDADO DE LOS DATOS DEL WIFI EN LA EEPROM
 * CREO (FALTA UN POCO DE INVESTIGACION), EN LA MEMORIA EEPROM NO PUEDES GUARDAR STRINGS. DEBO GUARDAR
 * LOS DATOS DEL WIFI DE MODO QUE SEPARE LA CADENA EN CARACTERES ADEMAS DE GUARDAR EL LARGO QUE TENIAN PARA
 * QUE AL MOMENTO DE RECUPERARLA SABER CUANTOS ESPACIOS DEBO DE LEER.
*/
/*ESPACIOS DE EEPROM
 * 5 = SSID
 * 50 = CONTRASEÑA
 * 90 = LARGO SSID
 * 95 = LARGO CONTRASEÑA
*/
#define MSG_BUFFER_SIZE 50
#define LED_WIFI 25
#define LED_BLUE 26
#define TOPIC "Tempec/Server"
#define EEPROM_SSID_LARGE 30
#define EEPROM_PASS_LARGE 40
#define EEPROM_WIFIACTIVO ??
#define EEPROM_NOMBRE_RED ??
#define EEPROM_CONTRASEÑA ??

/*------------------------*/



/*----------DISPALAY SIETE SEGMENTOS Y CUATRO DIGITOS----------*/
#define DATO 15  // Pin conectado a DS pin 14 de 74HC595
#define CLOCK 4// Pin conectado a SHCP pin 11 de 74HC595
#define LATCH 2// Pin conectado a STCP pin 12 de 74HC595
#define CERO B00111111
#define UNO B00000110
#define DOS B01011011
#define TRES B01001111
#define CUATRO B01100110
#define CINCO B01101101
#define SEIS B01111101
#define SIETE B00000111
#define OCHO B01111111
#define NUEVE B01100111
#define MILLARES B00000001
#define CENTENAS B00000010
#define DECENAS B00000100
#define UNIDADES B00001000
#define PUNTO B10000000
int numeros[10] = {CERO,UNO,DOS,TRES,CUATRO,CINCO,SEIS,SIETE,OCHO,NUEVE};
int unidades[4] = {MILLARES,CENTENAS,DECENAS,UNIDADES};
int millar = 0;
int centena = 0;
int decena = 0;
int unidad = 0;
/*
 * ---p--g--f--e--d--c--b--a
 * B--0--0--0--0--0--0--0--0
 *        a
 *     ▓▓▓▓  
 *   ▓       ▓
 * f ▓       ▓ b
 *   ▓   g   ▓
 *     ▓▓▓▓
 *   ▓       ▓
 * e ▓       ▓ c
 *   ▓       ▓
 *     ▓▓▓▓   ▓ 
 *        d      p
*/
/*-------------------------------------------------------------*/



/*MICRO SD*/
#define PinSD 4
/*--------*/

/*RADIO FRECUENCIA*/
#define farmRed 2022
#define RX2 16
#define TX2 17
/*----------------*/


/*----------VARIABLES PARA WIFI----------*/
/*char* ssid = "404";//???????????????
char* password = "404";//?????????????*/
const char* ssid = "INFINITUM3F41_2.4";
const char* password = "xd7TS6tsHJ";
const char* mqtt_server = "test.mosquitto.org"/*"9bd78e371b064745883b9e4ede7be333.s2.eu.hivemq.cloud"//*/;
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
char msg[MSG_BUFFER_SIZE];
int value;
boolean WIFI = false;
String MENSAJE = "";
/*---------------------------------------*/

/*----------VARIABLES DS18B20----------*/
float SetPoint = 26;
float temperaturaIn = 0;
float lastemperaturaIn = 0;
float temperaturaEx = 0;
float Histerisis = 1;
float HisN = 1;
unsigned long lecturaMillis = 0;
unsigned long intervalo = 3000;/*INTERVALO DE LECTURA*/
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensor(&oneWire);
/*-------------------------------------*/

/*VARIABLES PARA MEMORIA SD*/
uint16_t sumac = 0;
/*-------------------------*/

/*VARIABLES DE BLUETOOTH SERIAL*/
/*String nameBlue = "NOMBRE";//Nombre modificable, talvez por el usuario o se podria dejar un nombre predeterminado
byte Mensaje[200];//*/
/*-----------------------------*/



/*----------SEGUNDO NUCLEO----------*/
TaskHandle_t Task1;


void Task1code(void * pvParameters)
{
  for(;;)
  {
    float t = temperaturaIn;
     if(t > 9 && t < 99)
  {
    millar = t/10;
    centena = (t-(millar*10));
    decena = (t-(centena+(millar*10)))*10;
    unidad = ((t-(centena+(millar*10)))*100)-(decena*10);
  }
  else if(t <= 9 && t > 0)
  {
    millar = 0;
    centena = (t-(millar*10));
    decena = (t-(centena+(millar*10)))*10;
    unidad = ((t-(centena+(millar*10)))*100)-(decena*10);
  }
  else if(t == -127)
  {
    //error = true;
  }
    shiftOut(DATO, CLOCK, MSBFIRST, unidades[0]);//DIGITO
    shiftOut(DATO, CLOCK, MSBFIRST, numeros[millar]);//NUMERO
    
    digitalWrite(LATCH,HIGH); // pulso ALTO
    digitalWrite(LATCH,LOW); // pulso BAJO
    delay(1);
    
    shiftOut(DATO, CLOCK, MSBFIRST, unidades[2]);//DIGITO
    shiftOut(DATO, CLOCK, MSBFIRST, numeros[centena]+PUNTO);//NUMERO
    
    digitalWrite(LATCH,HIGH); // pulso ALTO
    digitalWrite(LATCH,LOW); // pulso BAJO
    delay(1);
    
    shiftOut(DATO, CLOCK, MSBFIRST, unidades[3]);//DIGITO
    shiftOut(DATO, CLOCK, MSBFIRST, numeros[decena]);//NUMERO
    
    digitalWrite(LATCH,HIGH); // pulso ALTO
    digitalWrite(LATCH,LOW); // pulso BAJO
    delay(1);
    
    /*shiftOut(DATO, CLOCK, MSBFIRST, unidades[3]);//DIGITO
    shiftOut(DATO, CLOCK, MSBFIRST, numeros[unidad]);//NUMERO
    
    digitalWrite(LATCH,HIGH); // pulso ALTO
    digitalWrite(LATCH,LOW); // pulso BAJO
    delay(5);*/
    
  }
}
  
/*----------------------------------*/



void setup_wifi()
{
  delay(10);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  unsigned long waiting = 0;
  while(WiFi.status() != WL_CONNECTED)
  {
    digitalWrite(LED_WIFI,HIGH);
    if(millis() - waiting >= 500)
    {
      digitalWrite(LED_WIFI,LOW);
      waiting = millis();
    }
    
  }
  digitalWrite(LED_WIFI,HIGH);
  randomSeed(micros());
}

void callback(char* topic,byte* payload, unsigned int length)
{
  for(int i = 0; i < length; i++)
  {
    //Aqui poner codigo para el procesamiento de la informacion entrante
    //Normalmente es asi como se presenta para imprimirla en el puerto serial:
    //Serial.print((char)payload[i]);
  }
}

void reconnect()
{
  while (!client.connected())
  {
    String clientId = "AAAA";/*EL NOMBRE PUEDE CAMBIAR*/
    //clientId += String(random(0xffff), HEX);
    if(client.connect(clientId.c_str()))
    {
      Serial.println("connected");
     // client.publish(Topic, "hello world");/*Publica para saber que esta conectado*/
      //client.subscribe("outTopic");/*el topic de publicacion puede ser diferente al de subscripcion*/ 
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}


void writeFile(fs::FS &fs, const char * path, const char * message){
    //Serial.printf("Writing file: %s\n", path);
    File file = fs.open(path, FILE_WRITE);
    if(!file){
        //Serial.println("Failed to open file for writing");
        return;
    }
    if(file.print(message)){
        //Serial.println("File written");
    } else {
        //Serial.println("Write failed");
    }
    file.close();
}

void appendFile(fs::FS &fs, const char * path, const char * message){
    //Serial.printf("Appending to file: %s\n", path);

    File file = fs.open(path, FILE_APPEND);
    if(!file){
        //Serial.println("Failed to open file for appending");
        /*Agregar un indicador que el mensaje no se escribio en la SD*/
        return;
    }
    if(file.print(message)){
        //Serial.println("Message appended");
    } else {
        //Serial.println("Append failed");
    }
    file.close();
}



void setup()
{
  EEPROM.begin(512);
  Serial.begin(9600);
  Serial2.begin(9600,SERIAL_8N1,RX2,TX2);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  sensor.begin();
  
  pinMode(DATO,OUTPUT);
  pinMode(CLOCK,OUTPUT);
  pinMode(LATCH,OUTPUT);
  pinMode(OUT_COOL,OUTPUT);
  pinMode(OUT_HEAT,OUTPUT);
  pinMode(LED_WIFI,OUTPUT);
  pinMode(LED_BLUE,OUTPUT);
  
  xTaskCreatePinnedToCore(
    Task1code,
    "Task1",
    10000,
    NULL,
    1,
    &Task1,
    0);
}

void loop()
{
  if (!client.connected())
  {
    reconnect();
  }
  client.loop();
  temperatura();
  
  unsigned long now = millis();
  if(now - lastMsg > 60000)
  {
    lastMsg = now;
    /*USAR COMO EJEMPLO PARA LA PUBLICACION DE UN FLOTANTE
    char tempString[8];
    dtostrf(temperature, 1, 2, tempString);
    Serial.print("Temperature: ");
    Serial.println(tempString);
    mqtt.publish(topicTemperature, tempString);//*/
    //TIPO/ID/TEMPERATURA INTERIOR/TEMPERATURA EXTERIOR/OUT0/OUT1
    char MSN[50];
    strcpy(MSN,MENSAJE.c_str());
    client.publish(TOPIC,MSN);
    
    
  }
  
}
