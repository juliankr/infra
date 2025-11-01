// CO2 Sensor with ESP32 for Arduino IDE (Built-in Libraries Only)
// Hardware: ESP32 + Sensirion SCD41
// Wiring: SDA=21, SCL=22, VDD=3.3V, GND

#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <SensirionI2cScd4x.h>
#include "configuration.h"  // Include all configuration variables

// Sensor configuration
SensirionI2cScd4x scd4x;
WebServer server(HTTP_PORT);

// Sensor readings
uint16_t co2 = 0;  // Changed from float to uint16_t
float temperature = 0;
float humidity = 0;
bool sensorReady = false;
unsigned long lastMeasurement = 0;

// Status tracking
bool wifiConnected = false;
unsigned long lastWifiCheck = 0;

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  delay(STARTUP_DELAY);
  
  Serial.println("=== CO2 Sensor Starting ===");
  Serial.print("Device: ");
  Serial.println(DEVICE_NAME);
  
  // Initialize I2C
  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  
  // Initialize sensor
  initializeSensor();
  
  // Connect to WiFi
  connectToWiFi();
  
  // Setup web server routes
  setupWebServer();
  
  Serial.println("Setup complete!");
}

void loop() {
  // Handle web server requests
  server.handleClient();
  
  // Check WiFi connection periodically
  if (millis() - lastWifiCheck > WIFI_CHECK_INTERVAL) {
    checkWiFiConnection();
    lastWifiCheck = millis();
  }
  
  // Read sensor data periodically
  if (millis() - lastMeasurement > MEASUREMENT_INTERVAL) {
    readSensorData();
    lastMeasurement = millis();
  }
  
  delay(MAIN_LOOP_DELAY);
}

void initializeSensor() {
  Serial.println("Initializing SCD41 sensor...");
  Serial.println("Checking I2C bus...");
  
  // Check if sensor is connected by scanning I2C
  Wire.beginTransmission(SENSOR_I2C_ADDRESS);
  uint8_t error = Wire.endTransmission();
  if (error == 0) {
    Serial.println("SCD41 sensor found on I2C bus!");
  } else {
    Serial.print("I2C Error: ");
    Serial.println(error);
    Serial.println("Check wiring: SDA->GPIO21, SCL->GPIO22, VDD->3.3V, GND->GND");
  }
  
  scd4x.begin(Wire, SCD40_I2C_ADDR_62);
  
  // Stop potentially previously started measurement
  Serial.println("Stopping any previous measurements...");
  uint16_t errorCode = scd4x.stopPeriodicMeasurement();
  if (errorCode) {
    Serial.print("Error stopping measurement: 0x");
    Serial.println(errorCode, HEX);
  } else {
    Serial.println("Previous measurements stopped successfully");
  }
  
  // Wait a bit before starting new measurement
  delay(SENSOR_INIT_DELAY);
  
  // Start periodic measurement
  Serial.println("Starting periodic measurements...");
  errorCode = scd4x.startPeriodicMeasurement();
  if (errorCode) {
    Serial.print("Error starting measurement: 0x");
    Serial.println(errorCode, HEX);
    Serial.println("Possible causes:");
    Serial.println("- Sensor not connected properly");
    Serial.println("- Wrong I2C address");
    Serial.println("- Sensor power issue");
    sensorReady = false;
  } else {
    Serial.println("SCD41 sensor initialized successfully!");
    Serial.println("Waiting for first measurement (this takes ~5 seconds)...");
    sensorReady = true;
  }
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < WIFI_MAX_ATTEMPTS) {
    delay(WIFI_RETRY_DELAY);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println("\nWiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiConnected = false;
    Serial.println("\nFailed to connect to WiFi!");
  }
}

void checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    if (wifiConnected) {
      Serial.println("WiFi connection lost! Attempting to reconnect...");
      wifiConnected = false;
    }
    connectToWiFi();
  } else if (!wifiConnected) {
    wifiConnected = true;
    Serial.println("WiFi reconnected!");
  }
}

