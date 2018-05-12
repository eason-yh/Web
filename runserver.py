#!flask/bin/python
#_*_ coding:utf-8 _*_
from app import app


if __name__ == '__main__':
    # debug模式不支持多人操作
    app.run(host='0.0.0.0', port=5000, debug=True)
    # 多线程操作
    # app.run(host='0.0.0.0', port=5000, threaded=True)