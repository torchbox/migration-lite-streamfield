from .utils import convert_simple_streamfield_value_to_dicts


SIMPLE_ORIGINAL_BODY_VALUE = [
    ("text", "Hello World"),
    ("integer", "123"),
    ("date", "2024-12-25"),
]

COMPLEX_ORIGINAL_BODY_VALUE = convert_simple_streamfield_value_to_dicts(
    SIMPLE_ORIGINAL_BODY_VALUE, add_ids=True
)


SIMPLE_MODIFIED_BODY_VALUE = [
    ("text", "Goodbye Galaxy!"),
    ("integer", "321"),
    ("date", "3024-12-25"),
]

COMPLEX_MODIFIED_BODY_VALUE = convert_simple_streamfield_value_to_dicts(
    SIMPLE_MODIFIED_BODY_VALUE
)
