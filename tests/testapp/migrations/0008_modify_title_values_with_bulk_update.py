from django.db import migrations


"""
This sixth and final data migration uses bulk_update() to modify the `title` values of the following
objects:

-   <TestPage title="Modified Test Page Tres">
-   <TestPage title="Modified Test Page Cuatro">
-   <Snippet title="Modified Test Snippet Tres">
-   <Snippet title="Modified Test Snippet Cuatro">

This provides additional assurances that updates via bulk_update() also don't
cause any mysterious loss of `mlstreamfield.fields.StreamField` values in the
process of reading the values and writing them back to the database when they
haven't been interacted with.
"""


def update_title_values(apps, schema_editor, *, forwards=True):
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    # Modify test pages
    to_update = []
    for page in TestPage.objects.all()[2:]:
        if forwards:
            page.title = f"Bulk {page.title}"
        else:
            page.title = page.title.removeprefix("Bulk ")
        to_update.append(page)
    # NOTE: The inclusion of 'body' here is intentional
    TestPage.objects.bulk_update(to_update, ["title", "body"])

    # Modify test snippets
    to_update = []
    for snippet in TestSnippet.objects.all()[2:]:
        if forwards:
            snippet.title = f"Bulk {snippet.title}"
        else:
            snippet.title = snippet.title.removeprefix("Bulk ")
        to_update.append(snippet)
    # NOTE: The inclusion of 'body' here is intentional
    TestSnippet.objects.bulk_update(to_update, ["title", "body"])


def migrate_forwards(apps, schema_editor):
    update_title_values(apps, schema_editor, forwards=True)


def migrate_backwards(apps, schema_editor):
    update_title_values(apps, schema_editor, forwards=False)


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0007_modify_title_values"),
    ]

    operations = [
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
