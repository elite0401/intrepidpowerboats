import random

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import password_reset as django_password_reset
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.translation import activate, check_for_language
from django.views.generic import TemplateView, CreateView, DetailView, FormView
from el_pagination.views import AjaxListView

from intrepidboats.apps.common.utils import send_successful_registration_emails, send_new_newsletter_subscriber_email, \
    send_new_registered_user_email
from .forms import NewsletterForm, UserRegistrationForm
from .models import PageSetting, NewsletterSubscriber, Article, Event, ExtraUserData


class HomeView(TemplateView):
    template_name = "home/index.html"
    HOME_PAGE_NAME = settings.HOME_PAGE_SETTINGS_NAME

    def get_context_data(self, **kwargs):
        page_setting = self.get_page_setting()
        page_assets = []
        if page_setting:
            page_assets = page_setting.random_assets(is_mobile=self.request.flavour == "mobile")
        return super(HomeView, self).get_context_data(
            page_setting=page_setting, page_assets=page_assets, newsletter_form=NewsletterForm())

    def get_page_setting(self):
        query_set = PageSetting.objects.filter(name=self.HOME_PAGE_NAME)
        if query_set.exists():
            return query_set.first()
        return None


class NewsletterSubmission(CreateView):
    model = NewsletterSubscriber
    form_class = NewsletterForm
    success_url = '/'  # TODO: unused url?

    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        super().form_valid(form)
        send_new_newsletter_subscriber_email(form)
        return JsonResponse({
            'success_page_url': reverse_lazy('common:newsletter_success'),
            'is_mobile': self.request.flavour == 'mobile',
        })


def activate_lang(request):
    lang = request.POST.get("language")
    check_for_language(lang)
    activate(language=lang)
    next_url = request.META.get('HTTP_REFERER')
    return redirect(next_url) if next_url else redirect('/')


class BlogPostDetailView(DetailView):
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        posts = self.model.objects.exclude(id=self.object.id).filter(featured=True)
        posts_to_show_amount = 3 if posts.count() >= 3 else posts.count()
        context['sticky_posts'] = random.sample(set(posts), posts_to_show_amount)
        return context


class WhatIsNewView(AjaxListView):
    model = Article
    context_object_name = 'entry_list'
    template_name = 'blog_posts/what_is_new/whats_new.html'
    page_template = 'blog_posts/what_is_new/article_item.html'


class ArticleDetailView(BlogPostDetailView):
    model = Article
    template_name = 'blog_posts/what_is_new/article_detail.html'


class EventsView(AjaxListView):
    model = Event
    context_object_name = 'entry_list'
    template_name = 'blog_posts/events/events.html'
    page_template = 'blog_posts/events/event_item.html'

    def get_context_data(self, **kwargs):
        return super(EventsView, self).get_context_data(**kwargs)


class RegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        return reverse('common:register-done')

    def form_valid(self, form):
        new_user = self.register(form)
        send_successful_registration_emails(form)
        send_new_registered_user_email(new_user)
        return HttpResponseRedirect(self.get_success_url())

    def register(self, form):
        new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'], )
        new_user.first_name = form.cleaned_data['first_name']
        new_user.last_name = form.cleaned_data['last_name']
        new_user.save()
        print (form)
        ExtraUserData.objects.create(user=new_user, phone=form.cleaned_data['phone'])
        new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(self.request, new_user)
        return new_user


def password_reset(request, template_name, email_template_name, subject_template_name, post_reset_redirect, from_email):
    return django_password_reset(request, template_name=template_name, email_template_name=email_template_name,
                                 subject_template_name=subject_template_name, post_reset_redirect=post_reset_redirect,
                                 from_email=from_email, extra_email_context={'domain': request.META['HTTP_HOST']})


def login_view(*args):
    return django_login(*args, redirect_authenticated_user=True)
