from django.db.models.signals import pre_save, post_save
from django.test import TestCase
from nose.tools import assert_equals
from nose.tools import assert_false
from nose.tools import assert_not_in
from nose.tools import assert_true
from nose.tools import istest

from intrepidboats.apps.common.models import PageAsset
from intrepidboats.apps.common.signals import update_external_url, set_external_url
from intrepidboats.libs.fixtures.page_setting import a_page_setting, a_page_asset
from intrepidboats.libs.test_utils.misc import refresh


class TestSharedVideoCreation(TestCase):
    def setUp(self):
        self.page_setting = a_page_setting()
        pre_save.disconnect(receiver=update_external_url, sender=PageAsset)
        post_save.disconnect(receiver=set_external_url, sender=PageAsset)

    @istest
    def page_assets_allow_just_one_is_last(self):
        first = a_page_asset(self.page_setting)
        last = a_page_asset(self.page_setting, is_last=True)
        assert_true(last.is_last)
        assert_false(first.is_last)

        first.is_last = True
        first.save()

        assert_false(refresh(last).is_last)
        assert_true(refresh(first).is_last)

    @istest
    def return_is_last_asset_at_the_end(self):
        last = a_page_asset(self.page_setting, is_last=True)
        for _ in range(10):
            a_page_asset(self.page_setting)

        assert_equals(last, self.page_setting.assets.last())

    @istest
    def return_random_order_of_assets_but_the_last_one_has_is_last_attr_true(self):
        a_page_asset(self.page_setting, is_last=True)
        for _ in range(10):
            a_page_asset(self.page_setting)

        last = self.page_setting.random_assets()[-1]
        assert_true(last.is_last)

    @istest
    def filter_by_enabled_attr(self):
        a_page_asset(self.page_setting, enabled=True)
        second = a_page_asset(self.page_setting, enabled=False)
        queryset = self.page_setting.assets_queryset().all()
        assert_not_in(second, queryset)
