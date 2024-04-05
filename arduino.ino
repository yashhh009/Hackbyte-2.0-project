#include <ESP8266WiFi.h>
const char* ssid = "jay110";  
const char* password = "Workbook123";
String apiKey = "E6VWLQ4W851OEAEA";
const char* server = "api.thingspeak.com";

WiFiClient client;

float Level;

void setup()
{
Serial.begin(115200);
delay(10);
Serial.println("Connecting to ");
Serial.println(ssid);
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED)
{
delay(500);
Serial.print(".");
}
Serial.println("");
Serial.println("WiFi connected");
}
void loop()
{
float reading = analogRead(A0);
Level = ((reading/1023)*100);
if (isnan(Level))
{
Serial.println("Failed to read from MQ-2 sensor!");
return;
}
 
if (client.connect(server, 80)) 
{
    String postStr = apiKey;
    postStr +="&field1=";
    postStr += String(Level);
    postStr += "\r\n\r\n";
 
    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(postStr.length());
    client.print("\n\n");
    client.print(postStr);
Serial.print("Gas, Smoke, Air Level: ");
Serial.println(Level);
Serial.println("Data Send to Thingspeak");
}
delay(500);
client.stop();
Serial.println("Waiting...");
delay(6000);
}
