from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()

app = Flask(__name__)
client = OpenAI()

# OPENAI_MODEL_NAME = "gpt-3.5-turbo"
# OPENAI_MODEL_NAME = "gpt-4o-mini"
OPENAI_MODEL_NAME = "gpt-4o-2024-08-06"


class JokesResponse(BaseModel):
    jokes: list[str]


def send_oai_query(subject, qty):
    if qty > 5:
        qty = 5
    elif qty < 1:
        qty = 1
    user_query = (
        f"Please write the {qty} best dad jokes you can come up with about {subject}"
    )
    # response = client.chat.completions.create(
    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL_NAME,
        messages=[{"role": "user", "content": [{"type": "text", "text": user_query}]}],
        temperature=0.8,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format=JokesResponse,
    )
    print(response.choices[0].message.parsed)
    # return response
    # return response.choices[0].message.to_dict()
    return response.choices[0].message.parsed.model_dump()


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/jokes", methods=["POST"])
def jokes_post():
    try:
        data = request.json
        resp = send_oai_query(data["subject"], int(data["quantity"]))
        # resp = ["Joke"] * int(data["quantity"])
        app.logger.debug("Data processed successfully")
        # return jsonify({"jokes": resp})
        return resp
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid request data"}), 400


@app.route("/hello_world")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run(port=8000, debug=True)
