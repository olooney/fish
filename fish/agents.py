import openai
import os
import tenacity
import json

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@tenacity.retry(stop=tenacity.stop_after_attempt(2), wait=tenacity.wait_fixed(1))
def tabulate(text, verbose=False, temperature=1.0) -> str:
    
    messages = [
        {"role": "system", "content": "Convert free form tables to JSON. Use an array of objects, where each object's keys are the column names." },
        {"role": "user", "content": """
|   Column1 | Column2   |   Column3 |
|----------:|:----------|----------:|
|         1 | A         |       4.5 |
|         2 | B         |       5.5 |
|         3 | C         |       6.5 |
"""},
        {"role": "assistant", "content": """{
"table": [
    {"Column1":1,"Column2":"A","Column3":4.5},
    {"Column1":2,"Column2":"B","Column3":5.5},
    {"Column1":3,"Column2":"C","Column3":6.5}
]}
"""},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=messages,
        temperature=temperature
    )
    message = response.choices[0].message.content
    return json.loads(message)['table']
