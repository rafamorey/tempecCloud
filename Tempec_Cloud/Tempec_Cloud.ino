#include "FS.h"
#include "SD.h"
#include <SPI.h>
#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <EEPROM.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <WebServer.h>


static const char *SSID = "TEMPEC";
static const char *PASSWORD = "DIINPEC123";


WebServer server(80);
File DATA;

/*VARIABLES A ELIMINAR*/
String red_wifi = "";
String contrasena = "";//*/
String setpoint = "";
String histeresis_h = "";
String histeresis_l = "";
/*--------------------*/



/* SI monitoreo SE ACTIVA IMPRIMIRA DATOS DE CONFIGURACION DE WIFI Y TEMPERATURA GUARDADOS EN LA EEPROM*/
#define monitoreo

/*----------SENSOR DE TEMPERATURA----------*/
/*ESPACIOS DE EEPROM
 * 205 = SETPOINT;
 * 215 = Histeresis;
 * 225 = Histeresis NEGATIVA;
 * 235 = INTERVALO DE LECTURA;
 * 245 = UNIDAD
 * 
*/
#define ONE_WIRE_BUS 5
#define TWO_WIRE_BUS 22/*REVISAR PCB PARA DEFINIRLO*/
#define OUT_COOL 32
#define OUT_HEAT 33
#define SENSOR0 0
#define SENSOR1 1
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
 * 100 = WIFI ACTIVO
*/
#define MSG_BUFFER_SIZE 50
#define LED_WIFI 25
#define LED_BLUE 26
#define TOPIC "Tempec/Server"
#define TOPSUB "Tempec/Devices"
#define EEPROM_SSID_LARGE 90
#define EEPROM_PASS_LARGE 95
#define EEPROM_WIFIACTIVO 100
#define EEPROM_NOMBRE_RED 5
#define EEPROM_PASSWORD 50

/*------------------------*/



/*----------DISPALAY SIETE SEGMENTOS Y CUATRO DIGITOS----------*/
#define DATO 15  // Pin conectado a DS pin 14 de 74HC595
#define CLOCK 4// Pin conectado a SHCP pin 11 de 74HC595//esp32 pin 4 para la pcb de prueba
#define LATCH 2// Pin conectado a STCP pin 12 de 74HC595//esp32 pin 2 para la pcb de prueba
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
const char* ssid = "";//"INFINITUM3F41_2.4";
const char* password = "";//"xd7TS6tsHJ";
const char* mqtt_server = "test.mosquitto.org"/*"9bd78e371b064745883b9e4ede7be333.s2.eu.hivemq.cloud"//*/;
WiFiClient espClient;
PubSubClient client(espClient);
String Strssid = "";
String Strpass = "";
unsigned long lastMsg = 0;//
char msg[MSG_BUFFER_SIZE];//
char msgIn[MSG_BUFFER_SIZE];//
int value;
boolean WIFI = false;//indicador que debera cambiar de estado si el wifi esta disponible o no
String MENSAJE = "";//usada para formar el mensaje de topico 10
String ID = "AAAB";//id consta de cuatro caracteres alfabeticos
String MAJIN = "";//usada para formar el mensaje entrante
String UBICACION = "";//usada para manejar la ubicacion
String VEINTE = "";//usada para formar el mensaje de topico 20
int inicio = 0;//variable usada para separar las secciones de un mensaje entrante por wifi
int inicioAnt = 0;//variable usada para separar las secciones de un mensaje entrante por wifi
String DATOS[20];//array donde se guardan temporalmente las variables extraidas de los mensajes entrantes hasta que se acomodan en su respectivo lugar
char EXTRACCION[20];//variable para la extraccion de datos tipo string de memoria eeprom
boolean extraon = true;//variable para no tener un for en el setup y extraer de la eeprom solo una vez en el loop
boolean twenty = false;
boolean serverconectado = true;
byte intentos = 0;
/*---------------------------------------*/

