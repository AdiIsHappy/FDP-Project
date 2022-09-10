#include <ESP8266WiFi.h>
#include <ros.h>
#include <geometry_msgs/Point.h>


// college 2.4Ghz wifi Setup
// const char *ssid =  "IITMandi_2.4GHz";
// IPAddress server(10, 8, 38, 114);
// const char *pass =  "wifi@iit";

int enA = D2;
int in1 = D3;
int in2 = D4;
int in3 = D5;
int in4 = D6;
int enB = D7;


const int max_speed = 254;

//Aditya's phone hotspot Setup
const char *ssid = "adi";
const char *pass = "GoodToGo";
IPAddress server(192, 168, 219, 72);

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

geometry_msgs::Point input;

void master_data(const geometry_msgs::Point& data){
  input = data;
}
ros::Subscriber<geometry_msgs::Point> sub("master_data", &master_data);


void setup() {
  Serial.begin(9600);
  ConnectToWifi();
  nh.initNode();
  nh.subscribe(sub);
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
}


void loop(){
  // Serial.print(input.x);
  // Serial.print(" ");
  // Serial.print(input.y);
  // Serial.print(" ");
  // Serial.println(input.z);
  Serial.println(input.x == 0 && input.y == 1);
  if      (input.x == 0 && input.y == 1){forward();}
  else if (input.x == 1 && input.y == 1){left();}
  else if (input.x == 1 && input.y == 0){turnLeft();}
  else if (input.x == 1 && input.y == -1){backRight();}
  else if (input.x == 0 && input.y == -1){backward();}
  else if (input.x == -1 && input.y == -1){backLeft();}
  else if (input.x == -1 && input.y == 0){turnRight();}
  else if (input.x == -1 && input.y == 1){right();}
  else {stop();}
  nh.spinOnce();    
}
//   \  |  /
//    \ | /
//     \|/ 
// <--------->
//     /|\
//    / | \
//   /  |  \  
    
void forward(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void left(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void right(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void backward(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void turnRight(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
}

void turnLeft(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}


void backLeft(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
}

void backRight(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
}

void stop(){
  analogWrite(enA, max_speed * input.z);
  analogWrite(enB, max_speed * input.z);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);  
}


