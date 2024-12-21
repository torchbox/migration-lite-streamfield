# Migration-Lite StreamField

A lightweight StreamField implementation for Wagtail that helps manage database migrations more effectively.

## Overview

Migration-Lite StreamField is a Django field that extends Wagtail's StreamField functionality, focusing on making database migrations more manageable. It preserves raw field data during migrations, allowing for safer schema changes and content updates.

## Features

- Drop-in replacement for Wagtail's StreamField
- Preserves raw data during migrations
- Handles both JSON string and list formats
- Compatible with Wagtail 6.2 and 6.3
- Full test coverage

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

## Migration Support

During migrations, the field:
- Preserves raw field data
- Handles both JSON strings and list formats
- Safely stores invalid JSON as raw text for error handling
- Maintains compatibility with Wagtail's migration system

## Requirements

- Python 3.8+
- Django 4.2+
- Wagtail 6.2+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed and maintained by [Torchbox](https://torchbox.com/).
```

</rewritten_file>
```

</rewritten_file>
