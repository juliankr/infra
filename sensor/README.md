# CO₂ Sensor with ESP32

This project implements a battery-powered air quality monitoring device using an ESP32 and Sensirion SCD41 sensor. The device measures CO₂, temperature, and humidity, then serves the data in Prometheus-compatible format.

## Hardware Setup

### Components
- ESP32 DevKit v1
- Sensirion SCD41 CO₂/Temperature/Humidity sensor
- USB power supply (power bank or wall adapter)

### Wiring
```
SCD41 Pin → ESP32 Pin
VDD       → 3.3V
GND       → GND
SDA       → GPIO 21
SCL       → GPIO 22
```

## Software Setup

### Prerequisites
- [Arduino IDE 2.0+](https://www.arduino.cc/en/software) 
- ESP32 board support in Arduino IDE
- SensirionI2CScd4x library installed

### Quick Setup

1. **Create configuration file:**
   ```bash
   cp configuration.h.template configuration.h
   ```

2. **Edit `configuration.h`** with your settings:
   ```cpp
   const char* WIFI_SSID = "YourWiFiName";
   const char* WIFI_PASSWORD = "YourWiFiPassword";
   const char* DEVICE_NAME = "co2-sensor-01";
   ```

3. **Upload to ESP32:**
   - Open `sensor.ino` in Arduino IDE
   - Select your ESP32 board and port
   - Click Upload

4. **Monitor serial output:**
   - Open Serial Monitor (115200 baud)
   - Note the IP address for Prometheus configuration

### Security
- **All configuration** is stored in `configuration.h` (excluded from git)
- **Template file** `configuration.h.template` is committed (without sensitive data)
- **The `.gitignore` file** ensures your credentials never get committed

## Configuration Options

All settings are centralized in `configuration.h`:

### WiFi Configuration
- `WIFI_SSID` - Your WiFi network name
- `WIFI_PASSWORD` - Your WiFi password

### Device Configuration
- `DEVICE_NAME` - Friendly name for your sensor
- `HTTP_PORT` - Web server port (default: 80)

### Timing Configuration (milliseconds)
- `MEASUREMENT_INTERVAL` - How often to read sensor (default: 30 seconds)
- `WIFI_CHECK_INTERVAL` - How often to check WiFi connection (default: 30 seconds)
- `SERIAL_BAUD_RATE` - Serial communication speed (default: 115200)
- `STARTUP_DELAY` - Initial startup delay (default: 1000ms)
- `SENSOR_INIT_DELAY` - Delay between sensor operations (default: 500ms)

### Hardware Configuration
- `I2C_SDA_PIN` - I2C SDA pin (default: GPIO21)
- `I2C_SCL_PIN` - I2C SCL pin (default: GPIO22)
- `SENSOR_I2C_ADDRESS` - SCD41 I2C address (default: 0x62)

### WiFi Connection Settings
- `WIFI_MAX_ATTEMPTS` - Maximum connection attempts (default: 20)
- `WIFI_RETRY_DELAY` - Delay between attempts (default: 500ms)

### Display Settings
- `TEMPERATURE_DECIMAL_PLACES` - Temperature precision (default: 2)
- `HUMIDITY_DECIMAL_PLACES` - Humidity precision (default: 1)

## API Endpoints

### `/metrics` - Prometheus Metrics
Returns sensor data in Prometheus text exposition format:
```
sensor_co2_ppm 415
sensor_temperature_celsius 23.7
sensor_humidity_percent 48.5
sensor_ready 1
sensor_wifi_connected 1
```

### `/` - Status Page
HTML status page showing current readings and device status.

### `/health` - Health Check
Returns "OK" if sensor and WiFi are working, "ERROR" otherwise.

## Troubleshooting

### Common Issues
1. **Configuration file not found**: Run `cp configuration.h.template configuration.h`
2. **Sensor not ready**: Check I²C wiring (SDA/SCL connections)
3. **WiFi connection failed**: Verify credentials in `configuration.h`
4. **Invalid measurements**: Wait 2-3 minutes after power-on for sensor stabilization

### Serial Monitor Output
Monitor via Arduino IDE Serial Monitor (115200 baud) for:
- Device configuration information
- Sensor initialization status
- WiFi connection attempts
- Real-time sensor readings
- Error messages

## Specifications

- **Measurement Range**: 
  - CO₂: 400-40,000 ppm
  - Temperature: -40 to +125°C
  - Humidity: 0-100% RH
- **Accuracy**:
  - CO₂: ±(40 ppm + 5% of reading)
  - Temperature: ±0.8°C
  - Humidity: ±6% RH
- **Update Rate**: Configurable (default: 30 seconds)
- **Power Consumption**: ~15mA during operation