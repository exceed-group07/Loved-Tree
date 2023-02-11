#include <Arduino.h>
#include <WiFi.h>
#include <DHT.h>
#include <DHT_U.h>
#include <Adafruit_Sensor.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#define DHTPIN 33
#define DHTTYPE DHT11
#define RED1 19
#define RED2 21
#define YELLOW 5
#define GREEN 18
#define LDR 39
TaskHandle_t Taskget = NULL;
TaskHandle_t Task2 = NULL;
void gettemp(void *param);

// Sensor pins 
#define sensorPower 14
#define sensorPin 32
DHT_Unified dht(DHTPIN, DHTTYPE);
uint32_t delayMS;

int Temp , HmdtAir , moisture , LDR_value;
int status_temp, status_water, status_humid, status_dehumid, intensity, color; 
int TempTarget = 27;
int HmdtTarget = 70;

// Right RGB
int redpinR = 2;
int bluepinR = 15;
int greenpinR = 0; 
// Left RGB
int redpinL = 25;
int bluepinL = 26;
int greenpinL = 27;

int val;
const char *ssid = "nitro 5";
const char *password = "12345687";
const String baseUrl = "https://ecourse.cpe.ku.ac.th/exceed07/";
int readSensor();

void Connect_Wifi() 
{
      WiFi.begin(ssid, password);
      Serial.print("Connecting to WiFi");
      while (WiFi.status() != WL_CONNECTED)
      {
        delay(500);
        Serial.print(".");
      }
      Serial.print("SUCCESS! IP = ");
      Serial.println(WiFi.localIP());
}

int readSensor() 
{
  digitalWrite(sensorPower, HIGH);  // Turn the sensor ON
  delay(10);              // Allow power to settle
  int val = analogRead(sensorPin);  // Read the analog value form sensor
  digitalWrite(sensorPower, LOW);   // Turn the sensor OFF
  return val;             // Return analog moisture value
}

void GET() 
{
    const String url = baseUrl + "hardware";
    String payload;
    DynamicJsonDocument doc(2048);
    HTTPClient http;
    http.begin(url);
    int httpCode = http.GET();
    Serial.println(httpCode);
    if (httpCode >= 200 && httpCode < 300) 
    {
        Serial.println("GET SUCCESS");
        payload = http.getString();
        deserializeJson(doc, payload);
        // actions on doc
        status_temp = doc["status_temp"].as<int>();
        status_water = doc["status_water"].as<int>();
        status_humid = doc["status_humid"].as<int>();
        status_dehumid = doc["status_dehumid"].as<int>();
        intensity = doc["intensity"].as<int>();
        color = doc["color"].as<int>();
    } 
    else 
    {
        Serial.println("GET ERROR");
    }
}
void PUT()
{
    const String url = baseUrl + "hardwareupdate";
    DynamicJsonDocument doc(2048);
    String json;
    // populate doc
    doc["tree_id"] = 0;
    doc["humid_soil_now"] = moisture;
    doc["temp_now"] = Temp;
    doc["humid_air_now"] = HmdtAir;
    doc["intensity_now"] = LDR_value;
    serializeJson(doc, json);
    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.PUT(json);
    if (httpCode >= 200 && httpCode < 300) 
    {
        Serial.println("PUT SUCCESS");
    } 
    else 
    {
        Serial.println("PUT ERROR");
    }
}

void setup()
{
  Serial.begin(9600);
  Connect_Wifi();
  //AIR
  // Initialize device.
  dht.begin();

  sensor_t sensor;
  // Set delay between sensor readings based on sensor details.
  delayMS = sensor.min_delay / 1000;

  //SOIL
  pinMode(sensorPower, OUTPUT);
  // Initially keep the sensor OFF
  digitalWrite(sensorPower, LOW);


  //RGB
  pinMode(redpinL, OUTPUT);
  pinMode(bluepinL, OUTPUT);
  pinMode(greenpinL, OUTPUT);
  pinMode(redpinR, OUTPUT);
  pinMode(bluepinR, OUTPUT);
  pinMode(greenpinR, OUTPUT);


  //LDR
  ledcSetup(0, 5000, 8);
  ledcAttachPin(RED1, 0);
  ledcSetup(1, 5000, 8);
  ledcAttachPin(RED2, 1);
  ledcSetup(2, 5000, 8);
  ledcAttachPin(YELLOW, 2);
  ledcSetup(3, 5000, 8);
  ledcAttachPin(GREEN, 3);
  pinMode(LDR, INPUT);

  //task
  xTaskCreatePinnedToCore(gettemp,"gettemp",20000,NULL,1,&Taskget,0);
}

