from flask import Flask,request
import json
import requests
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)

@app.route("/api/transfer", methods=["POST"])
def api_transfer():
    app.logger.info("Info message")
    app.logger.warning("Warning msg")
    app.logger.error("Error msg!!!")
    # 默认返回内容
    return_dict = {"code": '1', "message": '', "data": False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    url = get_Data.get('url')
    http_method = get_Data.get('http_method')
    http_data = get_Data.get('http_data')
    app.logger.warning(url)
    app.logger.warning(http_method)
    app.logger.warning(http_data)

    if http_method == 'POST':
        r_http_result = requests.post(url=url, json=http_data)
    else:
        r_http_result = requests.get(url=url)
    # 对参数进行操作
    return_dict['data'] = r_http_result.text

    return (json.dumps(return_dict, ensure_ascii=False))

if __name__ == '__main__':
    app.debug = True
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    handler.setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    app.run(host='0.0.0.0')
