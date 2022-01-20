from app.viewsets import PublicationViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('publication', PublicationViewSet)
router.register(r'publication', PublicationViewSet, basename='publication')
router.register('user', UserViewSet)

