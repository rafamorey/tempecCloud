void temperatura()
{
    if(millis() - lecturaMillis >= intervalo)
  {
    SENSOR_IN.requestTemperatures();
    SENSOR_OUT.requestTemperatures();
    lastemperaturaIn = temperaturaIn;
    if(Termometrica == "C")
    {
      temperaturaIn = SENSOR_IN.getTempCByIndex(0);
      temperaturaOut = SENSOR_OUT.getTempCByIndex(0);
    }
    else if(Termometrica == "F")
    {
      temperaturaIn = SENSOR_IN.getTempFByIndex(0);
      temperaturaOut = SENSOR_OUT.getTempFByIndex(0);
    }
    Serial.print("TEMPERATURA INTERIOR: ");
    Serial.println(temperaturaIn);
    Serial.print("TEMPERATURA EXTERIOR: ");
    Serial.println(temperaturaOut);
    Serial.print("VOLTAJE EN 21: ");
    voltaje = digitalRead(DIVISOR);
    Serial.println(voltaje);
    //temperaturaEx = sensor.getTempCByIndex(1);
    //if(temperaturaIn != lastemperaturaIn)
    //{
     /* Decodificacion(temperaturaIn);
      lastemperaturaIn = temperaturaIn;*/
   // }
    lecturaMillis = millis();
  }
  
  /*if(cambio == false)
  {//*/
    if(temperaturaIn >= (SetPoint+(Histeresis/2)))
    {
      portiempo(300000, 300000);
      COOLING = true;
      HEATING = false;
    }
    else if(temperaturaIn <= (SetPoint + 0.2) && temperaturaIn > SetPoint && COOLING == true)
    {
      portiempo(120000, 300000);
      COOLING = true;
      HEATING = false;
      NEUTRAL = true;
      parpadeo = false;
      SIM = 0;
    }
    else if((temperaturaIn <= SetPoint && COOLING == true) || (temperaturaIn >= SetPoint && HEATING == true))
    {
      portiempo(0, 300000);
      COOLING = false;
      HEATING = false;
      NEUTRAL = true;
      SIM = 0;
      parpadeo = false;
    }
    else if(temperaturaIn >= (SetPoint - 0.2) && temperaturaIn < SetPoint && HEATING == true)
    {
      portiempo(0, 300000);
      COOLING = false;
      HEATING = true;
      NEUTRAL = true;
      SIM = 0;
      parpadeo = false;
    }
    else if(temperaturaIn <= (SetPoint - (Histeresis / 2)))
    {
      portiempo(0, 300000);
      COOLING = false;
      HEATING = true;
      NEUTRAL = false;
    }
  crear();
  alertas();
}


void crear()
{
  //SENSOR_OUT.requestTemperatures();
  //temperaturaOut = SENSOR_OUT.getTempCByIndex(0);
  //TIPO/ID/TEMPERATURA INTERIOR/TEMPERATURA EXTERIOR/OUT0/OUT1
  MENSAJE = "10/";
  MENSAJE += ID;
  MENSAJE += "/";
  MENSAJE += temperaturaIn;
  MENSAJE += "/";
  MENSAJE += temperaturaOut;
  /*  MENSAJE += "/1/";
  MENSAJE += "0";//*/
}

void crearveinte()
{
  VEINTE = "20/";
  VEINTE += ID;
  VEINTE += "/";
  VEINTE += "OVERLORD";/*NOMBRE QUE TENDRA EL DISPOSITIVO*/
  VEINTE += "/";
  VEINTE += SetPoint;
  VEINTE += "/";
  VEINTE += Histeresis;
  VEINTE += "/";
  VEINTE += HisN;
  strcpy(msgIn,VEINTE.c_str());
  client.publish(TOPIC,msgIn);
  twenty = false;
}


void alertas()
{
  if(temperaturaIn >= (SetPoint + Warning_heat))
  {
    //ENVIAR ALERTA AL SERVIDOR(QUE SOLO SERA ENVIAR LA TEMPERATURA)
    digitalWrite(WAR_HEAT,HIGH);
    SIM = 1;
    parpadeo = true;
  }
  else if(temperaturaIn <= (SetPoint - Warning_cold))
  {
    digitalWrite(WAR_COOL,HIGH);
    SIM = 2;
    parpadeo = true;
  }
  
  if(temperaturaIn < (SetPoint + Histeresis) && temperaturaIn > (SetPoint - Histeresis))
  {
    parpadeo = false;
    SIM = 0;
  }
  
}


void portiempo(unsigned long ON, unsigned long OF)
{
  if(ON == 0)
  {
    digitalWrite(OUT_COOL,LOW);
    digitalWrite(OUT_HEAT,LOW);
  }
  else
  {
    if(millis() - activacionMillis <= (ON + OF))
    {
      if(millis() - activacionMillis > ON)
      {
        digitalWrite(OUT_COOL,LOW);
        digitalWrite(OUT_HEAT,LOW);
      }
      else
      {
        digitalWrite(OUT_COOL,HIGH);
        digitalWrite(OUT_HEAT,LOW);
      }
    }
    else
    {
      activacionMillis = millis();
    }
  }
}
