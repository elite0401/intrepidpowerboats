from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .models import TestimonialPlugin, TestimonialVideoPlugin, IntrepidDifferenceSectionPlugin, ImageWithTextPlugin


class TestimonialCMSPlugin(CMSPluginBase):
    model = TestimonialPlugin
    name = _("Testimonial")
    render_template = "difference/cms/testimonial.html"
    module = 'Custom'

    def render(self, context, instance, placeholder):
        context = super(TestimonialCMSPlugin, self).render(context, instance, placeholder)
        if len(instance.testimonial.message) <= 300:
            context['first_half'] = instance.testimonial.message
            context['see_more'] = None
        else:
            first_half = instance.testimonial.message[:300].rsplit(' ', 1)
            context['first_half'] = first_half[0]
            context['see_more'] = (first_half[1] if len(first_half) > 1 else '') + instance.testimonial.message[300:]
        return context


class TestimonialVideoCMSPlugin(CMSPluginBase):
    model = TestimonialVideoPlugin
    name = _("Testimonial video")
    render_template = "difference/cms/testimonial_video.html"
    module = 'Custom'


class IntrepidDifferenceSectionCMSPlugin(CMSPluginBase):
    model = IntrepidDifferenceSectionPlugin
    name = _("Intrepid Difference Section")
    render_template = "difference/cms/text_section.html"
    module = 'Custom'
    allow_children = True
    child_classes = ['ImageWithTextPluginCMSPlugin']


class ImageWithTextPluginCMSPlugin(CMSPluginBase):
    model = ImageWithTextPlugin
    name = _("Image with text")
    render_template = "difference/cms/slider_image.html"
    module = 'Custom'


plugin_pool.register_plugin(TestimonialCMSPlugin)
plugin_pool.register_plugin(TestimonialVideoCMSPlugin)
plugin_pool.register_plugin(IntrepidDifferenceSectionCMSPlugin)
plugin_pool.register_plugin(ImageWithTextPluginCMSPlugin)
