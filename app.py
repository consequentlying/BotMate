import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]
message_list = [{"role": "system", "content": "You are a helpful assistant."}]
chat_history = []


@app.route("/")
def index():
    return render_template("chat.html.jinja2", chat_history=chat_history)


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form["message"]

    message_list.append({"role": "user", "content": message})

    # 使用 OpenAI API 生成回复
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_list,
    )

    # 从 OpenAI API 的响应中提取回复内容
    reply = completion.choices[0]['message']['content']

    message_list.append({"role": "assistant", "content": reply})

    # 将回复添加到聊天历史中
    chat_history.append((message, reply))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
