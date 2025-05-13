from scapy.all import *
import pandas as pd

# Function to capture packets and extract required information
def capture_and_extract():
    # Capture packets (adjust filter as needed)
    packets = sniff(count=10000)
    
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

            # Update or initialize data for the IP address
            if ip_src in ip_data:
                ip_data[ip_src]['TPC'] += 1
                ip_data[ip_src]['TPL'] += packet_length
                ip_data[ip_src]['TPT'] += packet_time
                ip_data[ip_src]['PL_list'].append(packet_length)
                ip_data[ip_src]['PT_list'].append(packet_time)
            else:
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
        data['APT'] = data['APT'] / 10000000000
        data['TPT'] = data['TPT'] / 10000000
        # Calculate rate and Kb/s (you need to adjust this calculation based on your requirements)
        # Here, we'll set them to 0 for simplicity
        data['Rate'] = 0
        if data['TPT'] > 0:
            data['Rate'] = data['TPL'] / data['TPT']
        else:
            data['Rate'] = 0
    # Iterate over each IP address in ip_data
    # Iterate over each IP address in ip_data
    for ip, data in ip_data.items():
        # Round up numerical values and list values in the data dictionary to 3 decimal places
        if data['TPT'] > 0:
            data['Rate'] = data['TPL'] / data['TPT']

        for key in data:
            if isinstance(data[key], list):
                # Round up each value in the list to 3 decimal places
                data[key] = [round(value, 3) for value in data[key]]
            else:
                # Round up numerical values to 3 decimal places
                data[key] = round(data[key], 3)


        
    return ip_data

# Main function to capture packets, extract data, and create DataFrame
def main():
    # Capture and extract data
    ip_data = capture_and_extract()
    
    # Create DataFrame from the extracted data and arrange columns
    df = pd.DataFrame(ip_data.values(), index=ip_data.keys())
    df = df[['TPC', 'TPL', 'APL', 'PLV', 'ALD', 'TPT', 'APT', 'ATD', 'PTV', 'Rate']]
    df.to_csv('extracted_data.csv')
    # Print the DataFrame
    print(df)

# Execute the main function
if __name__ == "__main__":
    main()
