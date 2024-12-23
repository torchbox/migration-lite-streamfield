
from django.test import TestCase
from testapp.constants import DATE_BLOCK_ID, INTEGER_BLOCK_ID, TEXT_BLOCK_ID
from testapp.models import TestPage, TestSnippet


class TestMigrationOutcomes(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i, page in enumerate(TestPage.objects.all().order_by("id"), start=1):
            setattr(cls, f"page_{i}", page)
        for i, snippet in enumerate(TestSnippet.objects.all().order_by("id"), start=1):
            setattr(cls, f"snippet_{i}", snippet)

    def assertHasOriginalBodyContent(self, body_value):
        data = body_value.raw_data
        self.assertEqual(len(data), 3)
        self.assertDictEqual(
            data[0], {"type": "text", "value": "Hello World!", "id": TEXT_BLOCK_ID}
        )
        self.assertDictEqual(
            data[1], {"type": "integer", "value": "123", "id": INTEGER_BLOCK_ID}
        )
        self.assertDictEqual(
            data[2],
            {"type": "date", "value": "2024-12-25", "id": DATE_BLOCK_ID},
        )
        rendered_body = str(body_value)
        self.assertInHTML('<div class="block-text">Hello World!</div>', rendered_body)
        self.assertInHTML('<div class="block-integer">123</div>', rendered_body)
        self.assertInHTML('<div class="block-date">2024-12-25</div>', rendered_body)

    def assertHasModifiedBodyContent(self, body_value):
        data = body_value.raw_data
        self.assertEqual(len(data), 3)
        self.assertDictEqual(
            data[0], {"type": "text", "value": "Goodbye Galaxy!", "id": TEXT_BLOCK_ID}
        )
        self.assertDictEqual(
            data[1], {"type": "integer", "value": "321", "id": INTEGER_BLOCK_ID}
        )
        self.assertDictEqual(
            data[2],
            {"type": "date", "value": "3024-12-25", "id": DATE_BLOCK_ID},
        )
        rendered_body = str(body_value)
        self.assertInHTML(
            '<div class="block-text">Goodbye Galaxy!</div>', rendered_body
        )
        self.assertInHTML('<div class="block-integer">321</div>', rendered_body)
        self.assertInHTML('<div class="block-date">3024-12-25</div>', rendered_body)

    def test_original_pages_and_snippets_have_retained_their_original_body_values(self):
        """
        Test the objects created in `0002_create_test_objects` and DID NOT have their `body` value
        updated in later migrations have retained their original values after:

        - Swapping the native StreamField for a custom one in `0003_swap_native_streamfield_for_mlstreamfield`
        - Updating their title in `0007_modify_title_values` and resaving
        - Updating their title in `0008_modify_title_values_with_bulk_update` via a bulk update
        """
        for obj, expected_title in [
            (self.page_1, "Modified Test Page"),
            (self.snippet_1, "Modified Test Snippet"),
        ]:
            with self.subTest(repr(obj)):
                self.assertEqual(obj.title, expected_title)
                self.assertHasOriginalBodyContent(obj.body)

    def test_modified_original_pages_and_snippets_have_retained_their_modified_body_values(
        self,
    ):
        """
        Test that the objects created in `0002_create_test_objects` and had their `body` value
        later modified in `0004_modify_body_values` have retained that updated body value after:

        - Updating their `title` value in `0007_modify_title_values` and resaving
        """
        for obj, expected_title in [
            (self.page_2, "Modified Test Page Deux"),
            (self.snippet_2, "Modified Test Snippet Deux"),
        ]:
            with self.subTest(repr(obj)):
                self.assertEqual(obj.title, expected_title)
                self.assertHasModifiedBodyContent(obj.body)

    def test_newer_pages_and_snippets_have_retained_their_original_body_values(self):
        """
        Test that the objects created in `0005_create_more_test_objects` and DID NOT have their body
        value updated in later migrations have retained their original values after:

        - Updating their `title` value in `0007_modify_title_values` and resaving
        - Updating their `title` value again in `0008_modify_title_values_with_bulk_update` via a bulk update
        """
        for obj, expected_title in [
            (self.page_3, "Bulk Modified Test Page Tres"),
            (self.snippet_3, "Bulk Modified Test Snippet Tres"),
        ]:
            with self.subTest(repr(obj)):
                self.assertEqual(obj.title, expected_title)
                self.assertHasOriginalBodyContent(obj.body)

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
        for obj, expected_title in [
            (self.page_4, "Bulk Modified Test Page Cuatro"),
            (self.snippet_4, "Bulk Modified Test Snippet Cuatro"),
        ]:
            with self.subTest(repr(obj)):
                self.assertEqual(obj.title, expected_title)
                self.assertHasModifiedBodyContent(obj.body)
