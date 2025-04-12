import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QLineEdit,
                            QVBoxLayout, QWidget, QTabWidget, QFileDialog)
from PyQt6.QtWebEngineWidgets import QWebEngineView

class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.bing.com"))
        self.browser.page().profile().downloadRequested.connect(self.handle_download)
        
        # 处理页面加载完成事件
        self.browser.loadFinished.connect(self.handle_load_finished)
        
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        
        self.nav_toolbar = QToolBar("Navigation")
        self.nav_toolbar.addAction("←", self.browser.back)
        self.nav_toolbar.addAction("→", self.browser.forward)
        self.nav_toolbar.addAction("↻", self.browser.reload)
        self.nav_toolbar.addAction("⌂", self.navigate_home)
        self.nav_toolbar.addWidget(self.urlbar)
        
        layout = QVBoxLayout()
        layout.addWidget(self.nav_toolbar)
        layout.addWidget(self.browser)
        self.setLayout(layout)
        
        self.browser.urlChanged.connect(self.update_urlbar)
    
    def navigate_to_url(self):
        url = self.urlbar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))
    
    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.bing.com"))
    
    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        
    def handle_download(self, download):
        # 设置下载保存路径
        path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "所有文件 (*.*)")
        if path:
            download.setPath(path)
            download.accept()
            
    def handle_load_finished(self, ok):
        # 处理页面加载完成事件
        if not ok:
            self.browser.setHtml("<h1>页面加载失败</h1><p>请检查网络连接或URL是否正确</p>")

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 浏览器")
        self.setGeometry(100, 100, 1024, 768)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.add_new_tab()
        
        self.setCentralWidget(self.tabs)
        
        # 添加新建标签页按钮
        self.new_tab_btn = QToolBar("New Tab")
        self.new_tab_btn.addAction("+", self.add_new_tab)
        self.addToolBar(self.new_tab_btn)
    
    def add_new_tab(self):
        tab = BrowserTab()
        self.tabs.addTab(tab, "新标签页")
        self.tabs.setCurrentWidget(tab)
    
    def close_tab(self, index):
        if self.tabs.count() < 2:
            return
        
        widget = self.tabs.widget(index)
        widget.deleteLater()
        self.tabs.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
