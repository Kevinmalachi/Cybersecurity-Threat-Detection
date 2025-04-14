<<<<<<< HEAD
# Cyber Threat Detection System

This is a machine learning-based system developed for my final year project to detect cyber threats in an eCommerce context. It uses supervised learning techniques to classify user behavior as either safe or suspicious.

## Project Structure
```
2025_Final_Project/
├── preprocessing.py      # Data preprocessing and feature engineering
├── train_model.py       # Model training and evaluation
├── predict_threat.py    # Threat detection inference logic
├── app.py              # Web interface for demo
└── models/
    └── cyber_threat_model.pkl  # Trained model
```

## Setup and Installation
1. Clone or download the project folder
2. Install the required Python libraries:
```bash
pip install -r requirements.txt
```

## Usage
1. Data Preprocessing:
```bash
python preprocessing.py
```

2. Train Model:
```bash
python train_model.py
```

3. Run Web Interface:
```bash
python app.py
```

## Model Details
-Algorithm used: Random Forest (can be adjusted)
-Input features include transaction amount, distance in KM, and IP status
-Output: "Safe" or "Suspicious" prediction

## Web Interface
The web interface allows users to:
-Users can manually input transaction data
-Simplified UI: only asks for 3 fields (amount, distance, IP trust level)
-Displays instant prediction with clear result text
-Includes basic input validation and error handling

## Error Handling
-Checks for missing or invalid input
-Handles wrong data types gracefully
=======
# Cybersecurity-Threat-Detection
22043973- Final Year Project- Cybersecurity Threat Detection Using Machine Learning for ECommerce 
>>>>>>> 76a6fffd5b3501c72393b4e719337c2409e88c6b