/*----------VARIABLES DS18B20----------*/
float SetPoint = 26;
float temperaturaIn = 0;
float lastemperaturaIn = 0;
float temperaturaOut = 0;
float Histeresis = 1;
float HisN = 1;
unsigned long lecturaMillis = 0;
unsigned long intervalo = 3000;/*INTERVALO DE LECTURA*/
OneWire oneWire_in(ONE_WIRE_BUS);
//OneWire oneWire_out(TWO_WIRE_BUS);
DallasTemperature SENSOR_IN(&oneWire_in);
//DallasTemperature SENSOR_OUT(&oneWire_out);
/*-------------------------------------*/

/*VARIABLES PARA MEMORIA SD*/
uint16_t sumac = 0;
/*-------------------------*/

/*VARIABLES DE BLUETOOTH SERIAL*/
/*String nameBlue = "NOMBRE";//Nombre modificable, talvez por el usuario o se podria dejar un nombre predeterminado
byte Mensaje[200];//*/
String NAME = "";
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
  
  WiFi.mode(WIFI_MODE_APSTA);
  WiFi.begin(ssid, password);
  unsigned long waiting = 0;
  unsigned long imposible = millis();
  while(WiFi.status() != WL_CONNECTED && millis() - imposible <= 3000)
  {
    digitalWrite(LED_WIFI,HIGH);
    if(millis() - waiting >= 500)
    {
      digitalWrite(LED_WIFI,LOW);
      waiting = millis();
    }
    
  }
  if(millis() - imposible >= 3000)
  {
    Serial.println("IMPOSIBLE CONECTAR A RED WIFI");
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
    //20--TIPO/ID/NOMBRE/SETPOINT/Histeresis POSITIVA/Histeresis NEGATIVA
    //----02/AAAA/
    //10--TIPO/ID/TEMPERATURA INTERIOR/TEMPERATURA EXTERIOR/OUT0/OUT1
    MAJIN += (char)payload[i];
    //Serial.print(MAJIN);
    //Serial.println("");
    //Serial.println("ULTIMA");
  }
  int corto = 0;
  String comp = "";
  corto = MAJIN.substring(0,2).toInt();
  comp = MAJIN.substring(3,7);
  inicio = 8;
  if(comp = ID)
  {
    switch (corto)
    {
      case 10:
      /*NO DERBERIAS HABER ECIBIDO ESTE MENSAJE*/
      break;
      case 20:
      for(int x = 0; x <= 4; x++)
      {
        inicioAnt = MAJIN.indexOf('/',inicio);
        DATOS[x] = MAJIN.substring(inicio,inicioAnt);
        inicio = inicioAnt;
        inicio += 1;
        //Serial.println(DATOS[x]);
      }
      SetPoint = DATOS[1].toFloat();
      Histeresis = DATOS[2].toFloat();
      HisN = DATOS[3].toFloat();
      MAJIN = "";
      EEPROM.put(EEPROM_SETPOINT, SetPoint);
      EEPROM.put(EEPROM_HISTENEG, HisN);
      EEPROM.put(EEPROM_HISTEPOS, Histeresis);
      EEPROM.commit();
      break;
      default:
      break;}
  }
}

