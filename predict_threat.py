import pandas as pd
import numpy as np
from preprocessing import DataPreprocessor
from train_model import CyberThreatDetector
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='predictions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ThreatPredictor:
    def __init__(self):
        try:
            self.preprocessor = DataPreprocessor.load_preprocessor()
            self.model = CyberThreatDetector.load_model()
            logging.info("Loaded preprocessor and model successfully")
        except Exception as e:
            logging.error(f"Error loading model or preprocessor: {str(e)}")
            raise
    
    def predict(self, data):
        """
        Make predictions on input data.
        data: can be a dictionary or pandas DataFrame
        """
        try:
            # Convert dictionary to DataFrame if necessary
            if isinstance(data, dict):
                data = pd.DataFrame([data])
            
            # Preprocess the data
            processed_data = self.preprocessor.preprocess_data(data)
            
            # Make prediction
            prediction = self.model.predict(processed_data)[0]
            prediction_proba = self.model.predict_proba(processed_data)[0]
            
            # Get confidence score
            confidence = prediction_proba[1] if prediction == 1 else prediction_proba[0]
            
            # Log prediction
            logging.info(f"Prediction made: {prediction} with confidence: {confidence:.4f}")
            
            return {
                'prediction': int(prediction),
                'status': 'threat' if prediction == 1 else 'safe',
                'confidence': float(confidence),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error in prediction: {str(e)}")
            raise
    
    def validate_input(self, data):
        """Validate input data format"""
        required_fields = {
            'user_id': str,
            'session_duration': (int, float),
            'transaction_amount': (int, float),
            'ip_address': str,
            'device_type': str,
            'location': str,
            'number_of_failed_logins': (int, float)
        }
        
        missing_fields = []
        invalid_types = []
        
        for field, expected_type in required_fields.items():
            if field not in data:
                missing_fields.append(field)
            elif not isinstance(data[field], expected_type):
                invalid_types.append(field)
        
        if missing_fields or invalid_types:
            error_msg = []
            if missing_fields:
                error_msg.append(f"Missing fields: {', '.join(missing_fields)}")
            if invalid_types:
                error_msg.append(f"Invalid type for fields: {', '.join(invalid_types)}")
            raise ValueError(' '.join(error_msg))
        
        return True

if __name__ == "__main__":
    # Example usage
    example_data = {
        'user_id': 'user123',
        'session_duration': 300,
        'transaction_amount': 150.0,
        'ip_address': '192.168.1.1',
        'device_type': 'mobile',
        'location': 'US',
        'number_of_failed_logins': 0
    }
    
    predictor = ThreatPredictor()
    result = predictor.predict(example_data)
    print("Prediction result:", result)
