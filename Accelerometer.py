import smbus
import time
import math
from datetime import datetime
import csv

# Initialize I2C bus
bus = smbus.SMBus(1)
address = 0x18  # I2C address for LIS3DH

# Initialize the sensor
def init_sensor():
    bus.write_byte_data(address, 0x20, 0x27)  # Activate the sensor
    bus.write_byte_data(address, 0x23, 0x00)  # Set accelerometer range

# Read acceleration data
def read_acceleration():
    x = bus.read_byte_data(address, 0x28) | (bus.read_byte_data(address, 0x29) << 8)
    y = bus.read_byte_data(address, 0x2A) | (bus.read_byte_data(address, 0x2B) << 8)
    z = bus.read_byte_data(address, 0x2C) | (bus.read_byte_data(address, 0x2D) << 8)

    # Convert 16-bit values to signed integers
    if x > 32767: x -= 65536
    if y > 32767: y -= 65536
    if z > 32767: z -= 65536

    return x, y, z

# Save acceleration data to a CSV file
def save_data_to_csv(timestamp, x, y, z, total_acceleration):
    with open("acceleration_data.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, x, y, z, total_acceleration])

# Initialize CSV file with header row
def initialize_csv():
    with open("acceleration_data.csv", mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X_Axis", "Y_Axis", "Z_Axis", "Total_Acceleration"])

# Calculate total acceleration
def calculate_total_acceleration(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)

# Main program
init_sensor()
initialize_csv()  # Initialize CSV file
last_saved_time = 0
save_interval = 5  # Save data every 5 seconds

while True:
    x, y, z = read_acceleration()
    total_acceleration = calculate_total_acceleration(x, y, z)

    # Record the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the current timestamp
    current_timestamp = time.time()

    # Print the current data to the console
    print(f"Time: {current_time}, X: {x}, Y: {y}, Z: {z}, Total Acceleration: {total_acceleration:.2f}")

    # If acceleration changes and the save interval has been reached, save to the file
    if total_acceleration > 0 and current_timestamp - last_saved_time > save_interval:
        save_data_to_csv(current_time, x, y, z, total_acceleration)
        last_saved_time = current_timestamp  # Update the last save time

    # Set the detection interval (1 second)
    time.sleep(1)
