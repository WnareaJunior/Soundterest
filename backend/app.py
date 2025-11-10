from flask import Flask, jsonify
from supabase import create_client, Client
from flask_cors import CORS
from dotenv import load_dotenv 
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def home():
    return 'hello world'

# Test endpoint to see all users
@app.route('/api/test')
def test():
    result = supabase_client.table('Users').select('*').execute()
    return jsonify(result.data)

@app.route('/api/user/<username>')
def profile(username):
    # Remove .single() for now to debug
    user_response = supabase_client.table('Users').select('*').eq('username', username).execute()
    
    print(f"Looking for user: {username}")
    print(f"Response: {user_response.data}")
    
    if not user_response.data:
        return jsonify({'error': 'User not found'}), 404
    
    user = user_response.data[0]

    samples_response = supabase_client.table('Samples').select('*').eq('owner_id', user['id']).execute()

    return jsonify({
        'user': user,
        'samples': samples_response.data
    })

if __name__ == '__main__':
    app.run(debug=True)