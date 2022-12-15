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


static const char *SSID = "TEM";
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
//#define monitoreo

/*----------SENSOR DE TEMPERATURA----------*/
/*ESPACIOS DE EEPROM
 * 205 = SETPOINT;
 * 215 = Histeresis;
 * 225 = Histeresis NEGATIVA;
 * 235 = INTERVALO DE LECTURA;
 * 245 = UNIDAD
 * 255 = DIFERENCIAL PARA ALERTA DE ALTA TEMPERATURA
 * 265 = DIFERENCIAL PARA ALERTA DE BAJA TEMPERATURA
*/
#define ONE_WIRE_BUS 5
#define TWO_WIRE_BUS 22
#define OUT_COOL 32
#define OUT_HEAT 33
#define WAR_COOL 26
#define WAR_HEAT 14
#define SENSOR0 0
#define SENSOR1 1
#define EEPROM_SETPOINT 205
#define EEPROM_HISTENEG 215
#define EEPROM_HISTEPOS 225
#define EEPROM_ILECTURA 235
#define EEPROM_METRICA 245
#define EEPROM_WARNINGH 255
#define EEPROM_WARNINGC 265
/*
 * RESISTENCIA PULL-UP  DISTANCIA DEL CABLE (METROS)
 *          4,7 kΩ            De 0 m a 5 m
 *          3,3 kΩ            De 5 m a 10 m
 *          2,2 kΩ            De 10 m a 20 m
 *          1,2 kΩ            De 20 m a 50 m
 */
 boolean HEATING = false;
 boolean COOLING = false;
 boolean NEUTRAL = false;
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
#define CLOCK 27// Pin conectado a SHCP pin 11 de 74HC595//esp32 pin 4 para la pcb de prueba
#define LATCH 2//2// Pin conectado a STCP pin 12 de 74HC595//esp32 pin 2 para la pcb de prueba
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
#define GRADO B01100011
#define ALTO B01110110
#define BAJO B00111000
#define NOTCERO B11000000
#define NOTUNO B11111001
#define NOTDOS B10100100
#define NOTTRES B10110000
#define NOTCUATRO B10011001
#define NOTCINCO B10010010
#define NOTSEIS B10000010
#define NOTSIETE B11111000
#define NOTOCHO B10000000
#define NOTNUEVE B10011000
#define NOTGRADO B10011100
#define NOTALTO B10001001
#define NOTBAJO B11000111
#define ERRORE B01111001
#define ERRORr B01010000
#define ERRORo B01011100

int numeros[10] = {CERO,UNO,DOS,TRES,CUATRO,CINCO,SEIS,SIETE,OCHO,NUEVE};
int notnumeros[10] = {NOTCERO,NOTUNO,NOTDOS,NOTTRES,NOTCUATRO,NOTCINCO,NOTSEIS,NOTSIETE,NOTOCHO,NOTNUEVE};
int unidades[4] = {MILLARES,CENTENAS,DECENAS,UNIDADES};
int SIMBOLO[3] = {GRADO,ALTO,BAJO};
int NOTSIMBOLO[3] = {NOTGRADO,NOTALTO,NOTBAJO};

int millar = 0;
int centena = 0;
int decena = 0;
int unidad = 0;
byte SIM = 0;
boolean parpadeo = false;
unsigned long timerParpadeo = 0;
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
#define EEPROM_USARSD 450
/*--------*/

/*RADIO FRECUENCIA*/
#define farmRed 2022
#define RX2 16
#define TX2 17
/*----------------*/

/*DETECCION DE FUENTE DE ALIMENTACION*/
#define DIVISOR 21
int voltaje = 0;
/*-----------------------------------*/