void reconnect()
{
  while (!client.connected() && serverconectado)
  {
    String clientId = "AAAA";/*EL NOMBRE PUEDE CAMBIAR*/
    //clientId += String(random(0xffff), HEX);
    if(client.connect(clientId.c_str()))
    {
      Serial.println("connected");
     // client.publish(Topic, "hello world");/*Publica para saber que esta conectado*/
      client.subscribe(TOPSUB);/*el topic de publicacion puede ser diferente al de subscripcion*/ 
    }
    else
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      Serial.print("SSID: ");
      Serial.println(ssid);
      Serial.print("PASS: ");
      Serial.println(password);
      intentos++;
      delay(5000);
      if(intentos > 5)
      {
        serverconectado = false;
        WIFI = false;
        intentos = 0;
      }
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
  //setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);//*/
  SENSOR_IN.begin();
  //SENSOR_OUT.begin();
  WiFi.softAP(SSID, PASSWORD);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("IP: ");
  Serial.println(myIP);

  server.on("/", INICIANDO); 
  server.on("/Online", ONLINE);
  server.on("/Offline", OFFLINE);
  server.on("/Cambio", Cambio);
  server.onNotFound(handle_NotFound);
  server.begin();
  
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
  if(extraon)
  {
    extraccion_de_EEPROM();
/*    red_wifi = ssid;
    contrasena = password;*/
  }
  
  if(WIFI)
  {
    serverconectado = true;
    if (!client.connected())
    {
      reconnect();
    }
    client.loop();
    unsigned long now = millis();
    if(now - lastMsg > 300000)
    {
      lastMsg = now;
      /*USAR COMO EJEMPLO PARA LA PUBLICACION DE UN FLOTANTE
       * char tempString[8];
       * dtostrf(temperature, 1, 2, tempString);
       * Serial.print("Temperature: ");
       * Serial.println(tempString);
       mqtt.publish(topicTemperature, tempString);//*/
       //TIPO/ID/TEMPERATURA INTERIOR/TEMPERATURA EXTERIOR/OUT0/OUT1
       strcpy(msg,MENSAJE.c_str());
       client.publish(TOPIC,msg);
    }
    if(twenty)
    {
      crearveinte();
    }
  }
  temperatura();
  server.handleClient();
}

void extraccion_de_EEPROM()
{
   int lengthssid = 0;
   int lengthpass = 0;

   EEPROM.get(EEPROM_SSID_LARGE, lengthssid);
   EEPROM.get(EEPROM_PASS_LARGE, lengthpass);
   EEPROM.get(EEPROM_SETPOINT, SetPoint);
   EEPROM.get(EEPROM_HISTENEG, HisN);
   EEPROM.get(EEPROM_HISTEPOS, Histeresis);
   EEPROM.get(EEPROM_WIFIACTIVO, WIFI);
   /*EEPROM.get(EEPROM_ILECTURA,);
   EEPROM.get(EEPROM_METRICA,);//*/
   EEPROM.commit();
   #ifdef monitoreo
   Serial.print("LARGO SSID");
   Serial.println(lengthssid);
   Serial.print("LARGO PASSWORD");
   Serial.println(lengthpass);
   #endif
   char arrayssid[lengthssid];
   char arraypass[lengthpass];
   int casa = 5;
   int casita = 50;
   Strpass = "";
   Strssid = "";
   for(int a = 0; a < lengthssid; a++)
   {
    EEPROM.get((casa + a),arrayssid[a]);
    EEPROM.commit();
    Strssid += arrayssid[a];
    #ifdef monitoreo
    Serial.print("Dato de EEPROM para ssid: ");
    Serial.println(arrayssid[a]);
    Serial.print("SSID FORMADA: ");
    Serial.println(Strssid);
    #endif
   }
   for(int b = 0; b < lengthpass; b++)
   {
    EEPROM.get((casita + b),arraypass[b]);
    EEPROM.commit();
    Strpass += arraypass[b];
    #ifdef monitoreo
    Serial.print("Dato de EEPROM para PASSWORD: ");
    Serial.println(arraypass[b]);
    Serial.print("PASSWORD FORMADA: ");
    Serial.println(Strpass);
    #endif
   }
   ssid = Strssid.c_str();
   password = Strpass.c_str();
   #ifdef monitoreo
   Serial.print("NOMBRE DE RED WIFI: ");
   Serial.println(ssid);
   Serial.print("CONTRASEÑA: ");
   Serial.println(password);
   Serial.print("SETPOINT: ");
   Serial.println(SetPoint);
   Serial.print("Histeresis POSITIVA: ");
   Serial.println(Histeresis);
   Serial.print("Histeresis NEGATIVA: ");
   Serial.println(HisN);
   Serial.print(WIFI ? "WIFI ACTIVO" : "WIFI INACTIVO");
   #endif
   if(WIFI)
   {
    setup_wifi();
   }
   extraon = false;
}
