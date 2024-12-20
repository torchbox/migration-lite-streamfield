from django.db import migrations


"""
This fifth data migration modifies the `title` values of all objects created
so far, saving each instance individually after the change.

This confirms that `mlstreamfield.fields.StreamField` values aren't mysteriously
lost for any reason when you modify unrelated field values and call the object's
save() method.

StreamFields do some surprisingly complicated things under-the-hood when retrieving
values and writing them back to the database, even when you don't interact with
the values in-between. So, we need assurance that nothing untoward happens during
that process.
"""


def update_title_values(apps, schema_editor, *, forwards=True):
    TestPage = apps.get_model("testapp", "TestPage")
    TestSnippet = apps.get_model("testapp", "TestSnippet")

    # Modify test pages
    for page in TestPage.objects.all():
        if forwards:
            page.title = f"Modified {page.title}"
        else:
            page.title = page.title.removeprefix("Modified ")
        page.save()

    # Modify test snippets
    for snippet in TestSnippet.objects.all():
        if forwards:
            snippet.title = f"Modified {snippet.title}"
        else:
            snippet.title = snippet.title.removeprefix("Modified ")
        snippet.save()


def migrate_forwards(apps, schema_editor):
    update_title_values(apps, schema_editor, forwards=True)


def migrate_backwards(apps, schema_editor):
    update_title_values(apps, schema_editor, forwards=False)


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0006_modify_body_values_with_bulk_update"),
    ]

    operations = [
        migrations.RunPython(migrate_forwards, migrate_backwards),
    ]
