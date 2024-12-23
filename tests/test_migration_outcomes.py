from django.test import TestCase
from testapp.constants import ORIGINAL_BODY_VALUE, MODIFIED_BODY_VALUE
from testapp.models import TestPage, TestSnippet


class TestMigrationOutcomes(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i, page in enumerate(TestPage.objects.all().order_by("id"), start=1):
            setattr(cls, f"page_{i}", page)
        for i, snippet in enumerate(TestSnippet.objects.all().order_by("id"), start=1):
            setattr(cls, f"snippet_{i}", snippet)

    def test_original_pages_and_snippets_have_retained_their_original_body_values(self):
        """
        Test the objects created in `0002_create_test_objects` and DID NOT have their `body` value
        updated in later migrations have retained their original values after:

        - Swapping the native StreamField for a custom one in `0003_swap_native_streamfield_for_mlstreamfield`
        - Updating their title in `0007_modify_title_values` and resaving
        - Updating their title in `0008_modify_title_values_with_bulk_update` via a bulk update
        """
        self.assertEqual(self.page_1.title, "Modified Test Page")
        self.assertEqual(len(self.page_1.body.raw_data), 3)
        for i, block in enumerate(self.page_1.body.raw_data):
            compare_to = ORIGINAL_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

        self.assertEqual(self.snippet_1.title, "Modified Test Snippet")
        self.assertEqual(len(self.snippet_1.body.raw_data), 3)
        for i, block in enumerate(self.snippet_1.body.raw_data):
            compare_to = ORIGINAL_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

    def test_modified_original_pages_and_snippets_have_retained_their_modified_body_values(
        self,
    ):
        """
        Test that the objects created in `0002_create_test_objects` and had their `body` value
        later modified in `0004_modify_body_values` have retained that updated body value after:

        - Updating their `title` value in `0007_modify_title_values` and resaving
        """
        test_page = self.page_2
        test_snippet = self.snippet_2

        self.assertEqual(test_page.title, "Modified Test Page Deux")
        self.assertEqual(len(test_page.body.raw_data), 3)
        for i, block in enumerate(test_page.body.raw_data):
            compare_to = MODIFIED_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

        self.assertEqual(test_snippet.title, "Modified Test Snippet Deux")
        self.assertEqual(len(test_snippet.body.raw_data), 3)
        for i, block in enumerate(test_snippet.body.raw_data):
            compare_to = MODIFIED_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

    def test_newer_pages_and_snippets_have_retained_their_original_body_values(self):
        """
        Test that the objects created in `0005_create_more_test_objects` and DID NOT have their body
        value updated in later migrations have retained their original values after:

        - Updating their `title` value in `0007_modify_title_values` and resaving
        - Updating their `title` value again in `0008_modify_title_values_with_bulk_update` via a bulk update
        """
        test_page = self.page_3
        test_snippet = self.snippet_3

        self.assertEqual(test_page.title, "Bulk Modified Test Page Tres")
        self.assertEqual(len(test_page.body.raw_data), 3)
        for i, block in enumerate(test_page.body.raw_data):
            compare_to = ORIGINAL_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

        self.assertEqual(test_snippet.title, "Bulk Modified Test Snippet Tres")
        for i, block in enumerate(test_snippet.body.raw_data):
            compare_to = ORIGINAL_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

    def test_modified_newer_pages_and_snippets_have_retained_their_modified_body_values(
        self,
    ):
        """
        Tests that the objects created in `0005_create_more_test_objects` and had their `body` value
        later modified in `0006_modify_body_values_with_bulk_update` have retained that updated `body`
        value after:

        - Updating their `title` value in `0007_modify_title_values` and resaving
        - Updating their `title` value again in `0008_modify_title_values_with_bulk_update` via a bulk update
        """
        test_page = self.page_4
        test_snippet = self.snippet_4

        self.assertEqual(test_page.title, "Bulk Modified Test Page Cuatro")
        self.assertEqual(len(test_page.body.raw_data), 3)
        for i, block in enumerate(test_page.body.raw_data):
            compare_to = MODIFIED_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])

        self.assertEqual(test_snippet.title, "Bulk Modified Test Snippet Cuatro")
        self.assertEqual(len(test_snippet.body.raw_data), 3)
        for i, block in enumerate(test_snippet.body.raw_data):
            compare_to = MODIFIED_BODY_VALUE[i]
            self.assertEqual(block["type"], compare_to["type"])
            self.assertEqual(block["value"], compare_to["value"])
