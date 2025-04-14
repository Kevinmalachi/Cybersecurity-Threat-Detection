import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='preprocessing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def preprocess_data(self, df):
        """
        Preprocess the input data for cyber threat detection.
        """
        try:
            # Create a copy of the dataframe
            processed_df = df.copy()
            
            # Handle missing values
            processed_df['session_duration'] = processed_df['session_duration'].fillna(processed_df['session_duration'].median())
            processed_df['transaction_amount'] = processed_df['transaction_amount'].fillna(0)
            processed_df['number_of_failed_logins'] = processed_df['number_of_failed_logins'].fillna(0)
            
            # Encode categorical variables
            categorical_columns = ['device_type', 'location']
            for col in categorical_columns:
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                processed_df[col] = self.label_encoders[col].fit_transform(processed_df[col].fillna('unknown'))
            
            # Extract features from IP address (simplified)
            processed_df['ip_risk_score'] = processed_df['ip_address'].apply(
                lambda x: np.random.uniform(0, 1)  # In real scenario, would check against IP reputation database
            )
            
            # Scale numerical features
            numerical_columns = ['session_duration', 'transaction_amount', 
                               'number_of_failed_logins', 'ip_risk_score']
            processed_df[numerical_columns] = self.scaler.fit_transform(processed_df[numerical_columns])
            
            # Drop original IP address column
            processed_df = processed_df.drop('ip_address', axis=1)
            
            logging.info(f"Successfully preprocessed {len(df)} records")
            return processed_df
            
        except Exception as e:
            logging.error(f"Error in preprocessing: {str(e)}")
            raise
    
    def save_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Save the preprocessor object"""
        joblib.dump(self, filepath)
    
    @staticmethod
    def load_preprocessor(filepath='models/preprocessor.pkl'):
        """Load the preprocessor object"""
        return joblib.load(filepath)

def prepare_training_data(data_path):
    """
    Prepare data for training the model.
    """
    try:
        # Load data
        df = pd.read_csv(data_path)
        
        # Drop rows with NaN in the target variable
        df = df.dropna(subset=['label'])
        
        # Initialize preprocessor
        preprocessor = DataPreprocessor()
        
        # Remove user_id from features
        features_df = df.drop(['label', 'user_id'], axis=1)
        
        # Preprocess features
        X = preprocessor.preprocess_data(features_df)
        y = df['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Save preprocessor
        preprocessor.save_preprocessor()
        
        return X_train, X_test, y_train, y_test, preprocessor
        
    except Exception as e:
        logging.error(f"Error in prepare_training_data: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    print("This module is for preprocessing cyber threat detection data.")
    print("Example features required:", [
        "session_duration", "transaction_amount",
        "ip_address", "device_type", "location", "number_of_failed_logins"
    ])
