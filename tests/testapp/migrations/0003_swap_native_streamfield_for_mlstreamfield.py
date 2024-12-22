from django.db import migrations

import mlstreamfield.fields


"""
That's right! We're officially swapping the native `wagtail.fields.StreamField`
for `mlstreamfield.fields.StreamField`. "What utter madness!" I hear you say.
"""


class Migration(migrations.Migration):
    dependencies = [
        ("testapp", "0002_create_test_objects"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testpage",
            name="body",
            field=mlstreamfield.fields.StreamField(blank=True),
        ),
        migrations.AlterField(
            model_name="testsnippet",
            name="body",
            field=mlstreamfield.fields.StreamField(blank=True),
        ),
    ]
