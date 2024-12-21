from django.test import TestCase
from wagtail.blocks import StreamBlock, StreamValue, TextBlock

from mlstreamfield.fields import StreamField


class TestStreamField(TestCase):
    def setUp(self):
        # Set up basic block types and field for use in tests
        self.block_types = [("text", TextBlock())]
        self.field = StreamField(self.block_types)

    def test_init_with_empty_args(self):
        # Verify StreamField can be initialised without any arguments
        # Should create an empty block dictionary
        field = StreamField()
        self.assertEqual(field.stream_block.child_blocks, {})

    def test_init_with_none_as_first_arg(self):
        # Verify StreamField handles None as first argument gracefully
        # Should create an empty block dictionary
        field = StreamField(None)
        self.assertEqual(field.stream_block.child_blocks, {})

    def test_init_with_block_types_as_first_arg(self):
        # Verify StreamField correctly initialises when block types are passed as first argument
        # Should create a StreamBlock instance
        field = StreamField(self.block_types)
        self.assertIsInstance(field.stream_block, StreamBlock)

    def test_init_with_block_types_as_kwarg(self):
        # Verify StreamField correctly initialises when block types are passed as keyword argument
        # Should create a StreamBlock instance
        field = StreamField(block_types=self.block_types)
        self.assertIsInstance(field.stream_block, StreamBlock)

    def test_deconstruct_with_args(self):
        # Test that deconstruct() properly handles positional arguments
        # Should not include block_types or verbose_name in kwargs
        field = StreamField(self.block_types, verbose_name="Test")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(args, [])
        self.assertNotIn("block_types", kwargs)
        self.assertNotIn("verbose_name", kwargs)

    def test_deconstruct_with_kwargs(self):
        # Test that deconstruct() properly handles keyword arguments
        # Should not include block_types or verbose_name in kwargs
        field = StreamField(block_types=self.block_types, verbose_name="Test")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(args, [])
        self.assertNotIn("block_types", kwargs)
        self.assertNotIn("verbose_name", kwargs)

    def test_to_python_with_empty_value(self):
        # Verify that None is converted to an empty StreamValue
        result = self.field.to_python(None)
        self.assertIsInstance(result, StreamValue)

    def test_to_python_with_list_value_during_migration(self):
        # Test handling of list data during database migrations
        # Should preserve raw data for later processing
        field = StreamField()  # Empty field to simulate migration
        value = [{"type": "text", "value": "test"}]
        result = field.to_python(value)
        self.assertEqual(result._raw_data, value)

    def test_to_python_with_json_string_during_migration(self):
        # Test handling of JSON string data during database migrations
        # Should parse JSON and store as raw data
        field = StreamField()  # Empty field to simulate migration
        value = '[{"type": "text", "value": "test"}]'
        result = field.to_python(value)
        self.assertEqual(result._raw_data, [{"type": "text", "value": "test"}])

    def test_to_python_with_invalid_json_string_during_migration(self):
        # Test handling of invalid JSON during database migrations
        # Should store invalid JSON as raw text for error handling
        field = StreamField()  # Empty field to simulate migration
        value = "invalid json"
        result = field.to_python(value)
        self.assertEqual(result.raw_text, value)

    def test_get_prep_value_with_raw_text_during_migration(self):
        # Test preparation of raw text data for database storage during migration
        # Should preserve raw text as-is
        field = StreamField()  # Empty field to simulate migration
        stream_value = StreamValue(StreamBlock([]), stream_data=[])
        stream_value.raw_text = "test value"
        result = field.get_prep_value(stream_value)
        self.assertEqual(result, "test value")

    def test_get_prep_value_with_raw_data_during_migration(self):
        # Test preparation of raw data for database storage during migration
        # Should convert raw data back to JSON string
        field = StreamField()  # Empty field to simulate migration
        stream_value = StreamValue(StreamBlock([]), stream_data=[])
        stream_value._raw_data = [{"type": "text", "value": "test"}]
        result = field.get_prep_value(stream_value)
        self.assertEqual(result, '[{"type": "text", "value": "test"}]')

    def test_get_prep_value_with_normal_streamvalue(self):
        # Test normal preparation of StreamValue for database storage
        # Should convert StreamValue to JSON string or list format depending on Wagtail version
        stream_value = self.field.to_python([{"type": "text", "value": "test"}])
        result = self.field.get_prep_value(stream_value)
        self.assertTrue(
            isinstance(result, (str, list)),
            f"Expected result to be str or list, got {type(result)}",
        )

    def test_init_with_streamblock_as_first_arg(self):
        # Verify StreamField correctly initialises when a StreamBlock instance is passed as first argument
        # Should use the provided StreamBlock instance directly
        stream_block = StreamBlock(self.block_types)
        field = StreamField(stream_block)
        self.assertEqual(field.stream_block, stream_block)

    def test_to_python_with_streamvalue(self):
        # Verify that an existing StreamValue instance is returned unchanged
        stream_value = StreamValue(self.field.stream_block, [])
        result = self.field.to_python(stream_value)
        self.assertEqual(result, stream_value)

    def test_get_prep_value_with_none(self):
        # Test preparation of None value for database storage
        # Should return None
        result = self.field.get_prep_value(None)
        self.assertIsNone(result)
