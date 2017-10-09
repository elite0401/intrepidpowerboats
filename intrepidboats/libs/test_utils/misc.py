def refresh(model_instance):
    return (type(model_instance)).objects.get(pk=model_instance.pk)
