import json

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from intrepidboats.libs.colorize.utils import get_image_colorized, yatint_image, tint_image
from .forms import OptionalEquipmentForm
from .models import Boat, BoatModelGroup, BuiltBoatEmail, BuiltBoatShare, BoatGeneralFeature, DeckPlan, AboutTheBoat, \
    AboutTheBoatImage, OptionalEquipment, BoatLengthGroup
from .utils import send_optional_equipment_user_mail, send_optional_equipment_intrepid_mail


class BoatModelGroupListView(TemplateView):
    template_name = 'boats/all_models.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = BoatLengthGroup.objects.all().order_by('title')
        context['model_groups'] = BoatModelGroup.objects.all()
        return context


class BoatModelListView(ListView):
    context_object_name = "boats"
    template_name = "boats/list.html"

    def get_queryset(self):
        return Boat.objects.prefetch_related("model_group").all()


class BoatLengthGroupDetailView(DetailView):
    template_name = "boats/groups/details.html"

    def get_queryset(self):
        return BoatLengthGroup.objects.prefetch_related("boats").all()

    def get_context_data(self, **kwargs):
        context = super(BoatLengthGroupDetailView, self).get_context_data(**kwargs)
        group = context["object"]
        boats = group.boats.all()
        context["boats"] = boats
        return context


class BoatListPerGroupCompare(ListView):
    template_name = "boats/compare.html"
    query_pk_and_slug = True
    context_object_name = "boats"

    def get_queryset(self):
        pks = self.request.GET.getlist("comparing_boats", [])
        return Boat.objects.filter(length_group__pk=self.kwargs["pk"], pk__in=pks).all()


class BoatListCompare(ListView):
    template_name = "boats/compare.html"
    query_pk_and_slug = True
    context_object_name = "boats"

    def get_queryset(self):
        pks = self.request.GET.getlist("comparing_boats", [])
        return Boat.objects.filter(pk__in=pks).all()


class BoatDetailView(DetailView):
    query_pk_and_slug = True

    def get_queryset(self):
        return Boat.objects. \
            prefetch_related("motor_selections__motor"). \
            prefetch_related("features__options").all()

    def get_context_data(self, **kwargs):
        context = super(BoatDetailView, self).get_context_data(**kwargs)
        context['all_models'] = Boat.objects.all()
        context['features'] = self.object.get_available_features()
        context['motor_selections'] = self.object.motor_selections.all()
        context['boat_models'] = {'general_feature': BoatGeneralFeature, 'deck_plan': DeckPlan, 'about': AboutTheBoat,
                                  'about_image': AboutTheBoatImage, 'optional_equipment': OptionalEquipment}
        context['optional_equipment_form'] = self.process_optional_equipment_form()
        context['vimeo_ids'] = json.dumps(list(self.object.videos.all().values_list('vimeo_video_code', flat=True)))
        if self.request.flavour == 'full':  # Only load this for desktop
            self.context_data_for_about(context)
        context['current_site'] = Site.objects.get_current().domain
        return context

    def process_optional_equipment_form(self):
        optional_equipment_form = OptionalEquipmentForm(self.request.GET)
        data = optional_equipment_form.data
        if 'equipment' in data:
            equipment_list = json.loads(data['equipment'])['selected_items']
            boat_model = json.loads(data['equipment'])['boat_model']
            intrepid_also = 'email_intrepid_also' in data and data['email_intrepid_also'] == 'on'
            send_optional_equipment_user_mail(
                data['email_address'], equipment_list, boat_model, data['first_name'], data['last_name'], intrepid_also
            )
            if intrepid_also:
                send_optional_equipment_intrepid_mail(
                    data['email_address'], equipment_list, boat_model, data['first_name'], data['last_name'],
                    data['phone_number']
                )
            messages.add_message(self.request, messages.SUCCESS, '(Placeholder)')
        return optional_equipment_form

    def context_data_for_about(self, context):
        thumbnails_per_page = settings.THUMBNAILS_PER_PAGE
        interior_galleries, exterior_galleries, cabin_galleries = [], [], []
        if hasattr(self.object, 'about'):
            interior_galleries = self.sub_galleries_for(self.object.about.interior_gallery(), thumbnails_per_page)
            exterior_galleries = self.sub_galleries_for(self.object.about.exterior_gallery(), thumbnails_per_page)
            cabin_galleries = self.sub_galleries_for(self.object.about.cabin_gallery(), thumbnails_per_page)
        context['interior_galleries'] = interior_galleries
        context['exterior_galleries'] = exterior_galleries
        context['cabin_galleries'] = cabin_galleries
        return context

    def sub_galleries_for(self, gallery, thumbnails_per_page):
        cant_pages = int(gallery.count() / thumbnails_per_page)
        cant_pages = cant_pages if gallery.count() % thumbnails_per_page == 0 else cant_pages + 1
        sub_galleries = []
        for page in range(cant_pages):
            from_index, to_index = page * thumbnails_per_page, (page + 1) * thumbnails_per_page
            sub_gallery = gallery[from_index:to_index]
            sub_galleries.append(sub_gallery)
        return sub_galleries

    def render_to_response(self, context, **response_kwargs):
        if context['optional_equipment_form'].data:
            return redirect(self.request.path)
        return super().render_to_response(context, **response_kwargs)


