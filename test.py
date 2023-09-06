import unittest
from utils import generate_regex


class TestGenerateRules(unittest.TestCase):

    def setUp(self):
        generate_regex_data = [
            'api.alt-epg-dev.xxx.com',
            'kibana.mon.xxx.com',
            'yi2mnglyyxty.sub.yyy.com',
            'foo.sub.xyz.com'
        ]

        self.test_data = (
            ('api.alt-epg-dev.xxx.com', True),
            ('kibana.mon.xxx.com', True),
            ('yi2mnglyyxty.sub.yyy.com', True),
            ('foo.sub.xyz.com', True),
            ('', False),
            ('fo_o.sub.xyz.com', False),
            ('random.xyz.com', False),
        )
        self.regexp_ = generate_regex(generate_regex_data)

    def test_generate_regex(self):
        for domain, expected_status in self.test_data:
            with self.subTest(domain=domain, expected_status=expected_status):
                self.assertRegex(
                    domain, self.regexp_
                    if expected_status else f'^(?!{self.regexp_})')


if __name__ == '__main__':
    unittest.main()
