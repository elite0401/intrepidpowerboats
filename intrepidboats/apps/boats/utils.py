from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext as _


def send_built_boat_email(built_boat, contact_sales):
    context = {
        'built_boat': built_boat,
        'email': built_boat.email,
        'name': built_boat.name,
        'site': Site.objects.get_current().domain,
        'image_url': built_boat.image.url,
    }

    if contact_sales:
        message = render_to_string('boats/emails/built_boats_email.txt', context)
        html_message = render_to_string('boats/emails/built_boats_email.html', context)
    else:
        message = render_to_string('boats/emails/built_boats_just_user_email.txt', context)
        html_message = render_to_string('boats/emails/built_boats_just_user_email.html', context)

    send_mail(
        subject=_("Your boat image - Intrepid Powerboats"),
        message=message,
        from_email=settings.BUILD_A_BOAT['NO_REPLY_EMAIL'],
        recipient_list=[built_boat.email],
        html_message=html_message,
    )


def send_built_boat_email_sales(built_boat):
    context = {
        'built_boat': built_boat,
        'email': built_boat.email,
        'name': built_boat.name,
        'site': Site.objects.get_current().domain,
        'admin_url': reverse("admin:boats_builtboatemail_change", args=[built_boat.pk]),
        'image_url': built_boat.image.url,
    }

    send_mail(
        subject=_("A user has built a boat - Intrepid Powerboats"),
        message=render_to_string('boats/emails/built_boats_email_sales_contact.txt', context),
        from_email=settings.BUILD_A_BOAT['NO_REPLY_EMAIL'],
        recipient_list=settings.BUILD_A_BOAT['SALES_CONTACT'],
        html_message=render_to_string('boats/emails/built_boats_email_sales_contact.html', context),
    )


def send_optional_equipment_user_mail(email, equipment_list, boat_model, first_name, last_name, intrepid_also):
    context = {
        'equipment_list': equipment_list,
        'boat_model': boat_model,
        'first_name': first_name,
        'last_name': last_name,
    }

    if intrepid_also:
        message = render_to_string('boats/emails/optional_equipment_user_intrepid_also_email.txt', context)
        html_message = render_to_string('boats/emails/optional_equipment_user_intrepid_also_email.html', context)
    else:
        message = render_to_string('boats/emails/optional_equipment_user_email.txt', context)
        html_message = render_to_string('boats/emails/optional_equipment_user_email.html', context)

    send_mail(
        subject=_("Optional equipment for your {boat_model} - Intrepid Powerboats".format(boat_model=boat_model)),
        message=message,
        from_email=settings.BUILD_A_BOAT['NO_REPLY_EMAIL'],
        recipient_list=[email],
        html_message=html_message,
    )


def send_optional_equipment_intrepid_mail(email, equipment_list, boat_model, first_name, last_name, phone_number):
    context = {
        'equipment_list': equipment_list,
        'boat_model': boat_model,
        'first_name': first_name,
        'last_name': last_name,
        'phone_number': phone_number,
        'email': email,
    }

    send_mail(
        subject=_("Optional equipment for your {boat_model} - Intrepid Powerboats".format(boat_model=boat_model)),
        message=render_to_string('boats/emails/optional_equipment_intrepid_email.txt', context),
        from_email=settings.BUILD_A_BOAT['NO_REPLY_EMAIL'],
        recipient_list=settings.TO_EMAIL['OPTIONAL_EQUIPMENT_TAB_FORM'],
        html_message=render_to_string('boats/emails/optional_equipment_intrepid_email.html', context),
    )


# pylint: disable=redefined-outer-name
# pylint: disable=unused-argument
def rotate(image, degrees, **kwargs):
    return image.rotate(degrees, expand=True)
