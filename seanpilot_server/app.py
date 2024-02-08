from flask import Flask, request
import openai

openai_client = OpenAI(api_key='')

app = Flask(__name__)

@app.post('/completion')
def completion():
    data = request.json
    code_context = data['code_context']
    
    try:
        openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
        )        response = openai.Completion.create(
          engine="code-davinci-002", # Or another suitable engine
          prompt=code_context,
          temperature=0.7,
          max_tokens=150,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0,
          stop=["#", "\n"]
        )
        completion_text = response.choices[0].text.strip()
        return {'completion': completion_text}
    except Exception as e:
        return {'error': str(e)}, 500
