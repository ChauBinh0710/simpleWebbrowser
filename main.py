# IMPORTS thư viện 
import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# WEB ENGINE( pip install PyQtWebEngine)
from PyQt5.QtWebEngineWidgets import *

# Tạo cửa sổ chính
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Thêm các elements vào cửa sổ chính
        # Thêm Widgets để hiển thị các web tab
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # Thêm nhấp đôi cho Event Listener
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        # Thêm nút đóng tab EVENT LISTENER
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        # Thêm tab hoạt động thay đổi EVENT LISTENER
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # Thêm thanh công cụ điều hướng
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # Thêm nút vào thanh công cụ điều hướng
        # Nút trở về trang trước
        back_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-left.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        # Lệnh điều hướng về trang trước
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        # Thêm nút tiến đến trang kế sau
        next_btn = QAction(QIcon(os.path.join('icons', 'cil-arrow-circle-right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        # Lệnh điều hướng trang tiếp kế sau
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        # Nút làm mới trang
        reload_btn = QAction(QIcon(os.path.join('icons', 'cil-reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)
        # Làm mới trang
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())

        # Nút trở về trang mặc định
        home_btn = QAction(QIcon(os.path.join('icons', 'cil-home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)
        #  Điều hướng về trang mặc định
        home_btn.triggered.connect(self.navigate_home)

        # Phân tách các nút điều hướng
        navtb.addSeparator()

        # THÊM BIỂU TƯỢNG HIỂN THỊ TRẠNG THÁI BẢO MẬT CỦA URL 
        self.httpsicon = QLabel()  
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))
        navtb.addWidget(self.httpsicon)

        # Thêm dòng chỉnh sửa để hiện và chỉnh sửa các URL
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        # Chạy URL khi nhấn enter
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        # Thêm nút dừng khi đang chạy URL
        stop_btn = QAction(QIcon(os.path.join('icons', 'cil-media-stop.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)
        # Dừng chạy URL
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        # Thêm mục lục phía trên
        # Mục lục file
        file_menu = self.menuBar().addMenu("&File")
        # Hoạt động thêm tab mới trong mục lục file
        new_tab_action = QAction(QIcon(os.path.join('icons', 'cil-library-add.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        # Thêm tab mới
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        # Mục lục trợ giúp
        help_menu = self.menuBar().addMenu("&Home")
        # Thêm mục lục trợ giúp
        navigate_home_action = QAction(QIcon(os.path.join('icons', 'cil-exit-to-app.png')),
                                            "Homepage", self)
        navigate_home_action.setStatusTip("Go to Homepage")
        help_menu.addAction(navigate_home_action)
        # NAVIGATE TO DEVELOPER WEBSITE
        navigate_home_action.triggered.connect(self.navigate_home)


        # Cài đặt tiêu đề của Browser
        self.setWindowTitle("OWN Browser")
        self.setWindowIcon(QIcon(os.path.join('icons', 'cil-screen-desktop.png')))

        # Thêm bảng kiểu để cá nhân hoá cửa sổ của bạn
        # STYLESHEET (DARK MODE)
        self.setStyleSheet("""QWidget{
           background-color: rgb(48, 48, 48);
           color: rgb(255, 255, 255);
        }
        QTabWidget::pane { /* The tab widget frame */
            border-top: 2px solid rgb(90, 90, 90);
            position: absolute;
            top: -0.5em;
            color: rgb(255, 255, 255);
            padding: 5px;
        }

        QTabWidget::tab-bar {
            alignment: left;
        }

        /* Style the tab using the tab sub-control. Note that
            it reads QTabBar _not_ QTabWidget */
        QLabel, QToolButton, QTabBar::tab {
            background: rgb(90, 90, 90);
            border: 2px solid rgb(90, 90, 90);
            /*border-bottom-color: #C2C7CB; /* same as the pane color */
            border-radius: 10px;
            min-width: 8ex;
            padding: 5px;
            margin-right: 2px;
            color: rgb(255, 255, 255);
        }

        QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
        }

        QLineEdit {
            border: 2px solid rgb(0, 36, 36);
            border-radius: 10px;
            padding: 5px;
            background-color: rgb(0, 36, 36);
            color: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 2px solid rgb(0, 66, 124);
        }
        QLineEdit:focus{
            border: 2px solid rgb(0, 136, 255);
            color: rgb(200, 200, 200);
        }
        QPushButton{
            background: rgb(49, 49, 49);
            border: 2px solid rgb(0, 36, 36);
            background-color: rgb(0, 36, 36);
            padding: 5px;
            border-radius: 10px;
        }""")


        # Chạy trang mặc định(GOOLE.COM)
        #url = http://www.google.com,
        #label = Homepage
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        # hiện trang mặc định
        self.show()

    # ############################################
    # Các Hàm
    ##############################################
    # Thêm tab mới
    def add_new_tab(self, qurl=None, label="Blank"):
        # Check if url value is blank
        if qurl is None:
            qurl = QUrl('')#pass empty string to url

        # Load the passed url
        browser = QWebEngineView()
        browser.setUrl(qurl)

        # Thêm tab
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Thêm trình lắng nghe sự kiện của trình duyệt web
        # Thay đổi trên URL
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))
        # Hiển thị khi tải xong
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    # Thêm tab mới khi nhấp đôi vào tabs
    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    # Đóng tab
    def close_current_tab(self, i):
        if self.tabs.count() < 2: #Only close if there is more than one tab open
            return

        self.tabs.removeTab(i)

    # Cập nhật văn bản URL khi thay đổi hoạt động của tab
    def update_urlbar(self, q, browser=None):
        #q = QURL
        if browser != self.tabs.currentWidget():
            # If this signal is not from the current tab, ignore
            return
        # Lược đồ URL
        if q.scheme() == 'https':
            # If schema is https change icon to locked padlock to show that the webpage is secure
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-locked.png')))

        else:
            # Nếu lược đồ không phải là https, hãy thay đổi biểu tượng thành ổ khóa bị khóa để cho biết rằng trang web không an toàn
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'cil-lock-unlocked.png')))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        
    # Kích hoạt thay đổi tab
    def current_tab_changed(self, i):
        # i = tab index
        # GET CURRENT TAB URL
        qurl = self.tabs.currentWidget().url()
        # Cập nhật dòng tìm kiếm URL
        self.update_urlbar(qurl, self.tabs.currentWidget())
        # Cập nhật tiêu đề cửa sổ 
        self.update_title(self.tabs.currentWidget())

    # Cập nhật tiêu đề của trang chủ
    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            # Nếu tín hiệu này không phải từ tab HOẠT ĐỘNG hiện tại, hãy bỏ qua
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)

    # Điều hướng đến URL trước
    def navigate_to_url(self):  # Không nhận URL
        # Lấy văn bản URL
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            # Chuyển HTTP làm lược đồ mặc định
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    # Điều hướng đến trang mặc định
    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

app = QApplication(sys.argv)
# Tên của Browser
app.setApplicationName("QB DnG Browser")
# APPLICATION COMPANY NAME
app.setOrganizationName("QB DnG Company")

app.setOrganizationDomain("Google.com")

window = MainWindow()
app.exec_()
