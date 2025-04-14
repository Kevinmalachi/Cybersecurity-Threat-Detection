class SimpleThreatPredictor:
    def predict(self, data):
        """
        A simple threat detection system that checks:
        1. IP address status
        2. Transaction amount
        3. Distance from usual location
        """
        try:
            # Check IP status first - quickest way to detect threats
            if data['ip_status'].lower() == 'suspicious':
                return {
                    'prediction': 1,
                    'status': 'suspicious',
                    'confidence': 0.95,
                    'message': '⚠️ Warning: Suspicious IP detected!'
                }
            
            # Get transaction details
            amount = float(data['transaction_amount'])
            distance = float(data['distance_km'])
            
            # Calculate risk score (0 to 1)
            risk_score = 0
            
            # Check transaction amount
            if amount > 1000:  # Medium risk
                risk_score += 0.4
            if amount > 5000:  # High risk
                risk_score += 0.3
                
            # Check location distance
            if distance > 100:  # Medium risk
                risk_score += 0.2
            if distance > 500:  # High risk
                risk_score += 0.3
                
            # Make final decision
            if risk_score > 0.5:
                return {
                    'prediction': 1,
                    'status': 'suspicious',
                    'confidence': risk_score,
                    'message': f'⚠️ Warning: Unusual transaction pattern detected!'
                }
            else:
                return {
                    'prediction': 0,
                    'status': 'safe',
                    'confidence': 1 - risk_score,
                    'message': '✅ Transaction looks normal'
                }
                
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            raise
            
    def validate_input(self, data):
        """
        Make sure all required data is present and valid
        """
        required = {
            'transaction_amount': (int, float),
            'distance_km': (int, float),
            'ip_status': str
        }
        
        for field, types in required.items():
            # Check if field exists
            if field not in data:
                raise ValueError(f"Missing {field}")
            
            # Check numeric fields
            if field != 'ip_status':
                try:
                    float(data[field])
                except:
                    raise ValueError(f"{field} must be a number")
            
        # Check IP status value
        if data['ip_status'] not in ['Trusted', 'Suspicious']:
            raise ValueError("IP status must be 'Trusted' or 'Suspicious'")
