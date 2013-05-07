import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from . import Emoji as EmojiInstance
from .models import Emoji

TOTAL_EMOJIS = 885


class EmojiTest(TestCase):
    def test_emoji_is_singleton(self):
        e = Emoji()
        e2 = Emoji()

        self.assertEqual(id(e), id(e2))

    def test_get_all_names(self):
        self.assertEqual(len(Emoji.names()), TOTAL_EMOJIS)

    def test_name_is_without_file_suffix(self):
        first_file = Emoji.names()[0]
        self.assertTrue('.png' not in first_file)

    def test_in_should_work_when_looking_for_emoji(self):
        emoji = Emoji()
        self.assertTrue('relaxed' in emoji)

    def test_replace_string_with_emojis(self):
        test_string = '''It's raining :cat:s and :dog:s.'''
        replaced_string = Emoji.replace(test_string)
        self.assertTrue('cat.png' in replaced_string)
        self.assertTrue('dog.png' in replaced_string)

    def test_replace_string_with_emojis_no_emoji_do_nothing(self):
        self.assertEqual(Emoji.replace('Hello.'), 'Hello.')

    def test_if_no_valid_emoji_return_unchanged(self):
        self.assertEqual(Emoji.replace(':ducklingdrinkingcoffee:'),
                         ':ducklingdrinkingcoffee:')

    def test_replace_string_should_use_staticfiles_app(self):
        self.assertEqual(
            Emoji.replace(':+1:'),
            '<img src="/static/emoji/img/%2B1.png" alt="+1" class="emoji">'
        )

    def test_emojiinstance_from_app(self):
        self.assertTrue('dog' in EmojiInstance)

    def test_convert_instance_to_dict_and_act_like_dict(self):
        e = Emoji()
        as_dict = dict(e)

        self.assertEqual(len(as_dict), TOTAL_EMOJIS)
        self.assertEqual(as_dict['+1'], '/static/emoji/img/%2B1.png')
        with self.assertRaises(KeyError):
            as_dict['nonexistant']


class EmojiListViewTest(TestCase):
    def test_should_return_json_list(self):
        res = self.client.get(reverse('emoji:list'))
        self.assertEqual(res.status_code, 200)

        items = json.loads(res.content)
        self.assertEqual(len(items), TOTAL_EMOJIS)
        self.assertEqual(items['+1'], '/static/emoji/img/%2B1.png')
