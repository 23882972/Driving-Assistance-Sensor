import smbus
import time

# Initialize I2C bus
bus = smbus.SMBus(2)

# Sensor I2C addresses
SENSOR_ADDRESS_1 = 0x37
SENSOR_ADDRESS_2 = 0x3a
SENSOR_ADDRESS_3 = 0x50  # Third sensor address

def read_sensor():
    try:
        # Read data from the sensors
        data_1 = bus.read_byte(SENSOR_ADDRESS_1)
        data_2 = bus.read_byte(SENSOR_ADDRESS_2)
        data_3 = bus.read_byte(SENSOR_ADDRESS_3)

        # Output raw data for debugging
        print(f"Read data: data_1={hex(data_1)}, data_2={hex(data_2)}, data_3={hex(data_3)}")

        # Determine presence based on the value of data_3
        if data_3 == 0xff:
            return "yes"  # Presence detected
        elif data_3 == 0x00:
            return "no"  # No presence detected
        else:
            return "uncertain"  # Uncertain state, sensor might still be detecting
    except Exception as e:
        print(f"Error reading sensor: {e}")
        return "error"

# Main loop to periodically read sensor data
while True:
    status = read_sensor()
    print(f"Presence status: {status}")
    time.sleep(1)  # Read every second
