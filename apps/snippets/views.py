from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseForbidden

from .models import SharedSnippet, Snippet
from .forms import SnippetCreateForm, SnippetEditForm
from apps.comments.forms import CommentForm

#############
# List views
#############


class ExploreView(ListView):
    model = Snippet
    template_name = "explore.html"
    paginate_by = 8
    context_object_name = "snippets"


class DashboardView(LoginRequiredMixin, ListView):
    model = Snippet
    template_name = "dashboard.html"
    context_object_name = "snippets"
    paginate_by = 2
    ordering = "-created_at"

    def get_queryset(self):
        return Snippet.objects.filter(user=self.request.user)


##############
# CRUD stuff
##############


class SnippetCreateView(LoginRequiredMixin, CreateView):
    model = Snippet
    form_class = SnippetCreateForm
    template_name = "snippet_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippet_detail.html"
    context_object_name = "snippet"

    # show the comment form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        pass


class SnippetEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Snippet
    form_class = SnippetEditForm
    template_name = "snippet_edit.html"

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


###############
# Share stuff
###############


class CreateShareLinkView(LoginRequiredMixin, View):
    """
    Creates a temporary, shareable link for a snippet.
    """

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, pk=kwargs["pk"])
        shared_snippet = SharedSnippet.objects.create(snippet=snippet)
        return redirect(shared_snippet.get_absolute_url())


class SharedSnippetDetailView(DetailView):
    model = SharedSnippet
    template_name = "shared_snippet_detail.html"
    context_object_name = "shared_snippet"
    # name of the model field that contains the slug
    slug_field = "token"
    # name of the url parameter that contains the slug
    slug_url_kwarg = "token"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the actual 'snippet' object to the template, not the 'SharedSnippet'
        context["snippet"] = self.object.snippet
        return context
