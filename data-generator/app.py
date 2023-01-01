from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
import json
import csv
import pandas as pd
import random
import uuid
from faker import Faker
import io
import zipfile
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
fake = Faker()

class DataGenerator:
    def __init__(self):
        self.fake = Faker()
        
    def generate_salesforce_data(self, start_date, end_date, min_records, max_records):
        """Generate realistic Salesforce CRM data"""
        num_records = random.randint(min_records, max_records)
        data = []
        
        for _ in range(num_records):
            created_date = self.fake.date_time_between(start_date=start_date, end_date=end_date)
            record = {
                'Id': str(uuid.uuid4()),
                'Name': self.fake.company(),
                'Type': random.choice(['Customer', 'Prospect', 'Partner', 'Competitor']),
                'Industry': random.choice(['Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail']),
                'AnnualRevenue': random.randint(100000, 50000000),
                'NumberOfEmployees': random.randint(10, 10000),
                'BillingStreet': self.fake.street_address(),
                'BillingCity': self.fake.city(),
                'BillingState': self.fake.state(),
                'BillingPostalCode': self.fake.zipcode(),
                'BillingCountry': self.fake.country(),
                'Phone': self.fake.phone_number(),
                'Website': self.fake.url(),
                'CreatedDate': created_date.isoformat(),
                'LastModifiedDate': self.fake.date_time_between(start_date=created_date, end_date=end_date).isoformat(),
                'OwnerId': str(uuid.uuid4()),
                'IsDeleted': random.choice([True, False]) if random.random() < 0.05 else False
            }
            data.append(record)
            
        return data
    
    def generate_salesforce_opportunities(self, start_date, end_date, min_records, max_records):
        """Generate Salesforce Opportunity data"""
        num_records = random.randint(min_records, max_records)
        data = []
        
        stages = ['Prospecting', 'Qualification', 'Needs Analysis', 'Value Proposition', 
                 'Id. Decision Makers', 'Perception Analysis', 'Proposal/Price Quote', 
                 'Negotiation/Review', 'Closed Won', 'Closed Lost']
        
        for _ in range(num_records):
            created_date = self.fake.date_time_between(start_date=start_date, end_date=end_date)
            close_date = self.fake.date_time_between(start_date=created_date, end_date=end_date + timedelta(days=365))
            
            record = {
                'Id': str(uuid.uuid4()),
                'Name': f"{self.fake.company()} - {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} {random.randint(2022, 2025)}",
                'AccountId': str(uuid.uuid4()),
                'StageName': random.choice(stages),
                'Amount': random.randint(5000, 1000000),
                'Probability': random.randint(10, 90),
                'CloseDate': close_date.date().isoformat(),
                'Type': random.choice(['New Customer', 'Existing Customer - Upgrade', 'Existing Customer - Replacement', 'Existing Customer - Downgrade']),
                'LeadSource': random.choice(['Web', 'Phone Inquiry', 'Partner Referral', 'Purchased List', 'Other']),
                'CreatedDate': created_date.isoformat(),
                'LastModifiedDate': self.fake.date_time_between(start_date=created_date, end_date=end_date).isoformat(),
                'OwnerId': str(uuid.uuid4()),
                'IsWon': random.choice([True, False]) if random.random() < 0.3 else False,
                'IsClosed': random.choice([True, False]) if random.random() < 0.4 else False
            }
            data.append(record)
            
        return data
    
    def generate_sfmc_data(self, start_date, end_date, min_records, max_records):
        """Generate Salesforce Marketing Cloud data"""
        num_records = random.randint(min_records, max_records)
        data = []
        
        for _ in range(num_records):
            sent_date = self.fake.date_time_between(start_date=start_date, end_date=end_date)
            record = {
                'JobID': random.randint(100000, 999999),
                'ListID': random.randint(1000, 9999),
                'BatchID': random.randint(10000, 99999),
                'SubscriberID': random.randint(1000000, 9999999),
                'SubscriberKey': str(uuid.uuid4()),
                'EmailAddress': self.fake.email(),
                'EventDate': sent_date.isoformat(),
                'EventType': random.choice(['Send', 'Open', 'Click', 'Bounce', 'Unsubscribe']),
                'SendID': random.randint(100000, 999999),
                'Subject': self.fake.sentence(nb_words=6),
                'FromName': self.fake.name(),
                'FromEmail': self.fake.email(),
                'TriggererSendDefinitionObjectID': str(uuid.uuid4()),
                'IsUnique': random.choice([True, False]),
                'URL': self.fake.url() if random.random() < 0.3 else None,
                'LinkName': self.fake.word() if random.random() < 0.3 else None,
                'LinkContent': self.fake.text(max_nb_chars=100) if random.random() < 0.3 else None
            }
            data.append(record)
            
        return data
    
    def generate_netsuite_data(self, start_date, end_date, min_records, max_records):
        """Generate NetSuite ERP data"""
        num_records = random.randint(min_records, max_records)
        data = []
        
        for _ in range(num_records):
            transaction_date = self.fake.date_time_between(start_date=start_date, end_date=end_date)
            record = {
                'InternalId': random.randint(1000, 999999),
                'TransactionNumber': f"SO{random.randint(100000, 999999)}",
                'Type': random.choice(['Sales Order', 'Invoice', 'Cash Sale', 'Credit Memo', 'Purchase Order']),
                'Status': random.choice(['Pending Approval', 'Pending Fulfillment', 'Partially Fulfilled', 'Pending Billing', 'Billed', 'Closed']),
                'Entity': self.fake.company(),
                'EntityId': random.randint(1000, 99999),
                'TranDate': transaction_date.date().isoformat(),
                'DueDate': (transaction_date + timedelta(days=random.randint(15, 90))).date().isoformat(),
                'Amount': round(random.uniform(100, 50000), 2),
                'Currency': random.choice(['USD', 'EUR', 'GBP', 'CAD']),
                'ExchangeRate': round(random.uniform(0.8, 1.2), 4),
                'Subsidiary': random.choice(['US Operations', 'EU Operations', 'APAC Operations']),
                'Department': random.choice(['Sales', 'Marketing', 'Operations', 'Finance']),
                'Location': random.choice(['New York', 'London', 'Singapore', 'Toronto']),
                'CreatedDate': transaction_date.isoformat(),
                'LastModifiedDate': self.fake.date_time_between(start_date=transaction_date, end_date=end_date).isoformat(),
                'CreatedBy': self.fake.name(),
                'Memo': self.fake.text(max_nb_chars=200) if random.random() < 0.5 else None
            }
            data.append(record)
            
        return data

