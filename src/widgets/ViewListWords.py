from typing import TYPE_CHECKING

from src.widgets.ViewWord import ViewWord
from .WidgetVerticalLayoutScrollForWords import WidgetVerticalLayoutScrollForWords

if TYPE_CHECKING:
    pass
# from .WidgetVerticalLayoutScroll import WidgetVerticalLayoutScroll


class ViewListWords(WidgetVerticalLayoutScrollForWords):

    def get_create_widget(self, item):
        return ViewWord(item)
