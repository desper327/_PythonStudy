import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextBrowser, QLabel, QDialog, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPixmap, QTextCursor, QTextCharFormat, QImage
from PyQt5.QtCore import Qt, QUrl, QSize, pyqtSignal

# --- 1. CustomTextEdit (NOW INHERITS FROM QTextBrowser) ---
class CustomTextEdit(QTextBrowser): # <--- CHANGED FROM QTextEdit to QTextBrowser
    imageClicked = pyqtSignal(str) # Define a signal to emit the image path when clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        # QTextBrowser is read-only by default, no need for self.setReadOnly(True)
        self.setOpenLinks(False) # <--- This method now exists because it's a QTextBrowser
                                 # Crucial: Prevent default external browser opening behavior

    def mousePressEvent(self, event):
        """Override the mouse click event to detect image clicks."""
        cursor = self.cursorForPosition(event.pos()) # Get text cursor at click position
        char_format = cursor.charFormat() # Get character format at cursor

        if char_format.isImageFormat(): # Check if it's an image format
            image_name = char_format.toImageFormat().name() # Get the image source (path/URL)
            self.imageClicked.emit(image_name) # Emit the signal with the image path

        super().mousePressEvent(event) # Call parent's method to maintain default behavior
                                     # This also ensures anchorClicked signal is emitted by QTextBrowser


# --- 2. ImageViewerDialog (remains unchanged) ---
class ImageViewerDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("图片查看器 - " + image_path.split('/')[-1])
        self.setGeometry(200, 200, 600, 450)

        layout = QVBoxLayout(self)
        self.image_label = QLabel("加载中...", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)

        self.loadImage(image_path)

    def loadImage(self, image_path):
        if not image_path:
            self.image_label.setText("未提供图片路径。")
            return

        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.image_label.setText(f"无法加载图片: {image_path}\n请确保路径正确。")
            else:
                self.image_label.setPixmap(pixmap)
                # Adjust window size to fit image, but cap it
                self.resize(min(pixmap.width() + 50, QApplication.desktop().width() * 0.8),
                            min(pixmap.height() + 50, QApplication.desktop().height() * 0.8))
                self.image_label.adjustSize()
                self.adjustSize()

        except Exception as e:
            self.image_label.setText(f"加载图片时发生错误: {e}")

# --- 3. MainWindow (remains largely the same, but now uses QTextBrowser's anchorClicked) ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTextBrowser 超链接与图片示例 (修复版)") # Updated title
        self.setGeometry(100, 100, 800, 600)
        self.init_ui()
        self.load_text_with_images_and_links()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.text_edit = CustomTextEdit(self) # Still instantiating CustomTextEdit
        main_layout.addWidget(self.text_edit)

        # Connect image click signal
        self.text_edit.imageClicked.connect(self.showImageViewerDialog)
        # Crucial: Connect anchorClicked signal (now available from CustomTextEdit (QTextBrowser))
        self.text_edit.anchorClicked.connect(self.handleAnchorClick)

    def load_text_with_images_and_links(self):
        html_content = """
        <h1>文档内容示例</h1>
        <p>这里既有图片，也有<a href="https://www.google.com">外部超链接</a>。</p>
        <p>点击图片会弹出新窗口，点击超链接会触发消息。</p>

        <h2>第一张图片: 风景</h2>
        <img src="22.png" width="300" height="200" />
        <p>点击这张图片来查看它。</p>

        <h2>本地链接示例</h2>
        <p>这是一个<a href="#local_section_id">指向文档内部的链接</a>。</p>
        <p>这部分内容在下面，点击链接会滚动到这里。</p>
        <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        <h2 id="local_section_id">本地链接的目标</h2>
        <p>你已滚动到本地链接的目标位置！</p>

        <h2>第二张图片: 抽象</h2>
        <img src="33.png" width="250" height="250" />
        <p>点击这张图片。</p>

        <p>请访问 <a href="https://www.qt.io">Qt 官网</a> 获取更多信息。</p>
        """
        self.text_edit.setHtml(html_content)

    #@Slot(str)
    def showImageViewerDialog(self, image_path):
        dialog = ImageViewerDialog(image_path, self)
        dialog.exec_() # Modal display

    #@Slot(QUrl) # Slot function receives a QUrl parameter
    def handleAnchorClick(self, url):
        """Handle hyperlink click events"""
        if url.scheme() == "http" or url.scheme() == "https":
            # External link
            QMessageBox.information(self, "外部链接", f"你点击了一个外部链接:\n{url.toString()}")
            # If you want to open in an external browser, uncomment the line below:
            # import webbrowser
            # webbrowser.open(url.toString())
        elif url.fragment(): # Check if it's a fragment (e.g., #local_id)
            # Internal link within the document
            self.text_edit.scrollToAnchor(url.fragment())
            QMessageBox.information(self, "内部链接", f"已滚动到文档内部锚点:\n#{url.fragment()}")
        else:
            # Other custom schemes or local file paths not handled as image
            QMessageBox.information(self, "自定义或本地链接", f"你点击了一个未处理的链接:\n{url.toString()}")

# --- Entry Point ---
if __name__ == "__main__":
    from PyQt5.QtWidgets import QDesktopWidget # Import QDesktopWidget to get screen size

    app = QApplication(sys.argv)
    app.desktop = QDesktopWidget() # Store desktop widget

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())