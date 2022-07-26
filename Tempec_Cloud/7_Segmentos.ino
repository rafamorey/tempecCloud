void Decodificacion(float t)
{
  boolean mill = false;
  boolean cent = false;
  boolean error = false;
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
    error = true;
  }
}
