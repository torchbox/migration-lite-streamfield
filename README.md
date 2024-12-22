# migration-lite-streamfield

(Or `mlstreamfield` for short)

All the goodness of Wagtail's Streamfield, but without the migration headaches.

## What problem does `mlstreamfield` solve?

Wagtail's `StreamField` is flexible and powerful, but that flexibility often comes at a price in client projects.

The native implementation has included information about the blocks in a StreamField in migrations pretty much from the beignning. Personally speaking, it's a decision I've come to respect. It makes sense from a 'framework' perspective, because you never truly know how your code is being used, or what developers might need to do within a data migration. However, there's no denying it adds a degree of overhead to most client projects:

- Each time you add a new block, you must generate a migration for any model you decide to add it to.
- Each time you change the definition of an existing block, you must generate a migration for any model that uses it.
- Each time you decide to rename a block type or move it to a more suitable place in the codebase, you must generate a migration for any model that uses it.
- Each time you change the label and help text for the field to improve the experience for editors, you must generate a migration to reflect those changes.

_Notice the pattern?_

You might not have realised, but all of these additional migrations slow a project down. Django evaluates a project's migration history regularly when running a number of key commands, including `makemigrations`, `migrate`, `runserver`, `test`, and whenever you run a custom management command. The more migrations you have, and the larger those migrations are, the longer that evaluation takes.

Whilst Wagtail has done some amazing work in recent versions to reduce the size of StreamFieldmigrations, the sheer number of migrations generated as part of the day-to-day development on a busy project can still be problematic. In addition to the aformentioned slow-down, there's also:

- The additional noise in code contributions
- The higher likelihood of merge conflicts when multiple developers are working on common blocks at the same time.
- The cumulative overhead of having to apply and reverse migrations when switching between multiple feature branches your are working on (or reviewing).

Let's also not forget those regretable 'environment-specific' merge migrations that are sometimes required to bring environments back to life when features are merged to an environment-specific branch in a different order to trunk (eek!).

## How is `mlstreamfield` different?

It's strength comes simply from _not including block definitions (or references to them) in migrations_ - pure and simple. It extends Wagtail's StreamField, so you get the same great editor experience, power and flexibility. Things just work a little differently when it comes to migrations.

## Frequently Asked Questions

### Cut to the chase! What will I lose by switching to `mlstreamfield`?

Direct - I like it! Let me sum it up for you very clearly:

#### 1.  You'll only be able to interact with raw data values in data migrations (accessed via `fieldname.raw_data`).

If, like me, you've written a lot of data migrations over the years, this is probably all you're interested in anyway! However, for those worried about the implications, the basic rundown is:

- `RichTextBlock` values will just be strings.
- `DateBlock`, `DateTimeBlock` and `TimeBlock` values will just be strings in ISO format.
- `ChooserBlock` values will just be strings (the ID of the chosen item).
- `StructBlock` values will just be dicts of raw values.
- `ListBlock` and `StreamBlock` values will just be lists of dicts representing each item.

The values are still accessible, and modifiable: You might just need to convert the odd ID into an object yourself, or use `datetime.date.fromisoformat()` to convert a date string into a date here and there.

Changes made directly to `fieldname.raw_data` are reflected when the object is saved, so it's honestly the easiest way to interact with field values in migrations anyway (regardless of whether you want to use this package or not).

This is barely worth mentioning, but lack of access to block definitions also means you won't be able to 'render' `StreamField` values in a data migration. However, that would be a very strange thing to need in data migration anyway.

#### 2. Some of the special 'migration operations' for StreamFields might not work as expectedafter switching

