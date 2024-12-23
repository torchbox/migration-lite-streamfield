from django.db import migrations

from tests.testapp.constants import ORIGINAL_BODY_VALUE


"""
This first data migration in the series creates the following objects,
all with the same `body` value:

-  <TestPage title="Test Page">
-  <TestPage title="Test Page Deux">
-  <TestSnippet title="Test Snippet">
-  <TestSnippet title="Test Snippet Deux">

The `body` field for both models is still using the native `StreamField` at
this point in time, so this alone isn't useful for testing. But, it's what
we do in the following migrations that is important.

(Bonus points for recognising that 'Deux' is French. I don't know the language
as well as I'd like to, but isn't 'Deux' just cool? It makes me think of
'Deus Ex Machina'!)

"""


def migrate_forwards(apps, schema_editor):
    ContentType = apps.get_model("contenttypes", "ContentType")
    Page = apps.get_model("wagtailcore", "Page")
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    content_type, _ = ContentType.objects.get_or_create(
        app_label="testapp", model="testpage"
    )

    # Add two test pages
    TestPage.objects.create(
        title="Test Page",
        draft_title="Test Page",
        slug="test-page",
        content_type=content_type,
        body=ORIGINAL_BODY_VALUE,
        depth=3,
        locale_id=1,
        path="000100010001",
        numchild=0,
        url_path="/home/test-page/",
        translation_key="72b25f92-0a15-4bc4-b0cf-9bf1eb976257",
    )
    TestPage.objects.create(
        title="Test Page Deux",
        draft_title="Test Page Deux",
        slug="test-page-2",
        content_type=content_type,
        body=ORIGINAL_BODY_VALUE,
        depth=3,
        locale_id=1,
        path="000100010002",
        numchild=0,
        url_path="/home/test-page-2/",
        translation_key="bc50f855-2939-4171-baa0-4dafa5b474cd",
    )
    Page.objects.filter(depth=2).update(numchild=2)

    # Add two test snippet
    TestSnippet.objects.create(title="Test Snippet", body=ORIGINAL_BODY_VALUE)
    TestSnippet.objects.create(title="Test Snippet Deux", body=ORIGINAL_BODY_VALUE)


def migrate_backwards(apps, schema_editor):
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    for page in TestPage.objects.all():
        page.delete()

    for snippet in TestSnippet.objects.all():
        snippet.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
