from sqlalchemy.orm import configure_mappers

from .LearnedWord import LearnedWord
from .LearningWord import LearningWord
from .PathOfSpeech import PathOfSpeech
from .Statuses import Statuses
from .SubtitleList import SubtitleList
from .SubtitleListAssociationWord import SubtitleListAssociationWord
from .User import User
from .UserAssociationSubtitleList import UserAssociationSubtitleList
from .WordWithTranslations import WordWithTranslations

# и так далее

# склеиваем все мапперы после загрузки
configure_mappers()
