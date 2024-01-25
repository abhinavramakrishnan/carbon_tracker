import openai

openai.api_key = "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"

def chatbot(message):
    prompt = f"Hello, I'm Terra, your personal sustainability assistant. How can I help you save energy and reduce your carbon footprint today?\n\nHuman: {message}\nTerra:"

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["Human:", "Terra:"]
    )

    response_text = response.choices[0].text.strip()
    return response_text

