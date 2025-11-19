class ThemeManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = []
            cls._instance._current_theme = None
        return cls._instance

    def subscribe(self, widget):
        self._subscribers.append(widget)

    def set_theme(self, theme):
        self._current_theme = theme
        self._notify()

    def _notify(self):
        for widget in self._subscribers:
            widget.apply_theme(self._current_theme)

    def get_theme(self):
        return self._current_theme
