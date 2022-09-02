#include <WiFi.h>
#include <WebServer.h>

static const char *SSID = "Tempec_";
static const char *PASSWORD = "wanda<3";

String red_wifi = "Tempec<3";
String contrasena = "123xxx123";
String setpoint = "20.5";
String histeresis_h = "2.2";
String histeresis_l = "3.3";
 
WebServer server(80);
 
void aliniciar() {
  server.send(200, "text/html", SendHTML(false));
}
 
void Online_h() {
  Serial.println("Modo Offline");
  server.send(200, "text/html", SendHTML(true));
}
 
void Offline_h() {
  Serial.println("Modo Online");
  server.send(200, "text/html", SendHTML(false));
}
 
void shazam() {
  red_wifi = server.arg("ssid");
  contrasena = server.arg("password");
  setpoint = server.arg("setpoint");
  histeresis_h = server.arg("histeresis_high");
  histeresis_l = server.arg("histeresis_low");
  
  Serial.println(red_wifi);
  Serial.println(contrasena);
  Serial.println(setpoint);
  Serial.println(histeresis_h);
  Serial.println(histeresis_l);
  server.send(200, "text/html", SendHTML(false));
}
 
void handle_NotFound() {
  server.send(404, "text/plain", "La pagina no existe");
}
 
String SendHTML(bool ONLINE) {

  String ptr = "<!DOCTYPE html> <html>\n";
  
  ptr += "<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr += "<title>D i i n p e c</title>\n";
  
  ptr += "<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr += "body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;} h3 {color: #444444;margin-bottom: 50px;}\n";
  ptr += ".button {display: block;width: 80px;background-color: #3498db;border: none;color: white;padding: 13px 30px;text-decoration: none;font-size: 25px;margin: 0px auto 35px;cursor: pointer;border-radius: 4px;}\n";
  ptr += ".button-on {background-color: #3498db;}\n";
  ptr += ".button-on:active {background-color: #2980b9;}\n";
  ptr += ".button-off {background-color: #34495e;}\n";
  ptr += ".button-off:active {background-color: #2c3e50;}\n";
  ptr += "p {font-size: 14px;color: #888;margin-bottom: 10px;}\n";
  ptr += "</style>\n";
  ptr += "</head>\n";
  ptr += "<body>\n";
  
  ptr +="<form action='/shazam' method='post'>\n";
  ptr += "<h1>T e m p e c</h1>\n";

  if (ONLINE)
  {
    ptr += "<a class=\"button button-off\" style='height:10px;width:25px;FONT-SIZE:10pt' href=\"/Offline\">Offline</a>\n";
  }
  else
  {
    ptr += "<a class=\"button button-off\" style='height:10px;width:25px;FONT-SIZE:10pt' href=\"/Online\">Online</a>\n";
    ptr += "<p>Red Wi-fi<br> <input type='text' name='ssid'     style='text-align:center' value="+red_wifi+"></p>\n";
    ptr += "<p>Password<br>  <input type='text' name='password' style='text-align:center' value="+contrasena+"></p>\n";
  }
  
  ptr += "<p>- Setpoint -<br> <input type='number' step='0.1' name='setpoint'       style='height:20px;width:40px'  value=";
  ptr += setpoint;
  ptr += "></p>\n";
  ptr += "<p>Histeresis +<br> <input type='number' step='0.1' name='histeresis_high' style='height:20px;width:40px' value=";
  ptr += histeresis_h;
  ptr += "></p>\n";
  ptr += "<p>Histeresis -<br> <input type='number' step='0.1' name='histeresis_low'  style='height:20px;width:40px' value=";
  ptr += histeresis_l;
  ptr += "></p>\n";

  ptr += "<p><button type='submit'>Enviar formulario</button></p>\n";
  ptr += "</form>\n";
  ptr += "</body>\n";
  ptr += "</html>\n";
  return ptr;
}
 
void setup() {
  Serial.begin(115200);
  WiFi.softAP(SSID, PASSWORD);
  IPAddress myIP = WiFi.softAPIP();

  server.on("/", aliniciar); 
  server.on("/Online", Online_h);
  server.on("/Offline", Offline_h);
  server.on("/shazam", shazam);
  server.onNotFound(handle_NotFound);
  server.begin();
  Serial.println("               TempecTempecTempec       TempecTempecTempec      TempecTempec      TempecTempec      TempecTempecTempec      TempecTempecTempec      TempecTempecTempec");
  Serial.println("                     Tempec             Tempec                  Tempec   TempecTempec   Tempec      Tempec      Tempec      Tempec                  Tempec");
  Serial.println("                     Tempec             TempecTempecTempec      Tempec      Tempec      Tempec      TempecTempecTempec      TempecTempecTempec      Tempec");
  Serial.println("                     Tempec             Tempec                  Tempec                  Tempec      Tempec                  Tempec                  Tempec");
  Serial.println("                     Tempec             TempecTempecTempec      Tempec                  Tempec      Tempec                  TempecTempecTempec      TempecTempecTempec");
  Serial.println("                     =================================================================================================================================================");
}

void loop() {
  server.handleClient();
}