void readSensorData() {
  if (!sensorReady) {
    Serial.println("Sensor not ready");
    return;
  }
  
  uint16_t error;
  bool isDataReady = false;
  
  // Check if data is ready (using correct method name)
  error = scd4x.getDataReadyStatus(isDataReady);
  if (error) {
    Serial.print("Error checking data ready: ");
    Serial.println(error);
    return;
  }
  
  if (!isDataReady) {
    return; // Data not ready yet
  }
  
  // Read measurement (co2 is now uint16_t)
  error = scd4x.readMeasurement(co2, temperature, humidity);
  if (error) {
    Serial.print("Error reading measurement: ");
    Serial.println(error);
  } else if (co2 == 0) {
    Serial.println("Invalid sample detected, skipping.");
  } else {
    // Valid measurement
    Serial.printf("CO2: %d ppm, Temperature: %.2f°C, Humidity: %.1f%%\n", 
                  co2, temperature, humidity);
  }
}

void setupWebServer() {
  // Prometheus metrics endpoint
  server.on("/metrics", HTTP_GET, []() {
    String metrics = generatePrometheusMetrics();
    server.send(200, "text/plain; charset=utf-8", metrics);
  });
  
  // Status endpoint for debugging
  server.on("/", HTTP_GET, []() {
    String html = generateStatusPage();
    server.send(200, "text/html", html);
  });
  
  // Health check endpoint
  server.on("/health", HTTP_GET, []() {
    String status = sensorReady && wifiConnected ? "OK" : "ERROR";
    server.send(200, "text/plain", status);
  });
  
  server.begin();
  Serial.println("HTTP server started on port 80");
}

String generatePrometheusMetrics() {
  String metrics = "";
  
  // Add help and type information
  metrics += "# HELP sensor_co2_ppm CO2 concentration in parts per million\n";
  metrics += "# TYPE sensor_co2_ppm gauge\n";
  metrics += "sensor_co2_ppm " + String((int)co2) + "\n";
  
  metrics += "# HELP sensor_temperature_celsius Temperature in degrees Celsius\n";
  metrics += "# TYPE sensor_temperature_celsius gauge\n";
  metrics += "sensor_temperature_celsius " + String(temperature, TEMPERATURE_DECIMAL_PLACES) + "\n";
  
  metrics += "# HELP sensor_humidity_percent Relative humidity percentage\n";
  metrics += "# TYPE sensor_humidity_percent gauge\n";
  metrics += "sensor_humidity_percent " + String(humidity, HUMIDITY_DECIMAL_PLACES) + "\n";
  
  // Add device status metrics
  metrics += "# HELP sensor_ready Sensor initialization status\n";
  metrics += "# TYPE sensor_ready gauge\n";
  metrics += "sensor_ready " + String(sensorReady ? 1 : 0) + "\n";
  
  metrics += "# HELP sensor_wifi_connected WiFi connection status\n";
  metrics += "# TYPE sensor_wifi_connected gauge\n";
  metrics += "sensor_wifi_connected " + String(wifiConnected ? 1 : 0) + "\n";
  
  // Debug output to serial
  Serial.print("Metrics - CO2: ");
  Serial.print(co2);
  Serial.print(", Temp: ");
  Serial.print(temperature);
  Serial.print(", Humidity: ");
  Serial.println(humidity);
  
  return metrics;
}

String generateStatusPage() {
  String html = "<!DOCTYPE html><html><head><title>CO2 Sensor Status</title></head><body>";
  html += "<h1>CO2 Sensor Status</h1>";
  html += "<p><strong>WiFi:</strong> " + String(wifiConnected ? "Connected" : "Disconnected") + "</p>";
  html += "<p><strong>IP Address:</strong> " + WiFi.localIP().toString() + "</p>";
  html += "<p><strong>Sensor:</strong> " + String(sensorReady ? "Ready" : "Not Ready") + "</p>";
  html += "<h2>Current Readings:</h2>";
  html += "<p><strong>CO2:</strong> " + String(co2, 0) + " ppm</p>";
  html += "<p><strong>Temperature:</strong> " + String(temperature, TEMPERATURE_DECIMAL_PLACES) + " °C</p>";
  html += "<p><strong>Humidity:</strong> " + String(humidity, HUMIDITY_DECIMAL_PLACES) + " %</p>";
  html += "<p><a href='/metrics'>Prometheus Metrics</a></p>";
  html += "<p><em>Last updated: " + String(millis() / 1000) + "s since boot</em></p>";
  html += "</body></html>";
  return html;
}