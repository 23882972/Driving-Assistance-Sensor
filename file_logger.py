from datetime import datetime
import csv

# Class for CSV files
class FileLogger:
    # Initializing the object
    def __init__(self, data_format='txt'):
        # Adding file paths and formats
        self.data_format = data_format
        self.data_file = "/home/csseiot/final/Driving-Assistance-Sensor/sensor_data." + data_format
        self.alert_log_file = "/home/csseiot/final/Driving-Assistance-Sensor/alert_log." + data_format
        self.data_writer = None
        self.alert_writer = None
        self.open_files()
    
    # Opening the files
    def open_files(self):
        if self.data_format == 'csv':
            self.data_file_handle = open(self.data_file, mode="a", newline='')
            self.alert_log_file_handle = open(self.alert_log_file, mode="a", newline='')
            self.data_writer = csv.writer(self.data_file_handle)
            self.alert_writer = csv.writer(self.alert_log_file_handle)

            # Writing the headers if the file is empty
            if self.data_file_handle.tell() == 0:
                self.data_writer.writerow(["Timestamp", "X_Axis", "Y_Axis", "Z_Axis", "Total_Acceleration", "Distance", "Is_Raining"])
            if self.alert_log_file_handle.tell() == 0:
                self.alert_writer.writerow(["Timestamp", "Code", "Alert_Reason"])
        elif self.data_format == 'txt':
            self.data_file_handle = open(self.data_file, mode="a")
            self.alert_log_file_handle = open(self.alert_log_file, mode="a")
    
    # Saving the data of sensors into the row
    def save_data(self, timestamp, x, y, z, total_accel, distance, is_raining):
        if self.data_format == 'csv':
            self.data_writer.writerow([timestamp, x, y, z, total_accel, distance, is_raining])
        elif self.data_format == 'txt':
            self.data_file_handle.write(f"{timestamp}\t{x}\t{y}\t{z}\t{total_accel}\t{distance}\t{is_raining}\n")
        self.data_file_handle.flush()

    # Saving the alert logs
    def save_alert_log(self, timestamp, code, reason):
        if self.data_format == 'csv':
            self.alert_writer.writerow([timestamp, code, reason])
        elif self.data_format == 'txt':
            self.alert_log_file_handle.write(f"{timestamp}\t{code}\t{reason}\n")
            self.alert_log_file_handle.flush()

    # Closing the files
    def close_files(self):
        self.data_file_handle.close()
        self.alert_log_file_handle.close()
