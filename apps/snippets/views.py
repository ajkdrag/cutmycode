from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Snippet
from django.urls import reverse_lazy


class ExploreView(ListView):
    model = Snippet
    template_name = "explore.html"
    paginate_by = 2
    context_object_name = "snippets"


class DashboardView(LoginRequiredMixin, ListView):
    model = Snippet
    template_name = "dashboard.html"
    context_object_name = "snippets"
    paginate_by = 2
    ordering = "-created_at"

    def get_queryset(self):
        return Snippet.objects.filter(user=self.request.user)


class SnippetCreateView(LoginRequiredMixin, CreateView):
    model = Snippet
    template_name = "snippet_create.html"
    fields = ("title", "description", "code", "language")
    # success_url = reverse_lazy("snippets:dashboard")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippet_detail.html"
    context_object_name = "snippet"


class SnippetEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Snippet
    template_name = "snippet_edit.html"
    fields = ["title", "description", "code", "language"]

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class SnippetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Snippet
    template_name = "snippet_delete.html"
    success_url = reverse_lazy("snippets:dashboard")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
