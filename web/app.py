from flask import Flask, render_template, send_file
from gevent.queue import Queue


class WebInterface():
    def __init__(self, web_queue):
        self._web_queue = web_queue
        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.index_site)

    def index_site(self):
        return render_template("index.html")

if __name__ == "__main__":
    intf = WebInterface(Queue())
    intf.app.run("127.0.0.1", 5000, debug=True)
