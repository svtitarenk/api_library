from django.urls import path, include
from rest_framework.routers import SimpleRouter
from library.apps import LibraryConfig
from library.views import BookViewSet, AuthorViewSet, BookIssueViewSet

# проводим стандартные настройки. Указываем приложение, импортируем из habits.apps.HabitsConfig
app_name = LibraryConfig.name

# присваиваем экземпляр класса
router = SimpleRouter()

# прописывем путь, по которому будет в пустом пути '', показываться ViewSet
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-issues', BookIssueViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]
# к urlpatterns добавляем наши urls
urlpatterns += router.urls
