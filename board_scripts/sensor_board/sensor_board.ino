#include <ESP8266WiFi.h>
#include <ros.h>
#include <geometry_msgs/Point.h>
#include <SensorData/sensorData.h>

int front_us_echo = D1;
int back_us_echo = D2;
int front_us_trig = D3;
int back_us_trig = D4;
int left_ir_input = D6;
int right_ir_input = D7;
long duration;
int distance;

// college 2.4Ghz wifi Setup
// const char *ssid =  "IITMandi_2.4GHz";
// IPAddress server(10, 8, 38, 114);
// const char *pass =  "wifi@iit";

//Aditya's phone hotspot Setup
const char *ssid = "adi";
const char *pass = "GoodToGo";
IPAddress server(192, 168, 156, 72);

// client used to connect to wifi
WiFiClient client;

// this is hardware class
class WiFiHardware {

public:
  WiFiHardware(){};

  void init() {
    // do your initialization here. this probably includes TCP server/client setup
    client.connect(server, 11411);
  }

  // read a byte from the serial port. -1 = failure
  int read() {
    // implement this method so that it reads a byte from the TCP connection and returns it
    //  you may return -1 is there is an error; for example if the TCP connection is not open
    return client.read();  //will return -1 when it will works
  }

  // write data to the connection to ROS
  void write(uint8_t *data, int length) {
    // implement this so that it takes the arguments and writes or prints them to the TCP connection
    for (int i = 0; i < length; i++)
      client.write(data[i]);
  }

  // returns milliseconds since start of program
  unsigned long time() {
    return millis();  // easy; did this one for you
  }
};

ros::NodeHandle_<WiFiHardware> nh;

void ConnectToWifi() {
  WiFi.mode(WIFI_STA);
  delay(10);
  Serial.println("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

SensorData::sensorData sensor_data;
ros::Publisher sensor_data_publisher("sensor_data", &sensor_data);

int disance_from_us(int trigPin,int echoPin){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2; 
  return distance;
}

void setup() {
  Serial.begin(9600);
  ConnectToWifi();
  nh.initNode();
  nh.advertise(sensor_data_publisher);
  pinMode(front_us_echo, INPUT);
  pinMode(front_us_trig, OUTPUT);
  pinMode(back_us_echo, INPUT);
  pinMode(back_us_trig, OUTPUT);
  pinMode(left_ir_input, INPUT);
  pinMode(right_ir_input, INPUT);
}


void loop(){
  sensor_data.frontUS = disance_from_us(front_us_trig, front_us_echo);
  Serial.println(sensor_data.frontUS);
  sensor_data.backUS = disance_from_us(back_us_trig, back_us_echo);
  sensor_data.leftIR = digitalRead(left_ir_input);
  sensor_data.rightIR = digitalRead(right_ir_input);
  sensor_data_publisher.publish(&sensor_data);  
  nh.spinOnce();  
}