void gettemp(void *param){
  while(1){
    // GET
  GET();
  //AIR
  delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) 
  {
    Serial.println(F("Error reading temperature!"));
  }
  else 
  {
    Serial.print(F("Temperature : "));
    Temp = event.temperature;
    Serial.print(event.temperature);
    Serial.println(F("°C"));
  }
  // Get humidity event and print its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) 
  {
    Serial.println(F("Error reading humidity!"));
  }
  else 
  {
    Serial.print(F("Humidity : "));
    HmdtAir = event.relative_humidity;
    Serial.print(event.relative_humidity);
    Serial.println(F("%"));
  }


  //SOIL
    //get the reading from the function below and print it
  moisture = readSensor();
  Serial.print("moisture[0 - 4095] : ");
  Serial.println(moisture);
  delay(1000);  
  Serial.println();


  //RGB
    {
      //RED
      if (color == 0)
      {
        // RIGHT
        Serial.print("RED Right : ");
        Serial.println(intensity);
        analogWrite(2, intensity); //red
        analogWrite(15, 0); //blue
        analogWrite(0, 0);//green
        // LEFT
        Serial.print("RED Left : ");
        Serial.println(intensity);
        analogWrite(25, intensity); //red
        analogWrite(26, 0); //blue
        analogWrite(27, 0); //green
        delay(1000);
      }

      //GREEN
      if (color == 1)
      {
        // RIGHT
        Serial.print("RED Right : ");
        Serial.println(intensity);
        analogWrite(2, 0);
        analogWrite(15, 0); 
        analogWrite(0, intensity); 
        // LEFT
        Serial.print("RED Left : ");
        Serial.println(intensity);
        analogWrite(25, 0);
        analogWrite(26, 0); 
        analogWrite(27, intensity); 
        delay(1000);
      }


      //BLUE
      if (color == 2)
      {
        // RIGHT
        Serial.print("RED Right : ");
        Serial.println(intensity);
        analogWrite(2, 0);
        analogWrite(15, intensity); 
        analogWrite(0, 0);
        // LEFT
        Serial.print("RED Left : ");
        Serial.println(intensity);
        analogWrite(25, 0);
        analogWrite(26, intensity); 
        analogWrite(27, 0); 
        delay(1000);  
      }
    }

  //LED
  // RED2
  Serial.print("status_temp [RED2] : ");
  Serial.println(status_temp);
  if (status_temp == 0)
  {
    ledcWrite(1, 0);
  }
  else
  {
    ledcWrite(1, 255);
  }

  // YELLOW
  Serial.print("status_water [YELLOW] : ");
  Serial.println(status_water);
  if (status_water == 0)
  {
    ledcWrite(2, 0);
  }
  else
  {
    ledcWrite(2, 255);
  }

  // GREEN
  Serial.print("status_humid [GREEN] : ");
  Serial.println(status_humid);
  if (status_humid == 0)
  {
    ledcWrite(3, 0);
  }
  else
  {
    ledcWrite(3, 255);
  }
  // RED1
  Serial.print("status_dehumid [RED1] : ");
  Serial.println(status_dehumid);
  if (status_dehumid == 0)
  {
    ledcWrite(0, 0);
  }
  else
  {
    ledcWrite(0, 255);
  }

    //LDR
    Serial.print("LDR [0 - 100] = ");
    LDR_value = map(analogRead(LDR),1000,4095,0,100);
    Serial.println(LDR_value);
    delay(1000);
  }
}


void loop()
{
  PUT();
}