from django.contrib.auth.mixins import LoginRequiredMixin


class OrganisorAndLoginRequiredMixin(LoginRequiredMixin):
    
    """Verify that the current user is authenticated and organisor."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organisor:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)