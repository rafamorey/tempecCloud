void temperatura()
{
    if(millis() - lecturaMillis >= intervalo)
  {
    SENSOR_IN.requestTemperatures();
    temperaturaIn = SENSOR_IN.getTempCByIndex(0);
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
  //SENSOR_OUT.requestTemperatures();
  //temperaturaOut = SENSOR_OUT.getTempCByIndex(0);
  //TIPO/ID/TEMPERATURA INTERIOR/TEMPERATURA EXTERIOR/OUT0/OUT1
  MENSAJE = "10/";
  MENSAJE += ID;
  MENSAJE += "/";
  MENSAJE += temperaturaIn;
  MENSAJE += "/";
  MENSAJE += temperaturaOut;
  MENSAJE += "/1/";
  MENSAJE += "0";
}

void crearveinte()
{
  VEINTE = "20/";
  VEINTE += ID;
  VEINTE += "/";
  VEINTE += "NOMBRE";/*NOMBRE QUE TENDRA EL DISPOSITIVO*/
  VEINTE += "/";
  VEINTE += SetPoint;
  VEINTE += "/";
  VEINTE += Histerisis;
  VEINTE += "/";
  VEINTE += HisN;
}
