from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, StepViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'steps', StepViewSet, basename='step')
router.register(r'', RecipeViewSet, basename='recipe')

urlpatterns = router.urls
