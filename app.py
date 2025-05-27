from flask import Flask, request, make_response
from wechat import parse_wechat_msg, build_reply
from deepseek_api import ask_deepseek

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        return request.args.get("echostr")
    elif request.method == "POST":
        xml_data = request.data
        msg = parse_wechat_msg(xml_data)
        user_msg = msg["content"]
        try:
            ai_reply = ask_deepseek(user_msg)
        except Exception as e:
            ai_reply = "AI 处理失败，请稍后再试。"
        return make_response(build_reply(msg["from_user"], msg["to_user"], ai_reply))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
