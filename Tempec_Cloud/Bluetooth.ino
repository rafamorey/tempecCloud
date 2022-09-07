/*void bluetooth()
{
  if(SerialBT.available())
  {
    //String mensaje = "";
    int largo = 0;
    while(SerialBT.available())
    {
      char datos = SerialBT.read();
      if(datos != '\n')
      {
        Mensaje[largo] = datos;
        largo++;
      }
    }
    if(Mensaje[0] == '0')
    {
      desmenuzado(2);
    }
    else if(Mensaje[0] == '1')
    {
      WIFI = true;
      desmenuzado(0);
    }
    else
    {
    }
  }
}*/


/*--void desmenuzado(int inicio)
{
    /* VARIABLES PARA LA UNION DE CARACTERES
     * red = NOMBRE DE LA RED WIFI;
     * pas = CONTRASEÑA DE LA RED WIFI
     * poi = SET POINT
     * pos = Histeresis POSITIVA
     * neg = Histeresis NEGATIVA
     * nom = NOMBRE DEL BLUETOOTH
     * sit = SITIO
    */
 /*-- int prime = 0;
  String red,pas,poi,pos,neg;
  for(int x = inicio; x <= 5; x++)
  {
    prime++;
    switch (x)
    {
      case 0:
      for(int w = prime+1; w <= (prime + Mensaje[prime]); w++)
      {
        red += char(Mensaje[w]);
      }
      prime += Mensaje[prime];
      break;
      case 1:
      for(int w = prime+1; w <= (prime + Mensaje[prime]); w++)
      {
        pas += char(Mensaje[w]);
      }
      prime += Mensaje[prime];
      break;
      case 2:
      for(int w = prime+1; w <= (prime + Mensaje[prime]); w++)
      {
        poi += char(Mensaje[w]);
      }
      SetPoint = poi.toFloat();
      prime += Mensaje[prime];
      break;
      case 3:
      for(int w = prime+1; w <= (prime + Mensaje[prime]); w++)
      {
        pos += char(Mensaje[w]);
      }
      Histeresis = pos.toFloat();
      prime += Mensaje[prime];
      break;
      case 4:
      for(int w = prime+1; w <= (prime + Mensaje[prime]); w++)
      {
        neg += char(Mensaje[w]);
      }
      HisN = pos.toFloat();
      prime += Mensaje[prime];
      break;
      case 5:
      for(int w = prime+1; w <= (prime + Mensaje[prime]); w++)
      {
        nameBlue += char(Mensaje[w]);
      }
      prime += Mensaje[prime];
      default:
      break;
    }
  }
  if(WIFI)
  {
    //EEPROM.put()
  }
  else
  {
    /*NO GUARDAR DATOS DE WIFI*/
  /*--}
}//*/
