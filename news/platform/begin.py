from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class AdBlocker(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if any(ad in url for ad in [
            "doubleclick.net", "googlesyndication.com", "adservice.google.com",
            "googletagmanager.com", "ads.yahoo.com", "taboola.com", "outbrain.com"
        ]):
            info.block(True)


class CustomWebEngineView(QWebEngineView):
    def createWindow(self, _type):
        # Block popups
        return None


class News(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.tab = QTabWidget()
        self.layout.addWidget(self.tab)

        self.interceptor = AdBlocker()

        def make_browser(url):
            view = CustomWebEngineView()

            # Create page then apply interceptor
            page = view.page()
            page.setUrlRequestInterceptor(self.interceptor)

            view.load(QUrl(url))
            return view

        self.tab.addTab(make_browser("https://coinmarketcal.com/"), "Coinmarketcal")
        self.tab.addTab(make_browser("https://www.coindesk.com/"), "Coindesk")
        self.tab.addTab(make_browser("https://cointelegraph.com/"), "Cointelegraph")
        self.tab.addTab(make_browser("https://coingape.com/"), "Coingape")
        self.tab.addTab(make_browser("https://crypto.news/"), "Crypto News")
        self.tab.addTab(make_browser("https://decrypt.co/"), "Decrypt")
        self.tab.addTab(make_browser("https://www.cryptotimes.io/"), "Cryptotimes")
        self.tab.addTab(make_browser("https://www.theblock.co/"), "The Block")
        self.tab.addTab(make_browser("https://cryptoslate.com/"), "Cryptoslate")
        self.tab.addTab(make_browser("https://coindoo.com/"), "Coindoo")
        self.tab.addTab(make_browser("https://u.today/"), "U Today")
