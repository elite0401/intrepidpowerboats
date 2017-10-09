from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods, require_GET
from django.views.generic import CreateView

from intrepidboats.apps.difference.models import SharedTestimonial, SharedTestimonialUploadInfo, \
    SharedTestimonialInfoBuilder
from intrepidboats.apps.difference.utils import send_shared_testimonial_email, send_new_testimonial_video_uploaded_email


class SharedTestimonialCreateView(CreateView):
    model = SharedTestimonial
    template_name = "difference/shared_testimonials/_form.html"
    fields = ['first_name', "last_name", "title", "email", "file", "message"]
    success_message = _("Thank you!")

    def form_valid(self, form):
        testimonial = form.save(commit=False)
        if 'video' in form.cleaned_data['file'].content_type:
            testimonial.file = None
            testimonial.info = SharedTestimonialUploadInfo.objects.get(ticket_id=form.data['ticket-id'])
        testimonial.save()
        send_new_testimonial_video_uploaded_email(testimonial)
        send_shared_testimonial_email(testimonial, self.request.META['HTTP_HOST'])
        return HttpResponse(content=self.get_success_message(), status=201)

    def form_invalid(self, form):
        return JsonResponse(data=form.errors, status=422)

    def get_success_message(self):
        return self.success_message


@require_GET
def create_upload_ticket(request):
    builder = SharedTestimonialInfoBuilder.default()
    testimonial_info = builder.create_testimonial_info()

    data = {
        "upload_link_secure": testimonial_info.upload_link_secure,
        "complete_path": reverse("difference:complete_ticket", kwargs={"ticket_id": testimonial_info.ticket_id}),
        "ticket_id": testimonial_info.ticket_id
    }
    return JsonResponse(data=data)


@require_http_methods(request_method_list=["PUT"])
def complete_upload_ticket(request, ticket_id):
    builder = SharedTestimonialInfoBuilder.default()
    builder.finish_upload(ticket_id=ticket_id)

    return JsonResponse(data={})
