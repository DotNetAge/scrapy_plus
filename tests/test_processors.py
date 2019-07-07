# coding:utf-8
import unittest
from douban.processors import Number, Text, Date, Price


class ProcessorTestCase(unittest.TestCase):

    def test_number_processor(self):
        tests_text = "共93.2人"
        expected = 93.2
        processor = Number()

        actual = processor([tests_text])
        self.assertEqual(actual[0], expected)

    def test_text_processor(self):
        tests_text = "<div>This is a text with some <b>html</b> tags</div>"
        expected_text = "This is a text with some html tags"
        processor = Text()

        actual = processor([tests_text])
        self.assertEqual(actual[0], expected_text)

    def test_price_processor(self):
        tests_text = "￥24.2 元"
        expected = 24.2
        processor = Price()

        actual = processor([tests_text])
        self.assertEqual(actual[0], expected)

    def test_date_processor(self):
        tests_text = "2015年2月3日"
        expected_text = '2015-02-03T00:00:00'
        processor = Date()

        actual = processor([tests_text])
        self.assertEqual(actual[0].strftime('%Y-%m-%dT%H:%M:%S'), expected_text)
