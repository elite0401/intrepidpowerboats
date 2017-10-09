from intrepidboats.apps.common.models import SiteMetaData


def site_metadata_processor(request):
    cms_metadata = None
    if hasattr(request, 'current_page'):
        if hasattr(request.current_page, 'metadata'):
            cms_metadata = request.current_page.metadata
    return {
        'cms_metadata': cms_metadata,
        'site_metadata': SiteMetaData.objects.get(),
    }
