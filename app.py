from flask import Flask, render_template, request
import requests
import logging
import json
import pandas as pd

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_request', methods=['POST'])
def send_request():
    url = request.form.get('url')
    authorization = request.form.get('authorization')
    header_keys = request.form.getlist('header_key[]')
    header_values = request.form.getlist('header_value[]')
    headers = {}

    for key, value in zip(header_keys, header_values):
        key = key.strip()  # Remove leading/trailing whitespace
        value = value.strip()  # Remove leading/trailing whitespace
        if key and value:  # Skip empty header names/values
            headers[key] = value

    cookies = request.form.get('cookies')

    # Log the request details
    logging.info('Sending HTTP request:')
    logging.info(f'URL: {url}')
    logging.info(f'Headers: {headers}')
    logging.info(f'Authorization: {authorization}')
    logging.info(f'Cookies: {cookies}')

    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        try:
            # Parse the JSON response
            data = response.json()
            
            # Convert the JSON data into a pandas DataFrame
            df = pd.DataFrame(data)
            
            # Convert the DataFrame to an HTML table
            table = df.to_html(index=False)

            return render_template('response.html', response=table)
        except json.JSONDecodeError:
            logging.warning('Unable to parse response as JSON')
    
    return render_template('response.html', response=response.text)


if __name__ == '__main__':
    app.run()