class BuildABoatView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(BuildABoatView, self).get_context_data(**{**kwargs, **{"is_build_a_boat": True}})


class MotorsView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(MotorsView, self).get_context_data(**{**kwargs, **{"is_motors": True}})


class AboutView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(AboutView, self).get_context_data(**{**kwargs, **{"is_about": True}})


class VideoView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(VideoView, self).get_context_data(**{**kwargs, **{"is_video": True}})


class OptionalEquipmentView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(OptionalEquipmentView, self).get_context_data(**{**kwargs, **{"is_optional_equipment": True}})


class DeckPlanView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(DeckPlanView, self).get_context_data(**{**kwargs, **{"is_deck_plan": True}})


class FeaturesView(BoatDetailView):
    def get_context_data(self, **kwargs):
        return super(FeaturesView, self).get_context_data(**{**kwargs, **{"is_features": True}})


class ModelPageHome(BoatDetailView):
    template_name = 'boats/boat_detail.html'


@require_GET
@cache_page(60 * 15)
def colorize(request, slug, image, color):
    boat = get_object_or_404(Boat, slug=slug)
    if image not in ['hull', 'boot_stripe', 'boot_stripe_accent', 'sheer_stripe', 'sheer_stripe_accent', 'logo']:
        raise Http404()

    image_file = Image.open(getattr(boat, image).file)
    response = HttpResponse(content_type="image/png")
    colorized = yatint_image(image_file, "#" + color)
    colorized.save(response, "PNG")
    return response


class BuiltBoatEmailCreateView(CreateView):
    model = BuiltBoatEmail
    template_name = "boats/detail/partials/built_boat_email_form.html"
    fields = ['name', 'email', 'image_url', 'phone', 'contact_sales']

    success_message = _("your email has been sent")

    def __init__(self, **kwargs):
        self.object = None
        super(BuiltBoatEmailCreateView, self).__init__(**kwargs)

    def form_valid(self, form):
        form.instance.boat = self.get_boat()
        self.object = form.save()
        self.object.decode_image()
        self.object.send_email()
        return HttpResponse(content=self.success_message, status=201)

    def get_boat(self):
        slug = self.kwargs['slug']
        return Boat.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        return super(BuiltBoatEmailCreateView, self).get_context_data(boat=self.get_boat(), **kwargs)


class BuiltBoatShareCreateView(CreateView):
    model = BuiltBoatShare
    fields = ['image_url']
    success_text = _("thanks for sharing!")
    text_post = 'Check out the Intrepid I just custom built'

    def __init__(self, **kwargs):
        self.object = None
        super(BuiltBoatShareCreateView, self).__init__(**kwargs)

    def form_valid(self, form):
        form.instance.boat = self.get_boat()
        self.object = form.save()
        self.object.decode_image()

        path = self.object.image.url

        return JsonResponse(
            data={
                "url": self.request.build_absolute_uri(path),
                "success_text": self.success_text,
                "text_post": self.text_post,
                "current_site": Site.objects.get_current().domain
            },
            status=201,
        )

    def get_boat(self):
        slug = self.kwargs['slug']
        return Boat.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        return super(BuiltBoatShareCreateView, self).get_context_data(boat=self.get_boat(), **kwargs)
