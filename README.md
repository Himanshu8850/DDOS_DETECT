# 🛡️ Real-Time DDoS Attack Detection with Scapy and Machine Learning

This project detects Distributed Denial of Service (DDoS) attacks in real-time using packet capture (`scapy`), feature extraction, and classification using a trained `RandomForestClassifier`.

---

## 📂 Files

### `trainer.py`

- Loads and preprocesses a CSV dataset (`extracted_data.csv`)
- Trains a Random Forest Classifier
- Saves the trained model to `model4.pkl`

### `DDOS_detect.py`

- Captures live network traffic using Scapy
- Extracts per-IP statistics and computes key features
- Uses the saved model to classify traffic as **Benign** or **Malicious**
- Displays the results for each active IP

---

## 🛠️ Features Extracted

- Total Packet Count (TPC)
- Total Packet Length (TPL)
- Average Packet Length (APL)
- Packet Length Variance (PLV)
- Average Length Difference (ALD)
- Total Packet Time (TPT)
- Average Packet Time (APT)
- Average Time Difference (ATD)
- Packet Time Variance (PTV)
- Rate (bytes/second)

---

## 📦 Requirements

```bash
pip install pandas scikit-learn numpy scapy joblib
```
