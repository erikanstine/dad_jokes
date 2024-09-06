from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI


load_dotenv()

app = Flask(__name__)
client = OpenAI()


def send_oai_query(subject, qty):
    user_query = (
        f"Please write the {qty} best dad jokes you can come up with about {subject}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": [{"type": "text", "text": user_query}]}],
        temperature=0.8,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "text"},
    )
    print(response)
    return response.choices[0].message


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/jokes", methods=["POST"])
def jokes_post():
    try:
        data = request.json
        resp = send_oai_query(data["subject"], data["quantity"])
        app.logger.debug("Data processed successfully")
        return jsonify({"message": resp})
    except Exception as e:
        print(e)
        return jsonify({"error": "Invalid request data"}), 400


@app.route("/hello_world")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run(debug=True)
