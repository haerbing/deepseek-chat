from flask import Flask, request, make_response
import hashlib
import time

from wechat import parse_wechat_msg, build_reply
from deepseek_api import ask_deepseek

app = Flask(__name__)

# 和公众号设置里的 Token 保持一致
TOKEN = "chenleibin2006"  # 你自己设置的 token

@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        # 微信服务器验证 GET 请求
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")

        check_str = "".join(sorted([TOKEN, timestamp, nonce]))
        check_signature = hashlib.sha1(check_str.encode("utf-8")).hexdigest()

        if check_signature == signature:
            return echostr
        else:
            return ""

    elif request.method == "POST":
        try:
            xml_data = request.data
            msg = parse_wechat_msg(xml_data)
            user_msg = msg["content"]

            # 调用 AI 接口
            ai_reply = ask_deepseek(user_msg)

            reply_xml = build_reply(
                to_user=msg["from_user"],
                from_user=msg["to_user"],
                content=ai_reply
            )
            return make_response(reply_xml)
        except Exception as e:
            print("处理失败:", e)
            return "success"  # 微信要求回复 success 避免重发

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