Some of the built-in migration operations mentioned in [the Wagtail documentation](https://docs.wagtail.org/en/stable/advanced_topics/streamfield_migrations.html#why-are-data-migrations-necessary), or in packages like [wagtail-streamfield-migration-toolkit](https://github.com/wagtail/wagtail-streamfield-migration-toolkit) might not work as expected.

Honestly though, once you get a handle on the few common data structures encountered in raw `StreamField` values, achieving something similar with `RunPython` is usually quite straightforward. Plus, understanding the raw data format of `StreamField` values is a skill that will help you with other aspects of development.

#### 3. It's an additional project dependency to manage

Although the entirety of the package is a single Python class in a single module, it's still an additional thing to consider when keeping your Wagtail version up-to-date.

That said, because of the tiny scope of the package, and the stability of the `StreamField` API (remember, field classes are regularly referenced by historic migrations,s), it's unlikely that a lot of changes will be needed to keep things compatible with the latest Wagtail version.

At Torchbox, we've been using a version of this field in client projects for a few years, and only had to change anything for the Wagtail 6.2 release (most ).

4.  **That's it!**

### Q: Will I lose existing field data when switching to `mlstreamfield`?

**Absolutely not**. `mlstreamfield.StreamField` is a drop-in replacement for the native version, and changes nothing about how data is stored internally. Any existing data is preserved. If you need proof, take a look through the [testapp migrations](https://github.com/torchbox/migration-lite-streamfield/tree/main/tests/testapp/migrations) for this package (It's thoroughly tested).

### Q: Will switching to `mlstreamfield` break my migration history?

**No**. You'll need to generate new migrations to account for any fields you've switched over, because you're changing the field type. But, adopting Migration-Lite StreamField doesn't touch historic migrations in any way, or change how migrations in general work.

Historic migrations will continue to use Wagtail's native `StreamField` for all operations up until the migration that changes the field type to `mlstreamfield.StreamField`.

### Q: Will switching to `mlstreamfield` prevent me from writing data migrations when a client changes their mind about something?

**No**. You can still access and modify field data in data migrations. You just need to use `fieldname.raw_data` to access it. If you want to see some examples, take a look at the [testapp migrations](https://github.com/torchbox/migration-lite-streamfield/tree/main/tests/testapp/migrations) for this package.

### Q: Will switching to `mlstreamfield` shrink my existing migration files?

**No**. Your historic migrations are completely unaffected. Switching to `mlstreamfield` will prevent things getting any worse, but it can't solve historic migrationproblems. That can only really be acheived through [migration squashing](https://medium.com/@SmoQ/django-squashing-database-migrations-4906e4beeb66).

The _earlier_ in a project you adopt `mlstreamfield`, the more you'll profit.

### Q: Can I use `mlstreamfield` in my Wagtail add-on package?

Technically, _yes_. But, the recommendation is to avoid it.

An add-on package doesn't usually suffer from the same issues as a client project (rapid development with multiple developers, experimental POCs, direction changes etc), so you're less likely to benefit from it.

Also, users of your package could feel blindsided by the change in migration behaviour if they've haven't adopted `mlstreamfield` themselves, and aren't familiar with the nuances.

### Q: Will I lose field data if I write a bad data migration?

**Yes**. But, that's true whether you decied to use `mlstreamfield` or not. Data migrations are notoriously tricky territory and require careful testing locally before committing. Nothing about `mlstreamfield` changes that.

## Requirements

- Python 3.11+
- Django 4.2+
- Wagtail 5.2+

## Installation

Install using pip:

```
pip install migration-lite-streamfield
```

Or add to your project's requirements:

```
migration-lite-streamfield==1.0.0
```

## Usage

Replace your existing StreamField imports with:

```python
from mlstreamfield.fields import StreamField
```

Then use it exactly as you would use Wagtail's StreamField:

```python
from wagtail.blocks import CharBlock, RichTextBlock
from mlstreamfield.fields import StreamField

class BlogPage(Page):
    body = StreamField([
        ('heading', CharBlock()),
        ('paragraph', RichTextBlock()),
    ], use_json_field=True)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed and maintained by [Torchbox](https://torchbox.com/).
```
