from flask import Flask, render_template_string, request, jsonify
import json
import random
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Simple HTML template embedded in the Python file
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Data Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .form-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { padding: 8px; width: 200px; }
        button { padding: 10px 20px; background: #007cba; color: white; border: none; cursor: pointer; }
        button:hover { background: #005a87; }
        .result { margin-top: 20px; padding: 20px; background: #f0f8ff; border: 1px solid #007cba; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Azure Data Generator</h1>
        <form id="dataForm">
            <div class="form-group">
                <label>Data Source:</label>
                <select id="system" required>
                    <option value="salesforce">Salesforce CRM</option>
                    <option value="sfmc">Salesforce Marketing Cloud</option>
                    <option value="netsuite">NetSuite ERP</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Start Date:</label>
                <input type="date" id="startDate" value="2022-01-01" required>
            </div>
            
            <div class="form-group">
                <label>End Date:</label>
                <input type="date" id="endDate" value="2025-12-31" required>
            </div>
            
            <div class="form-group">
                <label>Number of Records:</label>
                <input type="number" id="records" value="1000" min="1" max="100000" required>
            </div>
            
            <div class="form-group">
                <label>Format:</label>
                <select id="format">
                    <option value="json">JSON</option>
                    <option value="csv">CSV</option>
                </select>
            </div>
            
            <button type="submit">Generate Data</button>
        </form>
        
        <div id="result" class="result" style="display:none;">
            <h3>Data Generated Successfully!</h3>
            <p id="resultText"></p>
            <a id="downloadLink" href="#" download>Download File</a>
        </div>
    </div>

    <script>
        document.getElementById('dataForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                system: document.getElementById('system').value,
                startDate: document.getElementById('startDate').value,
                endDate: document.getElementById('endDate').value,
                records: parseInt(document.getElementById('records').value),
                format: document.getElementById('format').value
            };
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('resultText').textContent = 
                        `Generated ${result.records} records successfully!`;
                    document.getElementById('downloadLink').href = result.download_url;
                    document.getElementById('result').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    </script>
</body>
</html>
'''

def generate_sample_data(system, start_date, end_date, records):
    """Generate simple sample data"""
    data = []
    
    for i in range(records):
        if system == 'salesforce':
            record = {
                'Id': f'SF{i:06d}',
                'Name': f'Company {i+1}',
                'Industry': random.choice(['Technology', 'Healthcare', 'Finance', 'Manufacturing']),
                'AnnualRevenue': random.randint(100000, 10000000),
                'CreatedDate': start_date.isoformat()
            }
        elif system == 'sfmc':
            record = {
                'JobID': random.randint(100000, 999999),
                'EmailAddress': f'user{i+1}@example.com',
                'EventType': random.choice(['Send', 'Open', 'Click', 'Bounce']),
                'EventDate': start_date.isoformat()
            }
        elif system == 'netsuite':
            record = {
                'InternalId': i + 1,
                'TransactionNumber': f'SO{i+1:06d}',
                'Type': random.choice(['Sales Order', 'Invoice', 'Purchase Order']),
                'Amount': round(random.uniform(100, 50000), 2),
                'TranDate': start_date.date().isoformat()
            }
        
        data.append(record)
    
    return data

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        system = data['system']
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        records = int(data['records'])
        format_type = data['format']
        
        # Generate data
        generated_data = generate_sample_data(system, start_date, end_date, records)
        
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{system}_data_{timestamp}.{format_type}"
        
        # Ensure temp directory exists
        os.makedirs('temp', exist_ok=True)
        filepath = os.path.join('temp', filename)
        
        # Save file
        if format_type == 'json':
            with open(filepath, 'w') as f:
                json.dump(generated_data, f, indent=2)
        elif format_type == 'csv':
            # Simple CSV generation without pandas
            if generated_data:
                with open(filepath, 'w') as f:
                    # Write header
                    headers = list(generated_data[0].keys())
                    f.write(','.join(headers) + '\n')
                    
                    # Write data
                    for record in generated_data:
                        values = [str(record.get(h, '')) for h in headers]
                        f.write(','.join(values) + '\n')
        
        return jsonify({
            'success': True,
            'records': len(generated_data),
            'filename': filename,
            'download_url': f'/download/{filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download/<filename>')
def download(filename):
    from flask import send_file
    try:
        filepath = os.path.join('temp', filename)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    print("Starting minimal data generator...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)