import xml.etree.ElementTree as ET
import time

def parse_wechat_msg(xml_data):
    root = ET.fromstring(xml_data)
    return {
        "from_user": root.find('FromUserName').text,
        "to_user": root.find('ToUserName').text,
        "content": root.find('Content').text
    }

def build_reply(to_user, from_user, reply_content):
    return f"""
    <xml>
      <ToUserName><![CDATA[{to_user}]]></ToUserName>
      <FromUserName><![CDATA[{from_user}]]></FromUserName>
      <CreateTime>{int(time.time())}</CreateTime>
      <MsgType><![CDATA[text]]></MsgType>
      <Content><![CDATA[{reply_content}]]></Content>
    </xml>
    """