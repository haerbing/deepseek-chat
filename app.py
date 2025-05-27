from flask import Flask, request, make_response
from wechat import parse_wechat_msg, build_reply
from deepseek_api import ask_deepseek
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        return request.args.get("echostr", "")
    
    elif request.method == "POST":
        # 微信云托管路径验证专用
        content_type = request.headers.get("Content-Type", "")
        data = request.data.decode("utf-8")
        
        if "application/json" in content_type:
            if '"CheckContainerPath"' in data:
                return "success"
        elif "xml" in content_type:
            try:
                xml = ET.fromstring(data)
                action = xml.find("action").text
                if action == "CheckContainerPath":
                    return "success"
            except:
                pass

        # 正常消息处理
        msg = parse_wechat_msg(request.data)
        user_msg = msg["content"]
        try:
            ai_reply = ask_deepseek(user_msg)
        except Exception:
            ai_reply = "AI 处理失败，请稍后再试。"
        return make_response(build_reply(msg["from_user"], msg["to_user"], ai_reply))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