/*----------VARIABLES PARA WIFI----------*/
/*char* ssid = "404";//???????????????
char* password = "404";//?????????????*/
const char* ssid = "INFINITUM6BF5";//"INFINITUM3F41_2.4";
const char* password = "GnGhxrWEm3";//"xd7TS6tsHJ";
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
String ID = "AAAC";//id consta de cuatro caracteres alfabeticos
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
float Warning_heat = 2;
float Warning_cold = 2;
float startRange  = 0.2;//RANGO EN EL QUE EMPIEZA A TRABAJAR POR TIEMPOS
String Termometrica = "C";
unsigned long lecturaMillis = 0;
unsigned long intervalo = 3000;/*INTERVALO DE LECTURA*/
unsigned long activacion = 300000;//INTERVALO DE ACTIVACIÓN Y DESACTIVACIÓN 
unsigned long activacionMillis = 0;//VARIABLE DE COMPARACION PARA ACTIVACION
unsigned long descativacionMillis = 0;
boolean relevo = false;
boolean cambio = false;
boolean subida = false;
boolean bajada = false;
boolean ACT = false;
boolean DES = false;
unsigned long uno = 0;
unsigned long dos = 0;

OneWire oneWire_in(ONE_WIRE_BUS);
OneWire oneWire_out(TWO_WIRE_BUS);
DallasTemperature SENSOR_IN(&oneWire_in);
DallasTemperature SENSOR_OUT(&oneWire_out);
/*-------------------------------------*/

/*VARIABLES PARA MEMORIA SD*/
uint16_t sumac = 0;
boolean onceuponatime = false;
boolean haydatos = false;
unsigned long savetime = 0;
String DATOSD = "";
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
    int decmil = 0;
    if(t > 99 && t <= 999)
    {
      decmil = t/100;
      millar = (t-(decmil*100))/10;
      centena = ((t-(decmil*100))-(millar*10));
    }
    else if(t > 9 && t <= 99)
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
    if(parpadeo)
    {
      for(int x = 0; x<=100; x++)
      {
        shiftOut(DATO, CLOCK, MSBFIRST, unidades[0]);//DIGITO
        shiftOut(DATO, CLOCK, MSBFIRST, (Termometrica == "C") ? notnumeros[millar] : notnumeros[decmil]);//NUMERO
    
        digitalWrite(LATCH,HIGH); // pulso ALTO
        digitalWrite(LATCH,LOW); // pulso BAJO
        delay(1);
    
        shiftOut(DATO, CLOCK, MSBFIRST, unidades[1]);//DIGITO
        shiftOut(DATO, CLOCK, MSBFIRST, (Termometrica == "C") ? notnumeros[centena]-PUNTO : notnumeros[millar]);//NUMERO
    
        digitalWrite(LATCH,HIGH); // pulso ALTO
        digitalWrite(LATCH,LOW); // pulso BAJO
        delay(1);
    
        shiftOut(DATO, CLOCK, MSBFIRST, unidades[2]);//DIGITO
        shiftOut(DATO, CLOCK, MSBFIRST, (Termometrica == "C") ? notnumeros[decena] : notnumeros[centena]);//NUMERO
    
        digitalWrite(LATCH,HIGH); // pulso ALTO
        digitalWrite(LATCH,LOW); // pulso BAJO
        delay(1);
    
        shiftOut(DATO, CLOCK, MSBFIRST, unidades[3]);//DIGITO
        shiftOut(DATO, CLOCK, MSBFIRST, NOTSIMBOLO[SIM]);//NUMERO
    
        digitalWrite(LATCH,HIGH); // pulso ALTO
        digitalWrite(LATCH,LOW); // pulso BAJO
        delay(1);
      }
      //parpadeo = false;
    }
    
      for(int z = 0; z<=100; z++)
      {
      shiftOut(DATO, CLOCK, MSBFIRST, unidades[0]);//DIGITO
      shiftOut(DATO, CLOCK, MSBFIRST, (Termometrica == "C") ? numeros[millar] : numeros[decmil]);//NUMERO
    
      digitalWrite(LATCH,HIGH); // pulso ALTO
      digitalWrite(LATCH,LOW); // pulso BAJO
      delay(1);
    
      shiftOut(DATO, CLOCK, MSBFIRST, unidades[1]);//DIGITO
      shiftOut(DATO, CLOCK, MSBFIRST, (Termometrica == "C") ? numeros[centena]+PUNTO : numeros[millar]);//NUMERO
    
      digitalWrite(LATCH,HIGH); // pulso ALTO
      digitalWrite(LATCH,LOW); // pulso BAJO
      delay(1);
    
      shiftOut(DATO, CLOCK, MSBFIRST, unidades[2]);//DIGITO
      shiftOut(DATO, CLOCK, MSBFIRST, (Termometrica == "C") ? numeros[decena] : numeros[centena]);//NUMERO
      
      digitalWrite(LATCH,HIGH); // pulso ALTO
      digitalWrite(LATCH,LOW); // pulso BAJO
      delay(1);
      
      shiftOut(DATO, CLOCK, MSBFIRST, unidades[3]);//DIGITO
      shiftOut(DATO, CLOCK, MSBFIRST, SIMBOLO[SIM]);//NUMERO
      
      digitalWrite(LATCH,HIGH); // pulso ALTO
      digitalWrite(LATCH,LOW); // pulso BAJO
      delay(1);
      }
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
    if(millis() - waiting >= 500)
    {
      digitalWrite(LED_WIFI,HIGH);
      waiting = millis();
    }
    digitalWrite(LED_WIFI,HIGH);
    onceuponatime = true;
    EEPROM.put(EEPROM_USARSD, onceuponatime);
    EEPROM.commit();
  }
  if(millis() - imposible >= 3000)
  {
    Serial.println("IMPOSIBLE CONECTAR A RED WIFI");
    digitalWrite(LED_WIFI,LOW);
    WIFI = false;
    //onceuponatime = false;
  }
  randomSeed(micros());
}

