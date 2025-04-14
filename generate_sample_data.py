import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import ipaddress

def generate_sample_data(n_samples=1000):
    """Generate sample data for cyber threat detection"""
    
    # Lists for categorical data
    device_types = ['mobile', 'desktop', 'tablet']
    locations = ['US', 'UK', 'CA', 'DE', 'FR', 'JP', 'AU', 'BR', 'IN', 'RU']
    
    # Generate base data
    data = {
        'user_id': [f'user_{i:04d}' for i in range(n_samples)],
        'session_duration': [],
        'transaction_amount': [],
        'ip_address': [],
        'device_type': [],
        'location': [],
        'number_of_failed_logins': [],
        'label': []
    }
    
    for i in range(n_samples):
        # Determine if this will be a threat
        is_threat = random.random() < 0.2  # 20% of data will be threats
        
        # Session duration (seconds)
        if is_threat:
            duration = random.uniform(1, 30) if random.random() < 0.5 else random.uniform(3600, 7200)
        else:
            duration = random.uniform(60, 3600)
        data['session_duration'].append(duration)
        
        # Transaction amount
        if is_threat:
            amount = random.uniform(1000, 5000) if random.random() < 0.7 else random.uniform(0, 100)
        else:
            amount = random.uniform(10, 500)
        data['transaction_amount'].append(amount)
        
        # IP address
        ip = str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1)))
        data['ip_address'].append(ip)
        
        # Device type
        if is_threat:
            device = random.choice(device_types)
        else:
            device = random.choices(device_types, weights=[0.4, 0.5, 0.1])[0]
        data['device_type'].append(device)
        
        # Location
        if is_threat:
            location = random.choice(locations)
        else:
            location = random.choices(locations, weights=[0.3, 0.2, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.03, 0.02])[0]
        data['location'].append(location)
        
        # Number of failed logins
        if is_threat:
            failed_logins = random.randint(3, 10)
        else:
            failed_logins = random.randint(0, 2)
        data['number_of_failed_logins'].append(failed_logins)
        
        # Label (1 for threat, 0 for safe)
        data['label'].append(1 if is_threat else 0)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add some random missing values
    mask = np.random.random(df.shape) < 0.05
    df.mask(mask, inplace=True)
    
    return df

if __name__ == "__main__":
    # Generate sample data
    print("Generating sample data...")
    df = generate_sample_data()
    
    # Save to CSV
    output_file = 'sample_data.csv'
    df.to_csv(output_file, index=False)
    print(f"Sample data saved to {output_file}")
    
    # Display sample statistics
    print("\nData Statistics:")
    print(f"Total samples: {len(df)}")
    print(f"Threat samples: {df['label'].sum()}")
    print(f"Safe samples: {len(df) - df['label'].sum()}")
    print("\nSample of the data:")
    print(df.head())
