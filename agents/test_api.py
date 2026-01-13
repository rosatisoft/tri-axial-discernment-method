from openai import OpenAI

client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"user", "content":"Dime un número entre 0 y 1"}
    ]
)

print(resp.choices[0].message.content)