void callback(char* topic,byte* payload, unsigned int length)
{
  for(int i = 0; i < length; i++)
  {
    //Aqui poner codigo para el procesamiento de la informacion entrante
    //Normalmente es asi como se presenta para imprimirla en el puerto serial:
    //20--TIPO/ID/NOMBRE/SETPOINT/Histeresis POSITIVA/Histeresis NEGATIVA/ALERTA SUPERIOR/ALERTA INFERIOR/METRICA
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
      for(int x = 0; x <= 7; x++)
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
      Warning_heat = DATOS[4].toFloat();
      Warning_cold = DATOS[5].toFloat();
      Termometrica = DATOS[6];
      MAJIN = "";
      EEPROM.put(EEPROM_SETPOINT, SetPoint);
      EEPROM.put(EEPROM_HISTENEG, HisN);
      EEPROM.put(EEPROM_HISTEPOS, Histeresis);
      EEPROM.put(EEPROM_WARNINGH, Warning_heat);
      EEPROM.put(EEPROM_WARNINGC, Warning_cold);
      EEPROM.put(EEPROM_METRICA, Termometrica.substring(0,1));
      EEPROM.commit();
      break;
      case 30:
      /**/
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
      onceuponatime = true;
     // client.publish(Topic, "hello world");/*Publica para saber que esta conectado*/
      client.subscribe(TOPSUB);/*el topic de publicacion puede ser diferente al de subscripcion*/ 
      EEPROM.put(EEPROM_USARSD, onceuponatime);
      EEPROM.commit();
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
      digitalWrite(LED_WIFI,LOW);
      delay(5000);
      if(intentos > 5)
      {
        serverconectado = false;
        WIFI = false;
        intentos = 0;
        digitalWrite(LED_WIFI,LOW);
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
   EEPROM.put(EEPROM_METRICA,'C');
  //Serial2.begin(9600,SERIAL_8N1,RX2,TX2);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);//*/
  SENSOR_IN.begin();
  SENSOR_OUT.begin();
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
  
  if(!SD.begin(PinSD))
  {
    #ifdef monitoreo
    Serial.println("MEMORIA SD NO INICIALIZADA");
    #endif
  }
  
  pinMode(DATO,OUTPUT);
  pinMode(CLOCK,OUTPUT);
  pinMode(LATCH,OUTPUT);
  pinMode(OUT_COOL,OUTPUT);
  pinMode(OUT_HEAT,OUTPUT);
  pinMode(LED_WIFI,OUTPUT);
  pinMode(WAR_COOL,OUTPUT);
  pinMode(WAR_HEAT,OUTPUT);
  pinMode(DIVISOR,INPUT);
  
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
    digitalWrite(LED_WIFI,HIGH);
    if (!client.connected())
    {
      reconnect();
    }
    client.loop();
    unsigned long now = millis();
    if(now - lastMsg > 60000)
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
  
  if(WIFI == false && onceuponatime == true)
  {
    if(millis() - savetime >= 60000)
    {
      String vanquivoide = "";
      vanquivoide += temperaturaIn;
      vanquivoide += "/";
      vanquivoide += temperaturaOut;
      appendFile(SD, "/TEMPERATURAS.txt",vanquivoide.c_str());
      savetime = millis();
      haydatos = true;
      #ifdef monitoreo
      Serial.println("TEMPERATURA GUARDADA EN MEMORIA SD");
      #endif
    }
  }
  else
  {
    savetime = millis();
  }
  if(WIFI == true && haydatos == true)
  {
    enviarDatosSD();
    int cantidad = 0;
    cantidad = (DATOSD.length()/11);
    for(int z = 1; z <= cantidad; z++)
    {
      String envio = "";
      envio = "30/";
      envio += ID;
      envio += "/";
      envio += DATOSD.substring(((z-1)*11),(z*11));
      strcpy(msg,envio.c_str());
      client.publish(TOPIC,msg);
      #ifdef monitoreo
      Serial.print("DATO ENVIADO: ");
      Serial.println(envio);
      #endif
    }
    haydatos = false;
    #ifdef monitoreo
    Serial.println("////////////TEMPERATURA ENVIADA AL SERVIDOR\\\\\\\\\\\\\\");
    #endif
    DATOSD = "";
  }
  server.handleClient();
}

void extraccion_de_EEPROM()
{
   int lengthssid = 0;
   int lengthpass = 0;
   char trica;
   EEPROM.get(EEPROM_SSID_LARGE, lengthssid);
   EEPROM.get(EEPROM_PASS_LARGE, lengthpass);
   EEPROM.get(EEPROM_SETPOINT, SetPoint);
   EEPROM.get(EEPROM_HISTENEG, HisN);
   EEPROM.get(EEPROM_HISTEPOS, Histeresis);
   EEPROM.get(EEPROM_WIFIACTIVO, WIFI);
   EEPROM.get(EEPROM_WARNINGH, Warning_heat);
   EEPROM.get(EEPROM_WARNINGC, Warning_cold);
   EEPROM.get(EEPROM_METRICA, trica);
   EEPROM.get(EEPROM_USARSD, onceuponatime);
   /*EEPROM.get(EEPROM_ILECTURA,);
   EEPROM.get(EEPROM_METRICA,);//*/
   EEPROM.commit();
   #ifdef monitoreo
   Serial.print("LARGO SSID");
   Serial.println(lengthssid);
   Serial.print("LARGO PASSWORD");
   Serial.println(lengthpass);
   Serial.println(onceuponatime ? "ONCE TRUE" : "ONCE FALSE");
   #endif
   char arrayssid[lengthssid];
   char arraypass[lengthpass];
   int casa = 5;
   int casita = 50;
   Strpass = "";
   Strssid = "";
   Termometrica = trica;
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
   Serial.println("////////////////////DATOS EXTRAIDOS DE EEPROM\\\\\\\\\\\\\\\\\\\\");
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
   Serial.println(WIFI ? "WIFI ACTIVO" : "WIFI INACTIVO");
   Serial.print("METRICA: ");
   Serial.println(Termometrica);
   Serial.print("ALERTA ALTA TEMPERATURA: ");
   Serial.println(Warning_heat);
   Serial.print("ALERTA BAJA TEMPERATURA: ");
   Serial.println(Warning_cold);
   Serial.println("////////////////////TERMINACION DE DATOS\\\\\\\\\\\\\\\\\\\\");
   #endif
   if(WIFI)
   {
    setup_wifi();
   }
   extraon = false;
}
