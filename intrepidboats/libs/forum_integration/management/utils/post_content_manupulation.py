import re

URL_FORMATS = {
    'OLD_FORMAT': r'\[(?:url|URL)=.*?\].*?\[/(?:url|URL)\]',
    'OLD_FORMAT_BY_GROUPS': r'\[(?:url|URL)=(.*)?\](.*)?\[/(?:url|URL)\]',
    'NEW_FORMAT_BY_GROUPS': "[\g<2>](\g<1>)",
}

IMG_FORMATS = {
    'OLD_FORMAT': r'\[(?:img|IMG)\].*?\[/(?:img|IMG)\]',
    'OLD_FORMAT_BY_GROUPS': r'\[(?:img|IMG)\](.*)?\[/(?:img|IMG)\]',
    'NEW_FORMAT_BY_GROUPS': "![](\g<1>)",
}

IMG_ALT_FORMATS = {
    'OLD_FORMAT': r'\[(?:img|IMG)=.*?\].*?\[/(?:img|IMG)\]',
    'OLD_FORMAT_BY_GROUPS': r'\[(?:img|IMG)=(.*)?\](.*)?\[/(?:img|IMG)\]',
    'NEW_FORMAT_BY_GROUPS': "![\g<2>](\g<1>)",
}


def get_url_blocks_from(text, old_format):
    blocks = []
    matches = re.finditer(old_format, text)
    for match in matches:
        blocks.append(match.group())
    return blocks


def replace_block_in(text, block, new_block):
    return text.replace(block, new_block)


def new_block_from(url_block, old_format, new_format):
    return re.sub(old_format, new_format, url_block)


def update_blocks_in(text, formats):
    blocks = get_url_blocks_from(text, formats['OLD_FORMAT'])
    for block in blocks:
        new_block = new_block_from(block, formats['OLD_FORMAT_BY_GROUPS'], formats['NEW_FORMAT_BY_GROUPS'])
        text = replace_block_in(text, block, new_block)
    return text


def update_urls_in(text):
    return update_blocks_in(text, URL_FORMATS)


def update_imgs_in(text):
    text = update_blocks_in(text, IMG_FORMATS)
    return update_blocks_in(text, IMG_ALT_FORMATS)
