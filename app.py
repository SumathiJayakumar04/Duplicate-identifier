
import webview
from backend import Api

if __name__ == '__main__':
    api = Api()
    window = webview.create_window("JP-001 | Duplicate Finder", "web/index.html", js_api=api, width=1000, height=700)
    webview.start()
