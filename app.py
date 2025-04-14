from flask import Flask, request, render_template, jsonify
from simple_predict import SimpleThreatPredictor
import os

app = Flask(__name__)

# Create our predictor
predictor = SimpleThreatPredictor()

# Make sure we have a templates folder
os.makedirs('templates', exist_ok=True)

# Create our simple web page
with open('templates/index.html', 'w') as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Transaction Risk Checker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background-color: #f5f5f5; 
            padding: 20px; 
        }
        .container { 
            max-width: 600px; 
            margin: 0 auto; 
        }
        .card {
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .result-safe {
            color: #198754;
            font-size: 1.2em;
        }
        .result-suspicious {
            color: #dc3545;
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="card-header">
                <h2 class="text-center">Transaction Risk Checker</h2>
            </div>
            <div class="card-body">
                <form id="checkForm">
                    <div class="mb-3">
                        <label class="form-label">Transaction Amount ($)</label>
                        <input type="number" class="form-control" name="transaction_amount" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Distance from Normal Location (km)</label>
                        <input type="number" class="form-control" name="distance_km" required>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">IP Address Status</label>
                        <select class="form-control" name="ip_status" required>
                            <option value="Trusted">Trusted</option>
                            <option value="Suspicious">Suspicious</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="btn btn-primary w-100">Check Transaction</button>
                </form>
            </div>
        </div>

        <div class="card" id="resultCard" style="display: none;">
            <div class="card-body text-center">
                <h3 id="resultMessage"></h3>
                <div class="progress mt-3">
                    <div class="progress-bar" id="confidenceBar" role="progressbar"></div>
                </div>
                <p class="mt-2">Confidence: <span id="confidenceValue"></span>%</p>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('checkForm').onsubmit = async (e) => {
            e.preventDefault();
            const form = e.target;
            const data = Object.fromEntries(new FormData(form));
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.error) {
                    alert(result.error);
                    return;
                }
                
                // Show result
                const resultCard = document.getElementById('resultCard');
                const resultMessage = document.getElementById('resultMessage');
                const confidenceBar = document.getElementById('confidenceBar');
                const confidenceValue = document.getElementById('confidenceValue');
                
                resultCard.style.display = 'block';
                resultMessage.textContent = result.message;
                resultMessage.className = result.status === 'safe' ? 'result-safe' : 'result-suspicious';
                
                const confidence = Math.round(result.confidence * 100);
                confidenceBar.style.width = confidence + '%';
                confidenceBar.className = 'progress-bar ' + 
                    (result.status === 'safe' ? 'bg-success' : 'bg-danger');
                confidenceValue.textContent = confidence;
                
                resultCard.scrollIntoView({ behavior: 'smooth' });
                
            } catch (error) {
                alert('Error checking transaction. Please try again.');
                console.error(error);
            }
        };
    </script>
</body>
</html>
    """)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def check_transaction():
    try:
        # Get the data from the form
        data = request.get_json()
        
        # Make sure the data is valid
        predictor.validate_input(data)
        
        # Check if the transaction is suspicious
        result = predictor.predict(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8080)
