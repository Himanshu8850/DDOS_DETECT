import time
from scapy.all import *
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import numpy as np
scaler=MinMaxScaler() 

def capture_and_extract():
    # Capture packets (adjust filter as needed)
    packets = sniff(count=1000)

    # Initialize dictionaries to store extracted data for each IP address
    ip_data = {}

    # Iterate through captured packets
    for packet in packets:
        # Check if the packet contains the IP layer
        if IP in packet:
            # Extract required information from the packet
            ip_src = packet[IP].src
            packet_length = len(packet)
            packet_time = packet.time


            # ////////////////////////////////////////////////////////////////////


            # Update or initialize data for the IP address
            if ip_src in ip_data:
                ip_data[ip_src]['TPC'] += 1
                ip_data[ip_src]['TPL'] += packet_length
                ip_data[ip_src]['TPT'] += packet_time
                ip_data[ip_src]['PL_list'].append(packet_length)
                ip_data[ip_src]['PT_list'].append(packet_time)
                
            else:
            # ////////////////////////////////////////////////////////////////////
                ip_data[ip_src] = {
                    'TPC': 1,
                    'TPL': packet_length,
                    'TPT': packet_time,
                    'PL_list': [packet_length],
                    'PT_list': [packet_time]
                }

    # Calculate additional metrics for each IP address
    for ip, data in ip_data.items():
        # Calculate average
        data['APL'] = data['TPL'] / data['TPC'] if data['TPC'] > 0 else 0
        data['APT'] = data['TPT'] / data['TPC'] if data['TPC'] > 0 else 0  

        # Calculate variance and differences for packet lengths (PL)
        data['PLV'] = sum((pl - data['APL']) ** 2 for pl in data['PL_list']) / len(data['PL_list']) if len(data['PL_list']) > 0 else 0
        data['ALD'] = sum(abs(data['PL_list'][i+1] - data['PL_list'][i]) for i in range(len(data['PL_list']) - 1)) / (len(data['PL_list']) - 1) if len(data['PL_list']) > 1 else 0

        # Calculate variance and differences for packet times (PT)
        data['PTV'] = sum((pt - data['APT']) ** 2 for pt in data['PT_list']) / len(data['PT_list']) if len(data['PT_list']) > 0 else 0
        data['ATD'] = sum(abs(data['PT_list'][i+1] - data['PT_list'][i]) for i in range(len(data['PT_list']) - 1)) / (len(data['PT_list']) - 1) if len(data['PT_list']) > 1 else 0
        data['APT'] = data['APT']
        data['TPT'] = data['TPT']
        # Calculate rate and Kb/s (you need to adjust this calculation based on your requirements)
        # Here, we'll set them to 0 for simplicity
        data['Rate'] = 0
        if data['TPT'] > 0:
            data['Rate'] = data['TPL'] / data['TPT']
        else:
            data['Rate'] = 0

    # Iterate over each IP address in ip_data
    for ip, data in ip_data.items():
        # Round up numerical values and list values in the data dictionary to 3 decimal places
        if data['TPT'] > 0:
            data['Rate'] = data['TPL'] / data['TPT']
        # print(ip)
        # /////////////////////////////////////////////////////////////
        # if(ip=='192.168.109.157'):
        #     data['Attack'] ="Flood"
        # else:
        #     data['Attack']="Benign"

        for key in data:
            if isinstance(data[key], list):
                data[key] = [round(value, 3) for value in data[key]]
            else:
                if not isinstance(data[key], str):
                    data[key] = round(data[key], 3)

    return ip_data

# Main function to capture packets, extract data, and create DataFrame
def main():
    model = joblib.load('model4.pkl')
    # Set the total duration for capturing data (in seconds)
    total_duration = 1200 # 1 minute
    capture_interval = 20  # 20 seconds

    start_time = time.time()
    # ///////////////////


    while time.time() - start_time < total_duration:


    # ///////////////////
        # Capture and extract data
    # print()
        df=pd.DataFrame()
        while len(df)==0:
            ip_data = capture_and_extract()

            # Create DataFrame from the extracted data and arrange columns
            df = pd.DataFrame(ip_data.values(), index=ip_data.keys())
        
        df = df[['TPC', 'TPL', 'APL', 'PLV', 'ALD', 'TPT', 'APT', 'ATD', 'PTV', 'Rate']]
        print(df.head())
        # df=df.iloc[:,1:]
        df = df.reset_index(inplace=False)
        # df.reset_index(inplace=True)
        df.rename(columns={'index': 'SRC'}, inplace=True)
        # z=df['SRC']
        df.columns = df.columns.str.strip()
    # Append data to CSV file
        # df.to_csv('extracted_data.csv', mode='a', header=False)
        # print(df)
        # print(dftest.head())
        # print(dftest.iloc[1:, 1:])
        # dat=np.array(dftest)
        # print(dat)
        x = model.predict(df.drop(columns=['SRC']))
        df['Label']=x
        print(df)
        # dat=np.column_stack((dat,x))
        # print(dat)
        # df['src']=lab
        # df['Label']=x
        # print(df.iloc[:,-2:])
    # Print the DataFrame
    # df.iloc[:,1:-1]=scaler.fit_transform(df.iloc[:,1:-1])

        # Clear the DataFrame
        df = pd.DataFrame()

# Execute the main function
if __name__ == "__main__":
    main()
