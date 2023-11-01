from django.contrib.auth.models import Group
from django.contrib.auth.mixins import AccessMixin



class GroupRequiredMixin(AccessMixin):
    permission_denied_message = 'You have no permission for that section...'
    group_name = 'Statistic'
    group = None

    def get_group(self):
        return self.group_name

    def dispatch(self, request, *args, **kwargs):
        try:
            self.group = Group.objects.get(name=self.get_group())
        except Group.DoesNotExist:
            return self.handle_no_permission()

        if not request.user.is_authenticated or self.group not in request.user.groups.all():
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)