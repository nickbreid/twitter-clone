from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
    )

from .models import Tweet
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin


# Create

class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'

    # model function get_absolute_url handles this dynamically
    # with that method defined, django automatically goes there
    # success_url = reverse_lazy('tweet:detail')

    # for use with LoginRequiredMixin
    # login_url = '/admin/'

    # big advantage of class-based views: you can use mixins.
    # this was refactored into mixins.py as FormUserNeededMixin
    #
    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
    #
    #     if self.request.user.is_authenticated():
    #         form.instance.user = self.request.user
    #         return super(TweetCreateView, self).form_valid(form)
    #     else:
    #         form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList(["User must be logged in to tweet."])
    #         return self.form_invalid(form)

# Update

class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    form_class = TweetModelForm
    # success_url = '/tweet/'
    template_name = 'tweets/update_view.html'
    queryset = Tweet.objects.all()


# Delete

class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = 'tweets/delete_confirm.html'
    success_url = reverse_lazy('tweet:list')

# List / Search

# Retrieve

# retrieve with class-based views
class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()

    # this function happens behind the scenes with a class-based view
    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return Tweet.objects.get(id=pk)

class TweetListView(ListView):

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all()
        query = self.request.GET.get("q", None)

        if query is not None:
            qs = qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy("tweet:create")
        return context



# retrieve with function-based views
# def tweet_detail_view(request, pk=None): # pk == id
#     obj = Tweet.objects.get(pk=pk) # GET from db
#     context = {
#         "object": obj
#     }
#     return render(request, "tweets/detail_view.html", context)
#
#
# def tweet_list_view(request):
#     queryset = Tweet.objects.all()
#     context = {
#         "object_list": queryset
#     }
#     return render(request, "tweets/list_view.html", context )
