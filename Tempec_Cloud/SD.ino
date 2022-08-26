void enviarDatosSD()
{
  readFile(SD, "/SILOS.txt");
  deleteFile(SD, "/SILOS.txt");
}

void readFile(fs::FS &fs, const char * path){
    //Serial.printf("Reading file: %s\n", path);

    File file = fs.open(path);
    if(!file){
        //Serial.println("Failed to open file for reading");
        /*Agregar un indicador que el archivo no quizo abrirse*/
        return;
    }

    //Serial.print("Read from file: ");
    while(file.available()){
      Serial.write(file.read());
      //sendTime = millis();
    }
    file.close();
}

void deleteFile(fs::FS &fs, const char * path)
{
  //Serial.printf("Deleting file: %s\n", path);
  if(fs.remove(path))
  {
    //Serial.println("File deleted");
  }
  else
  {
   // Serial.println("Delete failed");
   }
}
