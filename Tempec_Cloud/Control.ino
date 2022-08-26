void temperatura()
{
    if(millis() - lecturaMillis >= intervalo)
  {
    sensor.requestTemperatures();
    temperaturaIn = sensor.getTempCByIndex(0);
    Serial.print("TEMPERATURA: ");
    Serial.println(temperaturaIn);
    //temperaturaEx = sensor.getTempCByIndex(1);
    //if(temperaturaIn != lastemperaturaIn)
    //{
     /* Decodificacion(temperaturaIn);
      lastemperaturaIn = temperaturaIn;*/
   // }
    lecturaMillis = millis();
  }
  
  if(temperaturaIn >= (SetPoint+Histerisis))
  {
    digitalWrite(OUT_COOL,HIGH);
    digitalWrite(OUT_HEAT,LOW);
    COOLING = true;
    HEATING = false;
  }
  else if(temperaturaIn <= SetPoint && COOLING == true)
  {
    digitalWrite(OUT_COOL,LOW);
    digitalWrite(OUT_HEAT,LOW);
    COOLING = false;
    HEATING = false;
  }
  else if(temperaturaIn <= (SetPoint-Histerisis))
  {
    digitalWrite(OUT_COOL,LOW);
    digitalWrite(OUT_HEAT,HIGH);
    COOLING = false;
    HEATING = true;
  }
  else if(temperaturaIn >= SetPoint && HEATING == true)
  {
    digitalWrite(OUT_COOL,LOW);
    digitalWrite(OUT_HEAT,LOW);
    COOLING = false;
    HEATING = false;
  }
  crear();
}


void crear()
{
  //TIPO/ID/TEMPERATURA INTERIOR/TEMPERATURA EXTERIOR/OUT0/OUT1
  MENSAJE = "10/";
  MENSAJE += "AAAA/";
  MENSAJE += temperaturaIn;
  MENSAJE += "/25.00/";
  MENSAJE += "1/";
  MENSAJE += "0";
}
