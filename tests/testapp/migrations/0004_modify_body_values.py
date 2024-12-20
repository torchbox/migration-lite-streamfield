from typing import Any, Sequence

from django.db import migrations

from tests.testapp.constants import (
    COMPLEX_MODIFIED_BODY_VALUE,
    COMPLEX_ORIGINAL_BODY_VALUE,
    SIMPLE_MODIFIED_BODY_VALUE,
    SIMPLE_ORIGINAL_BODY_VALUE,
)


"""
This second data migration modifies the `body` values of some of the
objects created in the first:

-  <TestPage title="Test Page Deux">
-  <TestSnippet title="Test Snippet Deux">

This allows us to confirm that field values can be changed successfully
in a migration once `mlstreamfield.fields.StreamField` is being used, and
the changes are retained as expected..

A second thing we are confirming here is that objects retain their values
after swapping `wagtail.fields.StreamField` for `mlstreamfield.fields.StreamField`
We're leaving "Test Page" and "Test Snippet" alone, so that we can check that
their original values are retained after all migrations have run.
"""


def set_body_values(
    apps,
    schema_editor,
    simple_value: Sequence[tuple[str, Any]],
    complex_value: Sequence[dict[str, Any]],
):
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    # Modify the second TestPage, but leave the first alone
    # Uses `simple_value` to show that the new field handles the simple 'list of tuples' format correctly
    page = TestPage.objects.last()
    page.body = simple_value
    page.save()

    # Modify the second TestSnippet, but leave the first alone
    # Uses `complex_value` to show that the new field handles the more complicated 'list of dicts' format correctly
    snippet = TestSnippet.objects.last()
    snippet.body = complex_value
    snippet.save()


def migrate_forwards(apps, schema_editor):
    set_body_values(
        apps, schema_editor, SIMPLE_MODIFIED_BODY_VALUE, COMPLEX_MODIFIED_BODY_VALUE
    )


def migrate_backwards(apps, schema_editor):
    set_body_values(
        apps, schema_editor, SIMPLE_ORIGINAL_BODY_VALUE, COMPLEX_ORIGINAL_BODY_VALUE
    )


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0003_swap_native_streamfield_for_mlstreamfield"),
    ]

    operations = [
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
