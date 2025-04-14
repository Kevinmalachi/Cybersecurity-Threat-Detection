import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import joblib
import logging
from preprocessing import prepare_training_data
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CyberThreatDetector:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
    def train(self, X_train, y_train):
        """Train the model"""
        try:
            self.model.fit(X_train, y_train)
            logging.info("Model training completed successfully")
        except Exception as e:
            logging.error(f"Error in model training: {str(e)}")
            raise
            
    def evaluate(self, X_test, y_test):
        """Evaluate the model and generate metrics"""
        try:
            # Make predictions
            y_pred = self.model.predict(X_test)
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(
                y_test, y_pred, average='binary'
            )
            conf_matrix = confusion_matrix(y_test, y_pred)
            
            # Log metrics
            logging.info(f"Model Evaluation Metrics:")
            logging.info(f"Accuracy: {accuracy:.4f}")
            logging.info(f"Precision: {precision:.4f}")
            logging.info(f"Recall: {recall:.4f}")
            logging.info(f"F1-Score: {f1:.4f}")
            
            # Create and save visualization
            self._plot_confusion_matrix(conf_matrix)
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'confusion_matrix': conf_matrix
            }
            
        except Exception as e:
            logging.error(f"Error in model evaluation: {str(e)}")
            raise
    
    def _plot_confusion_matrix(self, conf_matrix):
        """Plot and save confusion matrix visualization"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('models/confusion_matrix.png')
        plt.close()
    
    def save_model(self, filepath='models/cyber_threat_model.pkl'):
        """Save the trained model"""
        joblib.dump(self.model, filepath)
        logging.info(f"Model saved to {filepath}")
    
    @staticmethod
    def load_model(filepath='models/cyber_threat_model.pkl'):
        """Load a trained model"""
        return joblib.load(filepath)

def train_and_evaluate(data_path):
    """Main function to train and evaluate the model"""
    try:
        # Prepare data
        X_train, X_test, y_train, y_test, preprocessor = prepare_training_data(data_path)
        
        # Initialize and train model
        detector = CyberThreatDetector()
        detector.train(X_train, y_train)
        
        # Evaluate model
        metrics = detector.evaluate(X_test, y_test)
        
        # Save model
        detector.save_model()
        
        return detector, metrics
        
    except Exception as e:
        logging.error(f"Error in train_and_evaluate: {str(e)}")
        raise

if __name__ == "__main__":
    import os
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Train the model using sample data
    print("Training model with sample data...")
    detector, metrics = train_and_evaluate('sample_data.csv')
    
    print("\nModel Evaluation Metrics:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"F1-Score: {metrics['f1']:.4f}")
    print("\nConfusion Matrix:")
    print(metrics['confusion_matrix'])
    
    print("\nModel and preprocessor have been saved in the 'models' directory.")
