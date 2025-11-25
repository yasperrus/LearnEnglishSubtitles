from src.core.theme_manager import ThemeManager


class ThemeWidget:

    def __init__(self):
        ThemeManager().subscribe(self)

    def apply_theme(self, theme):
        if not theme:
            return

        if hasattr(self, "main_widget"):
            self.main_widget.setVisible(True)
            self.main_widget.setStyleSheet(
                f"""#main_widget {{
                         background: qlineargradient(
                            spread:pad,
                            x1:0, y1:1, x2:1, y2:1,
                            stop:0 {theme.primary_bg},
                            stop:1 {theme.secondary_bg}
                        )
                     }}
                    QPushButton {{
                        border-radius: 8px;
                        margin-left: 10px;
                        margin-right: 10px;
                        padding-top: 5px;
                        padding-bottom: 5px;
                        padding-left: 15px;
                        padding-right: 15px;
                        border: 1px solid #ffffff;
                        background-color: rgba(255, 255, 255, 120); 
                        color: black;  
                    }}
                    
                    QPushButton:hover {{
                        background-color: rgba(255, 255, 255, 150); 
                    }}
                    
                    QPushButton:pressed {{
                        background-color: rgba(255, 255, 255, 192);
                    }}
                    QWidget, QLabel, QPushButton {{
                        color: {theme.text_color};
                     }}
                     
                     """
            )

        if hasattr(self, "test_main_widget"):
            self.test_main_widget.setVisible(True)
            self.test_main_widget.setStyleSheet(
                f"""#test_main_widget {{
                         background: qlineargradient(
                            spread:pad,
                            x1:0, y1:1, x2:1, y2:1,
                            stop:0 {theme.primary_bg},
                            stop:1 {theme.secondary_bg}
                        )
                     }}
                     QWidget, QLabel, QPushButton, QLineEdit {{
                        color: {theme.text_color};
                     }}
                     """
            )

        if hasattr(self, "list_widget"):
            self.list_widget.setVisible(True)
            self.list_widget.setStyleSheet(
                f"""#list_widget {{
                     background: qlineargradient(
                        spread:pad,
                        x1:0, y1:1, x2:1, y2:1,
                        stop:0 {theme.primary_bg},
                        stop:1 {theme.secondary_bg}
                    );
                 }}
                 """
            )

        if hasattr(self, "config_widget"):
            self.config_widget.setVisible(True)
            self.config_widget.setStyleSheet(
                f"""#config_widget {{
                     background: qlineargradient(
                        spread:pad,
                        x1:0, y1:1, x2:1, y2:1,
                        stop:0 {theme.secondary_bg},
                        stop:1 {theme.primary_bg}
                    )
                 }}
                 """
            )

        if hasattr(self, "but_primary_bg"):
            self.but_primary_bg.setStyleSheet(
                f" #but_primary_bg {{  background: {theme.primary_bg}; padding: 0px; margin: 0px;  border-radius: 13px; }}"
            )

        if hasattr(self, "but_secondary_bg"):
            self.but_secondary_bg.setStyleSheet(
                f"#but_secondary_bg {{  background: {theme.secondary_bg}; padding: 0px; margin: 0px; border-radius: 13px; }}"
            )

        if hasattr(self, "but_text_bg"):
            self.but_text_bg.setStyleSheet(
                f"#but_text_bg {{ background: {theme.text_color}; padding: 0px; margin: 0px;  border-radius: 13px; }}"
            )
