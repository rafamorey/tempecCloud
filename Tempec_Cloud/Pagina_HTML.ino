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
  ptr += "p {font-size: 14px;color:rgb(255,150,0);margin-bottom: 10px;}\n";
  ptr += "</style>\n";
  ptr += "</head>\n";
  ptr += "<body background=data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCADhAOADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD8qqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoors/BHwi8TePtsun2PkWLAn7dd5jhONw+U4JflSp2g4OM4rWlRqV5clKLb8jCviKWGg6taSjFdWcZRX1d4T/Zz8L6BHFJqRfXbxWV2knOyFSCSAI1JypGM7i2cdACRXz18UtD/4Rz4ha9YiOGKNbppIo7cYRI3+dFAwMYVgMdBjivUxmVYjA0o1a2l3a3b9PuueHl2fYTNMRPD4a75Ve7Vk/Tr96Ru+G/gD4v8AEdtb3S21tY2NxAtxDdXVwCrqwBUYTcwJBzyB0Pfiuo0n9lfWJrhhqet2NnBsyr2yPOxbI4KsEwMZ5z2HHPHrXwRvrnUvhboU08nmOI2hDYAwscjKo49ERR+Fd1z7V9pg8hwFSlCrPmd0nq+6v0PzjMeKs1o4mrh4uK5W1ouzt1ufPx/ZRC8N4p2/XT/8Jad/wyev/Q0N/wCC/wD+2173zRzXof2Flv8Az6/GX+Z4v+tecf8AP/8A8lj/AJHgjfsnBf8AmagPrYf/AG2sXUP2WfEEN1ILPVtMntRjbLO0kTnjnKBWxznuf6V9M81FWcuH8BLaFvm/1bLhxdm1N3dVS9Yx/RI+GvFXg/V/BWoR2Os2n2S5kiEyoJUkyhJAOUJHVT+VY9es/tM6hb33xGSOB972tlHFKuCNrFnkA56/K6nj1ra/Zz+Hum+JtL8Q3+saVDf25KWlu8xyAxBMoABypw0Z38EfwnrXwDy/22Plg8O9m9X5d7I/XFnCoZVDMsXHdJtLTd9LvzvvseGUV9D+Ov2Yojai68Jzyics7tY3sgZWGCQsTheoPA3Eg55YY58N8TeFdV8G6q+m6xZtZXiqH2MQwZT0KspIYdRkE8gjqDWGMy3E4F/vY6d1qvv/AEZ2ZfnGCzON8PPXs9JL5f0jKooorzD2QooooAKKKKACiiigAooooAKKKKACrGn6bd6tdpa2VtLd3L5KwwIXdsAk4A5PANSaPo974g1S207TrZ7u9uH2RQxjkn+gAySTwACTxX1x8KPhPY/DfTEll23mt3Cg3FwqghMc+WueQgPU/wAX4DHsZbltXMKlo6RW7/T1Pnc6zqjk9HmlrN7L9X5HHfDH9nSDSANR8XQx3t1uRoLBXzFHjDHzDwHIPykcpx/GGyvs8NvDaW8cFvEkMMShI441CqigYAAHQAdqk2n0o+7X6nhcHQwUfZ0Y6d+r+Z+EZjmmKzOp7SvO/l0Xohy/davl/wDae0sWfjqyuY7byorixUNMEwJZFdgfmxywQxj1A2+1fUbZ2ivF/wBqbTreXwZpOoGPNzFf+Ssm4/KrxuzDHTnYn/fHua87PKTq4Cf92z+49jhTEewzSF/tXj+H+aIv2WdVim8K6zp3lO0trercMxA27ZEAAHPXMLZ47ivbVzXzF+yzcyR+NtVhEriJtNaQxhjtZ1kjCkjuQGbB7bj619O87aeQ1fa4CCfS6+5k8WUfYZpV5ftWf3r/ADQnNHNHNHNfQHx+oc1FUvNY/ijVJdE8M6vqMCo89nZzXEayAlSyIWAOCOMj1qJSUIuT2RpShKrUVNbt2Pj74o65/wAJH8QddvlaGSNrloontzlHjjxGjA5OcqgORwc8V9E/s46KLH4YxTCbzDqFxLcMu3Hl/N5W3Oef9WDnj72O2T8m194eHdJ/sLQdN0zzfP8AsdtFb+bt279iBd2MnGcdM1+fcOwliMZVxU+n5yf/AA5+xcYTjhMuoYKHdfdBf8FF2quueH9P8TWVxYapp9teWrKTtkQDawUruUn7j4JGeCOxq1RX6FKKknGSumfkFOpOlNVIOzR8p/E74E6l4JDX+lmbWdGJctIkRMlsBlh5gHUbBkuMDIOQvGfLq+/udvtXzl8bvgh/Yxn8Q+HbfOnnc93YxDPkY5aSMf8APP1H8Pb5c7fz3N8iVJPEYNe71j1Xmu679j9i4e4p+uSWFxztPpLv5Ps+3f138Oooor4g/SgooooAKKKKACiiigAooq5caPe2emWeoz20kVleNItvM4wJdhAcr6gEgZ6ZyOoNNJu7S2E5JWTe59WfBH4YW/g3wzDqN1Cp1u/jDTNIp3QoeRGMgFSONw7tkZIAr0WvFf2dvikNVs4vCWp8XFrC5tLt5ctLEP8AllgnJZQflxwEX+EKSfayMV+xZXOjPCQlhtFtbz63/rXc/nTiGliqWY1Prju3qvTpYSpeaOaOa9g+YDmuJ+M2kzax8MtdgiZFZbYXOZCQMROJCOAedkZA98fWu25qvLbxXlvLBPEk8EqlJI5FDK6kYIIPUEdqwr0/bUp0+6a+9WOzB13hcRTrr7DT+53PjX4Q6sdF+JXh+4EXnb7n7Nt3bceaDFu6HpvzjvjHHWvs7sa+E9Ss7rwp4kurQXGy9027aIXFs5GJI3I3I3B6rkHg19029xFeWsc8EiTQyKHjkjYMrqeQQR1BHevjuGKkuWrQfR3/AEf5H6NxxSi6mHxUftJr7tV/6UT80c0c0c19wfluoc81wvxt1htC+Fet+Vcpbz3EYt037cyB5FV0UHqdhkPHIAJ7ZrujnNeK/tUatFD4T0XTNr+bc3huVYAbcRxlWzz1zKuOOx/Hys0qOlgKtS9mlb79D6DIcP8AWczoQav7yf3a/oeH/C/RP+Ei+IGg2Rjhlja6WWWO4GUeOP8AeOpGDnKqRg8HNfazda+XP2Y7GG6+JElxIm+WzsZJ4WyRtcsiZ46/K7Dn1r6iryOGafJhJT/mf5W/U+m42xHtMfCivsx/F/8AAsFFS80c19YfnOpFRRUdxcRWlvLPPKkMESl5JJGCqigZJJPQAd6XmaJNuyPm/wDaE+Ftj4T+ya5pMUNlZTyfZprJAcrKd7h17YIBG0Y27RgYNeLV2vxY+JU/xL8RreeW1vYW0fkWsDNyFySWIzgMxPOOgCjJxk8leabd6b5H2u1mtfPiWeLzoynmRt911yOVPYjg1+MZjUo1sTOeGjaP9a+Vz+lsop4mhgqVPGSvUtr/AJedivRRRXmHshRRRQAUUUUAbPg7wzceMvE+naNbHZJdy7TJx8iAEu+CRnChjjPOMDmvr/xd8ObHxT4NPhtXa0s7eNY7Niok+ztGAFI3cngY6g4J55ryz9lnw0q22seIZFRizfYImDNuTCh5Mjpg7oyDyfkbp395wQB71+lZDl8Pqcqk1f2n5bf8H7j8X4qzit/aMaVCXL7L/wBKer+5WX39z4TP9oeD/EeP+PXVdLuv9l/Lmjf8VOGX3Br7F+G/j6y+Ivhm3u4XQXkKIl7bgbfs8uMcDJwjYYpyeuOoIHH/AB2+EsPirTZtb0q1mbxBbqoZI1BN6gABBHdwoypHJwUwTtx4N8LfHj/DvxdBqfltPaujQXUKhdzxkg8EjghlVuCM7cZAJrx6MquQ432VXWnLr+vquv8Awx9Di6dHizLPb0NK0Onn29H0f/BPs+pearW9xFd28U8EqTQSqHjkjYMrqRkEEdQR3qSv0jzPxRqSdmS80c0c1FTEfIHx20YaL8UNYEdrJawXRS6j3hsSF0Bd1J6gyeZ04BBHbFfSfwh1T+1fhh4euVi8nbbCEru3ZMTeUW6DqI847Zxz1ryP9qjw+8esaPrab2gmhNo+IztR0JYZb1YO2B/sHr26H9lnV4pvCusaZhhLBerOSwG0+YgVQOev7p88dx+HwmAvhM5q0Wrc9/8A5JfgfrWaWzDhvD4hauHLf/0l/jY9nqXmjmjmvuz8m1I9vy5r5a/aa1CK7+IsUCSb5LOxjglXBGxizuBz1+V1PHr9a+pif3aivin4p6hPqXxH8SS3EvnSLfSwhsAfJGxRBx6Kqj8K+S4mrcuEjD+Z/l/wT9E4Jo+0x86j+zH83b/M9l/ZT0uWHSde1FmT7PcXEUCqCd26NSxzx0xKMc9j+PunOK5D4PaOdF+Gfh2ASeb5lr55bbjBlLSAdewfHviuw52j617OV0fq+Ep030jf5vX82fM57iPrmZ1qy/mt8lovyE5qKiivUPDCvBP2k/iRhf8AhD7BxgbZdRbZ1PyvGisfXhmwOoXn7wr0b4vfEKP4e+EzNCP+JtdbobNVZcoxU/vMMDuVBt7HJIBxnNfK3hXw3qPxA8Uw2UbTTT3MvmXV23zmNCw3yuSRnGe55JA6kV8dnuPlaOAw69+W9vPp8/y9T9J4VymLk81xWkIbX6tdf+3enn6HR/B74V3nxE1xJni26LaSK1zI4bEuMHyVwQckdSCMA56lQ3t37QngpfEng2S9hjP27SS1xHjoY8ZmXlgANqhwcE/Jgfer0LQdBtPC+h2Wl2SNFZ2cflpuRSznGS7BQBuOM8cdT3qa6hhvoJIJokmilUpJHIoZXUjBBB6gjtXXh8lp0cHLDS+KXxfp9zPPx3E1avmVPF0/gg9F5db+qPgeiuo+JvhN/BnjbU9O8jyLXzTNahSxXyWOUAZuWwPlJ55UjJxXL1+X1acqNSVOe6dj9xo1oYilGrTd1JXXzCiiisjYKKK6z4TaTLrfxJ8O2sJQMLxJzvJAKxnzGHA6kIQPfHStaVN1akaa3bS+8wr1lh6M60topv7lc+tPAGgf8Iv4P0PSxEtvJDaRtNGr7wJWAeUk5OcMW6HHpxW7RUvNfuVOmqcI01slb7j+XK9Z4irKrPdtt/MjXoRXzT+0J8LP+Efvj4l0yKd7C9lZrwN8wglZuGznOHyevAYdcMor6W6GquraVZ+INLuNP1C2S7tLhNksTjIZexyOQQcEEcggEc15mZ4GOOo+ye+6fn/W57GS5pUyjFRrLWD+Jd1/n2Pnr9nn4rpoVxH4W1ISNb3c22xnUs3lSuQPLK9lJ5GB94nOQ25fo6vir4keB7j4f+K7nTJQfIJMtrIzBmeEsQpbAGG4IPA5Bxxgn6j+Efj5PiJ4Tt52cLqloVtryJmUlm2j94AOgk68gDcrDoM14WRY2ak8vxGjjt6LdfLp5H1vFWWUpxjm2E1jP4vns/ns/P1OyqXmoql5r7Q/MdTyv9pXSZLz4bCaNkX7HdxXMoYnJU7owBx1zIOuOAa86/ZZ1GeLxhqtgr4t7iy8149o5dJFCnPXhZH/AD9hXu3xB0/+1vA2v2wtvtkkljMIoRHvLybCV2r3YMFIxzkDFfK3wY1+Xw98StDlj3lLmcWUqLIUDLL8nPqFJVsHqVHTqPhcy/2fNqGIvZS0/G35M/V8j/23IMThFvG/5X/NM+zOaioor7o/KSLUL2HTNPur66fyrW1iaaWTBO1FBLHA5PAPSvhDTdPuNY1K1sbSPzrq6mWGKPIG52YBRk8DJI619ifGLWJtB+F/iKWJVaSWH7PiQEriVljc8Hrtc498da+cPgVoo1z4oaMj27zw27PdSFQ2I9iFkdiOgD7OvBJA74r4HP08RjKGGXX/ANudv0P1rhJ/U8uxeOey/wDbY3/U+u7e3itLeKCCJIYIlCRxxqFVFAwAAOgA7VZ5o5o5r70/JW5Sd2HNUda1Sz8PabcahqFxHa2lum+WWQ8KvTGOpJOAAOSSAOatr0zmvmz9or4mSavqbeGbGaRbO0bN6UkUpPLwVTA7J3BP3s5Hyg15mY4+OX0ZVXu9EvM9/JcrqZti44daRWsn5f1ojzvxx4y1P4n+Kvt00G6eTbb2tpbqWKruO2McZY5Y/UnjAwB9PfB34aw/D3w2GdWl1W+RJLzzGBCsASI1AJHy7ioPOWJ5xgDzf9nP4XxXSjxVqsEcq8jTI2YEblYq0pX1BGFz3DNgbVNe/wBeDkOAlLmx+J+KWz9f8+nkfW8UZtTgllWD0hDe3VrZfLr5+gUUUV9kfmep4Z+1VoO/T9C1pfJ/dyNau2P3rBhujGccqvlydTxu4HJr51r7X+K2mQ618NPElvJviiis2nDoQCzR5lUcjpuXn2z0r4or8u4jw7pYz2vSav8Adofu/B2L+sZd7F70218nr+oUUUV8qfdhXsn7LkEp8b6lcLE5hTT2jaUKdqs0kZUE9ATtbA77T6V43X0H+yfjy/FR/iDWmP8AyNXuZJD2mYUl6v7k3+h8zxLP2eU12uyX3tL9T3qpeaior9fP5y1CipeaioLOX+JXgGx+IHhe4sp0Rb63R5LG4zjy5cZ5OD8rAKp9cZxkLj5S8J+JNS+Fnjb7V5P+lWcklrd2hkwJF5SSMlcj6HkAhTzivtb7x4rxv9ob4W/25Yt4k0qJPttjCWvwRtaaIDIbr1QA9eSuB/CBXyWd4CUlHGYb+JDe3l+bX5H6Fwxm8KbeW4zWnU0V9lfp6P8AM9Z0HXLPX9DsdXs5Vms7yFZdqsrPGSPuOQSAQcgjsQRV0KVUOK+Xf2f/AIoQeEdTk0bV7lbfRrx/MjlaMEQ3B2ruLZ4UqMHORlV6Dca+oeV4PSvUyzHLMKHtF8S0fr/Wx89neVVMoxbpL4JbPuu3quom35c18RagT4H+IFybDMh0jU2+z/aOS3lSnbvxjP3RnGPwr7d3fKK+T/2ivD8OhfEqeS3CJHqFvHeeUkYQIxyjdOpLRlifVj9T43ElKXsYV19mX5/8Mj6bgmtFYmthp/bX5f8AAbPq+iuV+EOqnXPhj4duhF5IjtRaFd27JjbyiencLnHbOOetdVX1lGoqtONSP2kn96PgsVQeGr1KEt4Nr7meL/tUalFb+F9F0/y3WW6vGuFYAbcRoVOeev71cfQ1zH7K+kPceKNY1Esggt7QW7KSd26RwykcdMRNnnuPwT9qbVJJvEehWBVPKhsmuQwB3FpJGUg89MRLjjufw9C/Zt0ubS/hl9pkeMjULme5hCk5VQBHhuOu6InjPGPpXxCX1rPW+kP0S/Vn6XKf1DhSK+1Udvvk3/6Sj1PmoqKq+ItetPDeh3uqagypaWcZlfYQHbrhUyQMlhwM8kgV93KXLFybskfldOnKtONOCu2cJ8bfig3gHRUt7GSH+3rvKRI/zNDFggzEAYJBG1c9yTztIrwP4P8Aw3l+IXiQebsXSLFklvmYkFkJOI1wQcttYZyAMHnOAcwDWvi/4+AHkyavqkoA6RxoFXH/AHyqL7khe56/XvgrwjZeB/D9rpVkkTrEn7yTZt8+UqAZDyTknnqegUcAV8HRjLPsZ7er/BhovPy9Xpfy08z9cxNSHCuXLC0XfEVN328/RaqPnr3Rp29vFaW8UEESQwRKEjjjUKqKBgAAdAB2qSiivvdlY/I223dkvNRUUUzPUVq+EvEmk/8ACP8AiLVNLE32gWV1Lbedt279jld2MnGcZxmvuyviP4i/8lA8Tf8AYTuf/RrV8NxQk6VKXm/yR+p8CTkqten0sn+L/wAznqKKK/PT9gCun8D/ABI1z4f3hl0u5zAwbzLOfLwPkDJK5GG+VfmGDxjOMg8xXffCzwFp/jldUW9luYXt/K8t4HVQN27JYFTn7o6EfjW1GrOjNTpy5WupwY6WHjh5SxSvDrpfyPX/AAb+0xoepW6xeILdtIu1XDTRq80L/dBIxlkJJY42tgKOSa9ct7iK7t4p4JUmglUPHJGwZXUjIII6gjvXyJ4i+C+v6HDJcW6pqturYH2UMZdpOASmOe2dpbGeuBmuc0fxZ4g8IzGLT9TvtMMUwke3jlZE8xSPvx9CeACCO2DX1+C4kq0ly4mPMu60f+T/AAPzzE8K4DMF7bLKvL5br/NfifcVFeIeBP2m7W5aSHxPax2ErP8AurqzSRoVXac713M+cjtuB3chcZPtOnX1tq1ql1Y3MN3bSZ2TW8gdGwSDgg4PII/CvtsLjsPjI81CV326r5H5zmGU4vLZcuKhyrv0fzJqKl5qKvQPHPlT47/C/wD4QfW11Oxw2kalI7LHHHtW1lzkxcDaF6lB1wCP4cn179n/AOJTeMvD82mX8ss+uacqkyySKzXEWeHx1JUYVjzwRkkua9E8QaHZ+KdBvNH1BGe2uk8tiqLuXjKspYY3jrz3wa+O9Qs9Z+DfxA+QbbuxkL2800Y2XEJyA+MnhlJBwcg5GQw4+FxMHkeNWKor91Pddv63XzR+r4KtDijLpYGu7V6esX37P9JfJn2cfvGvCf2p9D8zTtD1lEhXypXs5XxiV9w3xjOOVAR+p4LcdTXsfg3xRD4w8MWes2myGO6i37SSWjYAq6FiBnaQRnHOM1x37QWn2998KdSnmTfLaSQy25yRtbzVTPHX5JCOf730r6DM4LF4Co4vRx5r+iufH5JOpgc4oxqKzUuRr190579lvULeTwfq1ismbyG+MrJg/LHJGqg56clG/L6V7L2NfNP7LWoXMfjDVLFJMWs1n50kW0fO6Oqoc9ePNb8/YV9JXFxFZ2sk88iQwRKXeSRgqooGSST0AHes8hre0wNPpy3X3P8AyN+KcP7LN5xX2rP71/mfHPxm1WLWPif4guIldVWcQHzAAd0aLGx4PTchx7Y6V9VfDnRotC8A+H7IWz2ki2kZmgkDBlmZdzghuQd7Mcds446V8faHC/jTx1p8OoSsX1bUY1uJYwqsTLKA7AYwD8x7Y9q+4mG18V4nD0frGIr4qXV/q2/0PpOL2sNhcLl6+yr/APgKUV+oMTI2epr5b+P3xSHjDVl0TTZYptD09wyzxnd9om24Z92PujlRjIPXJG3HpP7RXxKXw3ozeH9PcLqOqRAzN5W4R2zBlYBjxlvu9D0c8Haa4n9nn4UJrl3D4p1QMtnazg2VuQ6+dIpz5hI6opHbqykHhSDtmmIq46t/ZmE6/E/L+t/kjnyDB0cswss6xq0XwLu+/q9l82ejfAv4WHwLox1K/wBv9rahGjurR7WtkIyIskbgxBy4PcDj5Mn0pTg0FSKPu19Rh8PTwtKFCn8MfzPhsdjamYVp4ms7yl+HkJ1opV61zfjT4l+HvAqouraiUuJImlhtIVZ5GC9OBwATwNxAJB54ONqlSnSjz1Gku7dkcuHw1bFVPZUIuT8jpV2/xVi+KvH3h7wOkR1jV4LOWQBkt0DPIwOcMETkL8pG7GMjGa+e/HP7SGs640ttoMf9i2RDIJzh7l1O4Z3dI8gr0ywK8PXm1tp+u+N9SlljjvNYvGKia4ctIRn5VMjnoMDqxwAPavkMbxJSpvlwkeZ93t92j/I/Rcv4NqSj7XMp8keyav8AN7L8T1rxr+05eXim18L2Z06HA/0y8xJMT8pyE5RejAht+Qcjaa8QuLiW6nkmmkaaaRi7ySMWZmJySSepJr1zwz8BjJGZdevHjfGRaWRUsOn3pDwCOexHo1eZ+J7ODT/Emq21qhS2hupY4lYkkKHIAyfavhcVjq2NnzVp8zX4H6BlMcsoOWHy+K03ff59fyMyiiiuI+kCvRvgPfQ2fjZo5W2vcWrxRDBO59ytj24VuvpXnNbfgfU/7H8X6RdmRYo0uUWVnIC+Wx2uCTwAVJGaaV9Dgx9H6xhalLumfVVZOu+E9I8TIq6hp1vMdoUzP8sgAORhwMgZzwD3PrWnUijdXApOGqdj8MpVZ4eXPTlZni3iD9n+6jjebRL0XX9y1uQEkIxzhuh56ZA6+1cNbXnin4cX26CbUNElaQH5WZI5ih7/AMMijPuMN6GvqDHrxVa80u01aHyby0hvIVbcEnjDqDyM4I68n866KWIlGXNez8tD63C8SVbeyxkVOPn/AFZnA+D/ANqGSG3W38TWLzbFwLrT0UFuFHzRkgZPzEsCB0AUV7noviDTfE2nx3Wl3sN/aKB+8gbOOAcMOqtgjKnBGeRXgviH4C6deLJJpFxJp0+MrHPueFjjoCRuGT/Ec9+K88u9B8W/CvVjeW5ubN4gp+3WZYxMpYEKxxjG4DKsOcDjBFfZZfxHWpLlre/H8V/X9Mmvk+UZxrgJ+zqdnt93+V/Q+y+etcf8WPhzD8SPDr2qMtvqFu5ltbkoCAdp+Vj1COeuMfwNggYrynwh+1HdwusHifTlvLfCg3OnqI5QQp3EoTtYsdvAKAcnB4Fe4+F/GGi+LbFrnSNRiv4lXa4jwJIySQA6NggHacZAzjIr7OnjMHmtJ0ISununo/680fI1suzPIK8cRKNrbSWsfn/k7HzP8F/iFP8ADrxVJpGrCeLS7qYQ3FvK3li2nDbRKwbG0ryrcjg5OSoFfUutaPb61ot7p07OsV5A9vI0ZAYK6lSRkHnB9K8P/aS+GaeTL4wtGkNzujXUI2PylThFlGTxg7EwOuRwMMTx2g/tFeIvD/hvTtMhgtbqWzBiFxclzmEKojTarLgqNwzk5G0YGCW8DC4xZPOpgcY7wXw9dH08v+HPrcZl3+sUKOaZdZT+0vNdfl+KsYfwS1C30v4paHLdP5cbPLADtLZeSJ40GB6syj2zzX058YtYOi/DXxDcNF5wktDbhd+3Blbyg3Q9A2cd8Y4618ZfbpItQ+2Wv+gyrL5sX2dmHknOV2kksMcYJJPHWtHUPGniHVrOS0vtd1K8tJMb4Li8kdGwcjKk4ODz9a8PAZt9SwtXDWu5Xs/Nqx9RmmQ/2ljqGMcrKFrrvZ36HW/s/wDhz/hIPiXp8jKjw6cDfOrMynKkBCMdSJGQ4PGAevQ/UPjTxZZeBfD91ql7KGWFM28ZfaLiYqSqDg8k+g6ZzwCa+OPA/jnUvh/rf9p6X5LTNE0Lx3Ee5HQ4OD0I5AOQQePTIOx45+IGs/GDX9Oge3hi2yfZ7KzhOMF2AG52PJOEBJwOM4GTnry3NKOBwM4U03Wb0072/Lt3OLN8jrZpmVOrVaVCK11101a+fft6EHhPRdS+LXxBhivp57qW6l86+uudyRLjcchSF4wq8bQSg4FfY+n2MGk6faWlrGIba2iWGKMEkKiDAGTyeB1Nc/8ADXwDY/D3wvb2cESf2lMiyXs4bc00oGThiBhFDMo4GMepJOF4u+O/hbwzZkRXi6zeOm5LewZZAc7seZJ91eVAOMkZB2mvo8vw9PKKLq4qaUp7vqvLu/PzPis4xVfiDFRw2Apt06eiS29eyXbyPRF2/wAVcj40+LHhzwMrx6hf+ZfL92ws1WWYHg4PIVeHBy+CRnGa+avFnxh8WePpobdrl7SN0Nv9i0wyIk+84IZdxLE8DHT0HJzJ4Z+Cuua4kc15jSLdyeLlG84gfxCPrjPc49fTPlYviWyaw0fnL/L/AIJ6GF4To4OKrZpW5f7q/wA9/uXzNHxt+0H4i8Ub4NO/4p+xJzstZC07fdPMuAeoP3QvDEHdXMeGPhnr3its29obaDari4uw0cbA9CDg5HfI49+Rn27w78K/D3h6GULZjU2lIPnX8aS4wOijbgD3HJ9+K6v9K+FxWPqYmXPUlzPz2Xy/ysepLPMNl9P2GV0VFd3/AFd/NnnHhT4F6ZpeybWJP7UnwG2puWGPoc4xluc4JwCD9016HaWcGnW6W9rBHbW8edscKBVGTk4A46k1JtIp1ec6kqmh8visficbLmrzuvw+4gvb6LT7We6nfy4IUaSRsE4UDJOB7Cvke9vJtQvJ7q4fzJ55GlkfAG5mOSePc19HfFvXF0PwReEJ5k19/oyNjIXeGyTz/cDfiRXzXXTR0h8z73hXD8lGpWa+J2+7/hwooorU+5CiiigD6d+FmvR634K05ol8trZFtJVGSAyYGeg6jaTj+9jtXUjI5rwb4HeKBputTaRcTqlvejMAlY4E2QMDsCy5HuVT0Ar3bnpXHWg4y5+jPxjO8H9Txkktpar0YlFFFZnzw+iiiqSfQevQ47xB8I9A8RH/AI8/7PuAMJJp6hM9cBkxtI56gBuBXmuqfCjxN4LuP7U0S9kuXgbEc2ns8V0uRgkKOe5B2k8H0zXsTeNdADbzrmnp9bmIn8ga5y/+N3hmyVfLubu/Zs5MEBG367yo59h2rphKtGKbjfs9mfZ4DF5tT9xQc49mrr7+h5X4u+K/i7xNpkmja1fN5azEzxiBYHcjGI3CgDahBIXHBPsMcVXqXxC+IHhnxppFz5GmSxaoip5NzNEFYAMNw3KxzwWwD8uCe+3Hm11pd5YwW81zaT28NwN0MksbKsg45UkcjkdPUV21p1KrU6knJ273/E/QMv5Y0EvY+y/u6fhYrUUUVznqBRRWg+jXmnx293fadeR2EhQiRo2jEisMja5UjkAkHB9eaaTZLko7nWp44+IHjvS00WK+1DUbSPbG4hjAOCpUCWUAEgjOd7YOCT0zW74c+AV3PIkmtXsdtHgE21uSZckHILFcLg45wwPPPetXRfjJ4S0GxS0stJvrWBfm2pFHw2AMk7/mOFAyeTiuo0v4teFtSeNW1MwzOu5VuYygU4yQzEbQR09M9M08RVrzl715Ndb3PgcZisfh4yhg8N7OPlHX100NvS/DOkaGofTrCC1KxiFpYohv28dXwN3Qck81oVlx+KtFupEtoNXsJZHYKix3SEsTwABnk1r1wyc5O8rnwdZV5y5q97+Yyin+XTKw1OMKKKr6pqEej6fcX865ht43lbyyCxUKeFHYgLWkYuTUYq7ZpTpyqSUYnj/x+19ZNTtNGgZDFCv2mbawJ3nIVT3ACgsPUSfSvJav69q8uvazeajOXMlxK0mHcuVBPC59AMD8KoV37aLofumAwqweGhQXRa+vUKKKKD0AooooAfDNJbTRzQyNFLGwdJEJDKwOQQexr3HSf2gNM/s+3/tKyuvtwUCb7PEjRkjjjLg4I5IPcnnvXhdFGjVnqjzcbl+HzBJV43seza1+0BEsbR6PpOcgYlviODnkbF68d9w6+3OBcfHnxFMkgSDT4JGBHmrCzMPcbmIz9RXR+GvghoWpaXBeyaxcX8E7KyT2pSJAuOQQQ5DZyOcehFdhpfwv8NaXCFh0qG7fChmuv3rMR35JUE99uBRKUKUtbL0Vz4ypiMjwacI0uZruv/kv8jxNvHPjLxNKsUOoahcSRqW8uxUoccAkiMDPbr0z71cs/hz408YXKyXkF0Co8vz9VlZSgAyBhsvjJ7AjJ+tfQdpZwWFukFtBHbwJnbFCgVRk5OAOOpNT7vasnXXRficM+JfZ6YShGPb+lY8U0f4A3TTf8TTUkjQMuI7KNpGcZ+YZbG04xggN16cc9hpvwP8ADNo0omiutQDAbPNmI2/QqF/X0rvKX8awdapbSx5WIz7HV/8Al44+mhQ03QdN0li1lp9tbBsbjbxJGTjpk456n86j8UTafaeH72XUkhk0+OPzZlcK2/ByFCtxuZhwD3xWhtNeHfHDxcuoahFodtN5sFo++cqwK+bjAXp1UZB56sR2qqfNUlzSbDK8NVzPFxTk7LVs5vwd4Zj+IXjSaFV+wWLNJdSxxYzHFuzsQ4xnkAEjA647V6ZJ8BNBkinEV3qMcoU7HaRGVD2LDYNw9gRWj8IfB/8Awj/heO6fbJeamEmJTPCYBRevOAWJ4HJ77c13e0gA1dSry1LHrZpndeGJcMLUtCOi82tz55+GM1p4b8fvpmsQwyMZTapI8CyeXcK+FYEjK85GR0JBPTI+gZoYri3eKVFljkUq6OAQwPBBB6ivH/j14Zhh+ya7GQk0jLbSqijD8MVfPc4GOc5GOmOe0+FPjOTxloZkvXQXto3lzFW+8oUYfb2LZYehIYj0GlX3oqcen9fgVm0XjsNTzOk9tJLs/wCv0NC++Hvh3UIXgOiWuGxl7eJYz1zwynI/A1y918AdCuhM8F5e2TNkou9JETPQYwCQPrn3r0kmmc1yxrTj/Vz52hmmNo6U6rX4ngt98B9fhaf7LPZ3qx5KqrMruB04IwCfrj3rNfQfiB4aRbKKLWoIVXcI7KV3jAJP/PMlQc549/evo6m+Ua3jiEun3Huw4lxNrVoxkvNHzRa/Ezxbo7SQf2vdCRXO8XSiRw3QglwSOnSt4fHzxArbltNOQ/7Mcn9XNe4aho2m6sEF9Y2955ednnxK+3OM4yOOg/KuU1v4NeG9ZnFwlvNp5/i+wkIjcADghlHTtjqc5qva02rXOuGcZTXa+sYblfdJf8BnN6f+0FatMReaPLDFt+/DMJXJ9PmC8dec1zvxQ+LCeM7ODT9OgmtrFW8yVpfkZ2GcLtViNvQ89wOmOanxP+H+l+CPs/2PU5Jppj8tnMoL7OcyFgBgZwoBHJDHPGBwNae6tUl6n0uBy3LpuGNw0PTf9QooooPpQooooAKKKKACiiigDvPhf8SG8G3DWV2C2k3D73Kj5onwBu45K4AyPbI54P0NBNHdW8c0LrLDIoZHQgqynkEHuK+Pa7X4f/E6+8GzRW0xa60jzAzwZ+eMc5MZzxyc7TwSO2c0SiqkbPfoz43OsjWNf1jD6T6rv/wT6Op1UtJ1q11ywNzpt1DeWrEb2XHBIBAYDoRkZBwRV5a4JRcXZn5ZVpSoy5ZqzEoopuTUJNuyMtTnPiN4qHg/wrNdQOou5h5Nv3IkbPzdCMqMnnuorxH4Z+F5fGniwPclpbW3JuruaXLBuchSSCCWbsevNV/iR4wbxj4jlnjP+gwForYcjcm4neQehbqeB2Hava/hP4Vbwt4VhMkQ+23v+kTErhkGOFPAPyqRx2YsK9HSjD0/M/SuT+wsrd/4tT8P+GX4nW0+mU+uA/Nyprmk2+u6Ld2F0qvFMhifaoZhycFcg/xHIPYgV84aDql/8L/G7iZSklrKba6jVfvx7hu25x6BgeO3avpzd8u2vHvjp4NVbeDxBAGLjZBOI4sqV52yMw9DhOevy9O/Rh57w7H2XD2LhzzwVfWFTT5/8H/I9dt547mJJYpFlikUMkiEFWU8ggjqKepwa8o+B/jQXtnJoN7c4uYP3lo0z/fTAygGOduMjnv6LXq1Y1ocjsup8/mOCnl9eVF7foMooorLU80VRurC8beOLDwfpYnuSJ5eUt7VD8ztjJOewBx9Mj2zm/EL4mWXg2B4YXju9WLEC1jcFIm4IaQDp1ztHXtjnHzzrWuX/iK+N3qNy1zcFQu5sAADoABwB16epPeuunh+XWrv2PtMoyGeKkq+I0h27/8AAH+IPEF74m1SW+v5jLM/Crk7Y1ycIo7KM8Cs6iiunc/UoxUEoxVkgooopFBRRRQAUUUUAFFFFABRRRQBp+H/ABJqHhm+W50+5eFgQWQMQkg5GGAPIwT+fFe0eCvjVY62EtNb8vTbzkCbpbsPTJOUOO3Q4684rwSik0pK0jyMdleGzCP72Npd1ufYdvJDcwJLFIssUihkdDlWBGQQR1FebfGjxsNH0kaPZvtur5MyjZlVhIKnGe5IwOvAPQ4NeSeHfHeueF2jWw1CZbZTk2kjF4G5zgoePXkYPJ5rM1jVrjXdUutQum3T3EhduSQM9AMknAGAB2AFTGnGD5ov+u587gOG/quK9rVlzRW3/BOn+FHhP/hKPFULTQ+bp9li4uAU3K+OVjPGPmI5B/hDHtX0ny2BXlnwl8ReGtB0GKyGrwrfSk3Nx9o/c7Gwo2KzAKe3Rs5DH0x6ZY30F7bpcW08dxA2dskLhlODg4I9wayrxm5KNtP1Pn+Iq1aviXzwajHSOj+/5k1FFFctpI+O1Cqupaemq2F9ZTNtiuIHiLR43AFCuVz1yDVqs7UNe03S3+z32oWllckbgtxOqHHIzgnpwfyq4qaknFanRh41OdezWp8wXEeo+C/ETosjWuo2M2FkjyMEdGGRyCOfcH3r6a8L68viTw/pupB1SSdB5vlhgu8ABsA87Q24fgcEjmvF/jN4i0LxHqVpJpkzXF5bqYZp1BMbrk4AJx0O4jAIIcc8Vy/hnx1rPhGG5i0y5EST4JDoHCMCPmUHIBwMdOh9QCO+pTjNcsj9Ux2XzznCU6jXJVXf8f8ANH0nr3iTSvDMIm1G8hs0wVC5LFiCBhVB3MOR24zXj/iz45XeoQy2ehwHTrdwQbmQ/vznHIwcIeozknpgg15neXlxqFw891PJczvjdJM5ZjgYGSfYCoamEY09i8v4dw+EtOs+eXnt93+f3BRRRVH1YUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABT4ZpLeVJYnaORGDK6EgqRyCD2NMooA2F8Z+II/u65qS/S7k/xp3/AAm3iH/oO6l/4Fyf41i0U23Lc5/q9H+Rfci/fa/qeqRCK81G7u4g24JPOzqD0zgnryfzqhRRQ23ubRjGKtFWCiiikUFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH/9k=>\n";
  
  ptr +="<form action='/Cambio' method='post'>\n";
  ptr += "<h1 style=color:rgb(255,150,0)>T e m p e c</h1>\n";

  if (ONLINE == false)
  {
    ptr += "<a class=\"button button-off\" style='height:10px;width:25px;FONT-SIZE:10pt;BACKGROUND-COLOR: rgb(233,10,10)' href=\"/Offline\">Offline</a>\n";
  }
  else
  {
    ptr += "<a class=\"button button-off\" style='height:10px;width:25px;FONT-SIZE:10pt' href=\"/Online\">Online</a>\n";
    ptr += "<p>Red Wi-fi<br> <input type='text' name='ssid'     style='text-align:center;background-color: #AA11AA;color:rgb(255,150,0);' value=";
    ptr += Strssid;
    ptr += "></p>\n";
    ptr += "<p>Password<br>  <input type='text' name='password' style='text-align:center;background-color: #AA11AA;color:rgb(255,150,0);' value=";
    ptr += Strpass;
    ptr += "></p>\n";
  }
  ptr += "<p>- Setpoint -<br> <input type='number' step='0.1' name='setpoint'       style='height:20px;width:40px;background-color: #AA11AA;color:rgb(255,150,0);'  value=";
  ptr += SetPoint;
  ptr += "></p>\n";
  ptr += "<p>Histeresis +<br> <input type='number' step='0.1' name='histeresis_high' style='height:20px;width:40px;background-color: #AA11AA;color:rgb(255,150,0);' value=";
  ptr += Histeresis;
  ptr += "></p>\n";
  ptr += "<p>Histeresis -<br> <input type='number' step='0.1' name='histeresis_low'  style='height:20px;width:40px;background-color: #AA11AA;color:rgb(255,150,0);' value=";
  ptr += HisN;
  ptr += "></p>\n";

  ptr += "<p><button type='submit' style = 'background-color: #AA11AA;height:40px;width:80px;color:rgb(255,150,0);'>Enviar formulario</button></p>\n";
  ptr += "</form>\n";
  ptr += "</body>\n";
  ptr += "<body style=background-color:#00AA00;>\n";
  ptr += "</body>\n";
  ptr += "</html>\n";
  return ptr;
}//*/