generator = DataGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_data():
    try:
        data = request.json
        system = data['system']
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        min_records = int(data['minRecords'])
        max_records = int(data['maxRecords'])
        format_type = data['format']
        
        # Generate data based on system
        if system == 'salesforce':
            generated_data = generator.generate_salesforce_data(start_date, end_date, min_records, max_records)
        elif system == 'salesforce_opportunities':
            generated_data = generator.generate_salesforce_opportunities(start_date, end_date, min_records, max_records)
        elif system == 'sfmc':
            generated_data = generator.generate_sfmc_data(start_date, end_date, min_records, max_records)
        elif system == 'netsuite':
            generated_data = generator.generate_netsuite_data(start_date, end_date, min_records, max_records)
        else:
            return jsonify({'error': 'Invalid system selected'}), 400
        
        # Create file based on format
        if format_type == 'json':
            filename = f"{system}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join('temp', filename)
            os.makedirs('temp', exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(generated_data, f, indent=2)
                
        elif format_type == 'csv':
            filename = f"{system}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join('temp', filename)
            os.makedirs('temp', exist_ok=True)
            
            df = pd.DataFrame(generated_data)
            df.to_csv(filepath, index=False)
            
        elif format_type == 'parquet':
            filename = f"{system}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.parquet"
            filepath = os.path.join('temp', filename)
            os.makedirs('temp', exist_ok=True)
            
            df = pd.DataFrame(generated_data)
            df.to_parquet(filepath, index=False)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'records_generated': len(generated_data),
            'download_url': f'/download/{filename}'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join('temp', secure_filename(filename))
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)