from faker import Factory

from intrepidboats.apps.common.models import PageSetting, PageAsset

fake = Factory.create()


def a_page_setting():
    return PageSetting.objects.create(
        name=fake.name()
    )


def a_page_asset(page_setting, **kwargs):
    defaults = {
        "page": page_setting,
        "vimeo_video_code": fake.ean8(),
        "video_external_url": fake.url(),
        "image": None,
        "enabled": True,
        "is_last": False,
    }
    return PageAsset.objects.create(**{
        **defaults,
        **kwargs,
    })
