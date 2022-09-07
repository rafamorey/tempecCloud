 void INICIANDO() {
  Serial.print("SSID: ");
  Serial.println(Strssid);
  Serial.print("PASSWORD: ");
  Serial.println(Strpass);
  server.send(200, "text/html", SendHTML(WIFI));
}
 
void ONLINE() {
  Serial.println("Modo Offline");
  WIFI = false;
  EEPROM.put(EEPROM_WIFIACTIVO, false);
  server.send(200, "text/html", SendHTML(WIFI));
  /*WIFI = false;
  EEPROM.put(EEPROM_WIFIACTIVO, false);*/
}
 
void OFFLINE() {
  Serial.println("Modo Online");
  WIFI = true;
  EEPROM.put(EEPROM_WIFIACTIVO, true);
  server.send(200, "text/html", SendHTML(WIFI));
  /*WIFI = true;
  EEPROM.put(EEPROM_WIFIACTIVO, true);*/
}
 
void Cambio() {
  if(WIFI)
  {
    red_wifi = server.arg("ssid");
    contrasena = server.arg("password");
  }
  //red_wifi = server.arg("ssid");
  //contrasena = server.arg("password");
  setpoint = server.arg("setpoint");
  histeresis_h = server.arg("histeresis_high");
  histeresis_l = server.arg("histeresis_low");
  
  if(WIFI)
  {
    ssid = red_wifi.c_str();
    password = contrasena.c_str();
  }
  //ssid = red_wifi.c_str();
  //password = contrasena.c_str();
  SetPoint = setpoint.toFloat();
  Histeresis = histeresis_h.toFloat();
  HisN = histeresis_l.toFloat();
  
  
  
  if(WIFI)
  {
    int casa = 5;
    int casita = 50;
    int ssidlong = red_wifi.length();
    int passwordlong = contrasena.length();
    EEPROM.put(EEPROM_SSID_LARGE, ssidlong);
    EEPROM.put(EEPROM_PASS_LARGE, passwordlong);
    EEPROM.commit();
    #ifdef monitoreo
    Serial.print("LARGO SSID: ");
    Serial.println(ssidlong);
    Serial.print("LARGO PASSWORD: ");
    Serial.println(passwordlong);
    #endif
    for(int c = 0; c < ssidlong; c++)
    {
      EEPROM.put((casa + c),red_wifi.substring(c,c+1));
      EEPROM.commit();
      #ifdef monitoreo
      Serial.print("DATO ");
      Serial.print(c);
      Serial.print(": ");
      Serial.println(red_wifi.substring(c,c+1));
      #endif
    }
    for(int d = 0; d < passwordlong; d++)
    {
      EEPROM.put((casita + d),contrasena.substring(d,d+1));
      EEPROM.commit();
      #ifdef monitoreo
      Serial.print("DATO ");
      Serial.print(d);
      Serial.print(": ");
      Serial.println(contrasena.substring(d,d+1));
      #endif
    }
    
  }
  
   EEPROM.put(EEPROM_SETPOINT, SetPoint);
   EEPROM.put(EEPROM_HISTENEG, HisN);
   EEPROM.put(EEPROM_HISTEPOS, Histeresis);
   EEPROM.commit();
   //WIFI=true;
   extraon = true;
   twenty = true;
  #ifdef monitoreo
  Serial.println(ssid);
  Serial.println(password);
  Serial.println(setpoint);
  Serial.println(histeresis_h);
  Serial.println(histeresis_l);
  #endif
  server.send(200, "text/html", SendHTML(WIFI));
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
  
  ptr +="<form action='/Cambio' method='post'>\n";
  ptr += "<h1>T e m p e c</h1>\n";

  if (ONLINE == false)
  {
    ptr += "<a class=\"button button-off\" style='height:10px;width:25px;FONT-SIZE:10pt' href=\"/Offline\">Offline</a>\n";
  }
  else
  {
    ptr += "<a class=\"button button-off\" style='height:10px;width:25px;FONT-SIZE:10pt' href=\"/Online\">Online</a>\n";
    ptr += "<p>Red Wi-fi<br> <input type='text' name='ssid'     style='text-align:center' value=";
    ptr += Strssid;
    ptr += "></p>\n";
    ptr += "<p>Password<br>  <input type='text' name='password' style='text-align:center' value=";
    ptr += Strpass;
    ptr += "></p>\n";
  }
  ptr += "<p>- Setpoint -<br> <input type='number' step='0.1' name='setpoint'       style='height:20px;width:40px'  value=";
  ptr += SetPoint;
  ptr += "></p>\n";
  ptr += "<p>Histeresis +<br> <input type='number' step='0.1' name='histeresis_high' style='height:20px;width:40px' value=";
  ptr += Histeresis;
  ptr += "></p>\n";
  ptr += "<p>Histeresis -<br> <input type='number' step='0.1' name='histeresis_low'  style='height:20px;width:40px' value=";
  ptr += HisN;
  ptr += "></p>\n";

  ptr += "<p><button type='submit'>Enviar formulario</button></p>\n";
  ptr += "</form>\n";
  ptr += "</body>\n";
  ptr += "</html>\n";
  return ptr;
}//*/
