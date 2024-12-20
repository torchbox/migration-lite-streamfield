from django.db import migrations

from tests.testapp.constants import (
    COMPLEX_ORIGINAL_BODY_VALUE,
    SIMPLE_ORIGINAL_BODY_VALUE,
)


"""
This third data migration creates some additional objects:

-  <TestPage title="Test Page Tres">
-  <TestPage title="Test Page Cuatro">
-  <TestSnippet title="Test Snippet Tres">
-  <TestSnippet title="Test Snippet Cuatro">

This allows us to confirm that objects can be created successfully whilst
`mlstreamfield.fields.StreamField` is being used, and that the values assigned
to the field are retained as expected.

(Bonus points for recognising that we've shifted from French to Spanish!)
"""


def migrate_forwards(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Page = apps.get_model("wagtailcore", "Page")
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    content_type = ContentType.objects.get(app_label="testapp", model="testpage")

    # Add pages
    TestPage.objects.create(
        title="Test Page Tres",
        draft_title="Test Page Tres",
        slug="test-page-3",
        content_type=content_type,
        body=SIMPLE_ORIGINAL_BODY_VALUE,
        depth=3,
        locale_id=1,
        path="000100010003",
        numchild=0,
        url_path="/home/test-page-3/",
        translation_key="9f121f31-bc8b-4591-9955-9fbe7bbff256",
    )
    TestPage.objects.create(
        title="Test Page Cuatro",
        draft_title="Test Page Cuatro",
        slug="test-page-4",
        content_type=content_type,
        body=COMPLEX_ORIGINAL_BODY_VALUE,
        depth=3,
        locale_id=1,
        path="000100010004",
        numchild=0,
        url_path="/home/test-page-4/",
        translation_key="5e6e7b4e-3e01-4533-8a11-51640fa5e191",
    )
    Page.objects.filter(depth=2).update(numchild=4)

    # Add snippetS
    TestSnippet.objects.create(
        title="Test Snippet Tres", body=SIMPLE_ORIGINAL_BODY_VALUE
    )
    TestSnippet.objects.create(
        title="Test Snippet Cuatro", body=COMPLEX_ORIGINAL_BODY_VALUE
    )


def migrate_backwards(apps, schema_editor):
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")
    TestPage.objects.last().delete()
    TestSnippet.objects.last().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0004_modify_body_values"),
    ]

    operations = [
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
