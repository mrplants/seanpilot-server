from pathlib import Path
import os

from flask import Flask, request
from openai import OpenAI
import yaml

# Retreive the env, default to dev
ENV = 'dev'
if os.environ.get('ENV'):
    ENV = os.environ.get('ENV')

# Load the config values
secrets = yaml.safe_load(open(Path(__file__).parent.parent / 'config' / ENV / 'secrets.yaml',
                              encoding='utf-8'))
values = yaml.safe_load(open(Path(__file__).parent.parent / 'config' / ENV / 'values.yaml',
                             encoding='utf-8'))

openai_client = OpenAI(api_key=secrets['OPENAI_API_KEY'])

app = Flask(__name__)

@app.post('/completion')
def completion():
    """Given a code context, returns the next line of code.
    """
    data = request.json
    code_context = data['code_context']

    response = openai_client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system",
             "content": ("You are an inline code completion tool.  Respond with the next line of "
                         "code given the current code context.")},
            {"role": "user",
                "content": f"code context: {code_context}"}
        ]
    )
    completion_text = response.choices[0].message.content
    return {'completion': completion_text}

if __name__ == '__main__':
    app.run(debug=True)
