# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json

from django.urls import reverse, NoReverseMatch
from django.test import TestCase

from . import Emoji as EmojiInstance
from .models import Emoji, UNICODE_WIDE

# Anyone know how to mock out so os.listdir only lists what I want
# instead of hitting the file system?
TOTAL_EMOJIS = 888
TOTAL_EMOJIS_UNICODE = 838


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
            '<img src="/static/emoji/img/%2B1.png" alt="+1" '
            'title="+1" class="emoji">'
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


class EmojiJSONListViewTest(TestCase):
    def test_should_return_json_list(self):
        res = self.client.get(reverse('emoji:list.json'))
        self.assertEqual(res.status_code, 200)

        items = json.loads(res.content.decode('utf8'))
        self.assertEqual(len(items), TOTAL_EMOJIS)
        self.assertEqual(items['+1'], '/static/emoji/img/%2B1.png')


class EmojiTemplateTagTest(TestCase):
    def test_emoji_replace_tag(self):
        try:
            res = self.client.get(reverse('emoji_test_list'), {'limit': 1})
        except NoReverseMatch:
            return

        self.assertEqual(res.status_code, 200)
        self.assertIn('<img src="/static/emoji/img/%2B1.png" '
                      'alt="+1" title="+1" class="emoji">', str(res.content))

    def test_emoji_replace_unicode_tag(self):
        try:
            res = self.client.get(reverse('emoji_replace_unicode_test'))
        except NoReverseMatch:
            return

        self.assertEqual(res.status_code, 200)
        self.assertIn(('<img src="/static/emoji/img/kiss.png" ' +
                       'alt="💋" title="kiss" ' +
                       'class="emoji">'), res.content.decode('utf-8'))

    def test_emoji_replace_html_entities(self):
        try:
            res = self.client.get(reverse('emoji_replace_html_entities_test'))
        except NoReverseMatch:
            return

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content.decode('utf-8'),
                         '\n\U0001f48b\n\U0001f48b\n')

    def test_emoji_include_script(self):
        try:
            res = self.client.get(reverse('emoji_include_test'))
        except NoReverseMatch:
            return

        self.assertEqual(res.status_code, 200)
        body = res.content
        self.assertTrue('/static/emoji/js/emoji.js' in str(body), 'emoji.js')

    def test_emoji_load_tag(self):
        try:
            res = self.client.get(reverse('emoji_load_test'))
        except NoReverseMatch:
            pass

        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            "Emoji.setDataUrl('/all.json').load();" in str(res.content)
        )

    def test_xss_replace_html_entities(self):
        try:
            res = self.client.get(reverse('xss_fix'))
        except NoReverseMatch:
            pass

        self.assertEqual(res.status_code, 200)
        correct_string = ('&lt;em&gt;\U0001f48b&lt;/em&gt;\n'
                          '&lt;em&gt;\U0001f48b&lt;/em&gt;')
        self.assertIn(correct_string, res.content.decode('utf-8'))

    def test_xss_replace_unicode(self):
        try:
            res = self.client.get(reverse('xss_fix'))
        except NoReverseMatch:
            pass

        self.assertEqual(res.status_code, 200)
        correct_string = ('&lt;em&gt;<img src="/static/emoji/img/shit.png" '
                          'alt="💩" title="shit" class="emoji">&lt;em&gt;')
        self.assertIn(correct_string, res.content.decode('utf-8'))

    def test_xss_replace_emoji(self):
        try:
            res = self.client.get(reverse('xss_fix'))
        except NoReverseMatch:
            pass

        self.assertEqual(res.status_code, 200)
        correct_string = ('&lt;em&gt;<img src="/static/emoji/img/dog.png" '
                          'alt="dog" title="dog" class="emoji">&lt;/em&gt;')
        self.assertIn(correct_string, res.content.decode('utf-8'))


class UnicodeTestBase(TestCase):
    # :kiss: filename 1f48b.png, chosen 'cause it prints properly in terminal
    UNICODE_KISS = '\U0001f48b'
    UNICODE_KISS_CHARACTER = '💋'
    UNICODE_KISS_SURROGATE_PAIR = '\ud83d\udc8b'


class EmojiUnicodeTest(UnicodeTestBase):
    def test_should_also_store_the_unicode_of_an_emoji(self):
        self.assertEqual(len(Emoji._unicode_characters), TOTAL_EMOJIS_UNICODE)

    def test_should_be_able_to_look_up_unicode(self):
        self.assertEqual(Emoji.name_for(self.UNICODE_KISS), 'kiss')
        self.assertEqual(Emoji.name_for(self.UNICODE_KISS_CHARACTER), 'kiss')

    def test_replace_unicode_in_string_with_images(self):
        self.assertIn(
            'kiss.png',
            Emoji.replace_unicode('I send a {0}!'.format(self.UNICODE_KISS)),
        )

    def test_emojis_that_were_showing_wrong(self):
        # These emojis were showing other images than the ones intended.
        emoji = '🍆'
        self.assertEqual(Emoji.name_for(emoji), 'eggplant')

        emoji = '😘'
        self.assertEqual(Emoji.name_for(emoji), 'kissing_heart')

    def test_remove_unicode_control_from_name_for(self):
        # fe0f is a control character that modifies the character
        # before, but we already do that modification so it's just
        # unecessary.
        emoji = '✌️'
        self.assertEqual(Emoji.name_for(emoji), 'v')

    def test_remove_unicode_control_from_replace_unicode(self):
        emoji = '✌️'
        self.assertEqual(
            Emoji.replace_unicode(emoji),
            '<img src="/static/emoji/img/v.png" alt="✌" '
            'title="v" class="emoji">'
        )

    def test_can_convert_unicode_surrogate_pair_emoji(self):
        """When in narrow mode the output characters might be a surrogate
        pair, but that matches in string comparison with the wide
        character.

        """
        # Tests that only matter when running narrow, @skipIf not
        # available in 2.6.
        if UNICODE_WIDE:
            return

        res = Emoji.replace_unicode(self.UNICODE_KISS_SURROGATE_PAIR)
        self.assertIn('\ud83d\udc8b', res)
        self.assertIn('\U0001f48b', res)


class EmojiHtmlEntitiesTest(UnicodeTestBase):
    INTEGER_KISS = '&#128139;'
    HEX_KISS = '&#x0001f48b;'
    HEX_KISS_SHORT = '&#x1f48b;'

    def test_should_replace_integer_encoded_unicode(self):
        self.assertEqual(
            Emoji.replace_html_entities(self.INTEGER_KISS),
            self.UNICODE_KISS
        )

    def test_should_replace_hex_encoded_unicode(self):
        self.assertEqual(
            Emoji.replace_html_entities(self.HEX_KISS),
            self.UNICODE_KISS
        )

    def test_should_replace_short_hex_encoded_unicode(self):
        self.assertEqual(
            Emoji.replace_html_entities(self.HEX_KISS_SHORT),
            self.UNICODE_KISS
        )
