from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from apps.snippets.models import Snippet
from .forms import CommentForm


class CommentCreateView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Snippet
    form_class = CommentForm
    # reuse same template for error display
    template_name = "snippet_detail.html"

    def get(self, request, *args, **kwargs):
        return redirect(self.get_object().get_absolute_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # fetch the Snippet by pk
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.snippet = self.object
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
