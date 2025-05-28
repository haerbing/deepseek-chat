from flask import Flask, request, make_response
import hashlib
import requests

from wechat import parse_wechat_msg, build_reply
from deepseek_api import ask_deepseek

app = Flask(__name__)

TOKEN = "weixincloud2024"


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

        return echostr if check_signature == signature else ""

    elif request.method == "POST":
        try:
            xml_data = request.data
            msg = parse_wechat_msg(xml_data)
            user_msg = msg["content"]

            # 获取用户 OpenID（微信云托管会自动加到 Header 中）
            openid = request.headers.get("x-wx-openid", "")

            # 调用微信内容安全接口（云托管模式下不需要 access_token）
            api_url = "https://api.weixin.qq.com/wxa/msg_sec_check"
            payload = {
                "openid": openid,
                "version": 2,
                "scene": 2,
                "content": user_msg
            }
            wechat_response = requests.post(api_url, json=payload)
            check_result = wechat_response.json()

            if check_result.get("errcode") == 0:
                reply_content = ask_deepseek(user_msg)
            else:
                reply_content = "消息未通过安全校验"

            reply_xml = build_reply(
                to_user=msg["from_user"],
                from_user=msg["to_user"],
                content=reply_content
            )
            return make_response(reply_xml)
        except Exception as e:
            print("处理失败:", e)
            return "success"  # 微信要求返回 "success"，避免重复推送

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)