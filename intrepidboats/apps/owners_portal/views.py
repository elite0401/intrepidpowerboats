from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import CreateView, UpdateView
from django.views.generic import TemplateView, RedirectView

from intrepidboats.apps.common.models import ExtraUserData
from intrepidboats.apps.common.utils import split_queryset
from intrepidboats.apps.contact.views import SendInformationFormInvalidMixin
from .forms import SharedPictureForm, AccountSettingsForm
from .models import SharedVideoBuilder, StepFeedback, BoatStep, UserBoat, SharedPicture, SharedMedia, Survey
from .utils import send_report_email, send_step_feedback_email


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "owners_portal/index.html"

    def get_context_data(self, **kwargs):

        if self.request.user.is_authenticated():
            my_stuff = self.get_gallery({'uploader': self.request.user})
            profile, _ = ExtraUserData.objects.get_or_create(user=self.request.user)
        else:
            my_stuff = None
            profile = None
        # get a random survey, if any
        survey = Survey.objects.filter(enabled=True).order_by('?').first()
        return super().get_context_data(
            last_boat=self.get_last_boat(),
            my_stuff=my_stuff,
            community_shares=self.get_gallery({'is_public': True, 'is_approved': True}),
            share_picture_form=SharedPictureForm(),
            current_site=Site.objects.get_current().domain,
            profile=profile,
            survey=survey,
            **kwargs
        )

    def get_last_boat(self):
        if self.request.user.is_authenticated() and self.request.user.user_boats.count() > 0:
            return self.request.user.user_boats.prefetch_related("steps__assets").last()
        else:
            return None

    def get_gallery(self, attrs):
        gallery = SharedMedia.objects.media_content(attrs=attrs)
        return split_queryset(gallery, 10)


class GalleryView(LoginRequiredMixin, RedirectView):
    pattern_name = 'owners_portal:owners_portal'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs) + '#gallery'


class EditBoatNameView(LoginRequiredMixin, UpdateView):
    success_url = '/'
    model = UserBoat
    fields = ['name']

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'new_name': self.object.name})


class AccountSettingsView(LoginRequiredMixin, SendInformationFormInvalidMixin, UpdateView):
    model = ExtraUserData
    form_class = AccountSettingsForm
    template_name = 'owners_portal/partials/account_settings_form.html'
    success_url = reverse_lazy('owners_portal:owners_portal')

    def form_valid(self, form):
        if form.cleaned_data['first_name']:
            self.request.user.first_name = form.cleaned_data['first_name']
        if form.cleaned_data['last_name']:
            self.request.user.last_name = form.cleaned_data['last_name']
        self.request.user.save()
        return super().form_valid(form)


class UploadPictureView(LoginRequiredMixin, CreateView):
    model = SharedPicture
    form_class = SharedPictureForm
    template_name = 'owners_portal/partials/gallery_picture_form.html'

    def get_success_url(self):
        return reverse('owners_portal:owners_portal') + '#gallery'

    def form_invalid(self, form):
        super().form_invalid(form)
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        form.is_approved = False
        messages.add_message(self.request, messages.SUCCESS, _('Success! Your item has been uploaded'))
        return super().form_valid(form)


@login_required
@staff_member_required
@require_POST
def change_notification(request, step_pk):
    step = get_object_or_404(BoatStep, pk=step_pk)
    send_report_email(step.user_boat)
    return JsonResponse(data={}, status=200)


class StepFeedbackCreateView(LoginRequiredMixin, CreateView):
    model = StepFeedback
    fields = ('comments',)
    object = None

    def get_context_data(self, **kwargs):
        return super(StepFeedbackCreateView, self).get_context_data(step=self.get_step(), **kwargs)

    def form_valid(self, form):
        feedback = form.instance
        feedback.user = self.request.user
        feedback.step = self.get_step()
        self.object = form.save()
        send_step_feedback_email(self.object)
        return JsonResponse({"ok": True, "message": _("Thank you!")}, status=201)

    def get_step(self):
        return BoatStep.objects.for_user(self.request.user).get(pk=self.kwargs['pk'])

    def get_initial(self):
        return {
            "user": self.request.user,
            "step_id": self.get_step().pk
        }


@require_POST
@login_required
@ensure_csrf_cookie
def create_upload_ticket(request):
    builder = SharedVideoBuilder.default()
    form_data = dict(request.POST)

    video = builder.create_video(
        request.user,
        comment=form_data['comment'][0],
        is_public=(form_data['is_public'][0] == 'True'),
    )

    data = {
        "upload_link_secure": video.upload_link_secure,
        "complete_path": reverse("owners_portal:complete_ticket", kwargs={"ticket_id": video.ticket_id})
    }
    return JsonResponse(data=data)


@require_http_methods(request_method_list=["PUT"])
@login_required
def complete_upload_ticket(request, ticket_id):
    builder = SharedVideoBuilder.default()
    builder.finish_upload(ticket_id=ticket_id, user=request.user)
    builder.send_new_uploaded_video_email(ticket_id, request.user)
    messages.add_message(request, messages.SUCCESS, _('Success! Your item has been uploaded'))
    return JsonResponse(data={})


def get_slide(request, media_id):
    gallery = SharedMedia.objects.media_content(attrs={'is_public': True, 'is_approved': True}).values_list('id',
                                                                                                            flat=True)
    galleries = split_queryset(gallery, 10)
    slide = None
    for index, sub_gallery in enumerate(galleries):
        if int(media_id) in sub_gallery:
            slide = index
            break
    return JsonResponse(data={'slide': slide, 'media_id': media_id})
