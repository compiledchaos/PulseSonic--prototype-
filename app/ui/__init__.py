# Makes app.ui a package for reliable relative imports of subviews

from .main_views.search import SearchView  # noqa: F401
from .main_views.player import PlayerView  # noqa: F401
from .main_views.recs import RecsView  # noqa: F401
