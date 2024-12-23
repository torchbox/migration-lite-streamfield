from typing import Any, Sequence

from django.db import migrations

from tests.testapp.constants import MODIFIED_BODY_VALUE, ORIGINAL_BODY_VALUE


"""
This fourth data migration uses bulk_update() to modify the `body` values of the
following objects created in the previous migration.

-  <TestPage title="Test Page Cuatro">
-  <TestSnippet title="Test Snippet Cuatro">

This allows us to confirm that field values can be changed successfully via bulk_update()
in a migration when `mlstreamfield.fields.StreamField` is being used, and the changes are
retained as expected.
"""


def set_body_values(
    apps,
    schema_editor,
    new_value: Sequence[dict[str, Any]],
):
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    # Modify "Test Page Cuatro"
    # Uses `simple_value` to show that the new field handles the simple 'list of tuples' format correctly
    page = TestPage.objects.last()
    page.body = new_value
    TestPage.objects.bulk_update([page], ["body"])

    # Modify "Test Snippet Cuatro"
    # Uses `complex_value` to show that the new field handles the more complicated 'list of dicts' format correctly
    snippet = TestSnippet.objects.last()
    snippet.body = new_value
    TestSnippet.objects.bulk_update([snippet], ["body"])


def migrate_forwards(apps, schema_editor):
    set_body_values(apps, schema_editor, MODIFIED_BODY_VALUE)


def migrate_backwards(apps, schema_editor):
    set_body_values(apps, schema_editor, ORIGINAL_BODY_VALUE)


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0005_create_more_test_objects"),
    ]

    operations = [
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
