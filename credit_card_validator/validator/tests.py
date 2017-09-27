from credit_card_validator.validator.views import CreditCard
from django.test import TestCase


class CreditCardTestCase(TestCase):
    def setUp(self):
        self.valid_numbers = [
            '4253625879615786',
            '4424424424442444',
            '5122-2368-7954-3214'
        ]
        self.invalid_numbers = [
            '42536258796157867',
            '4424444424442444',
            '5122-2368-7954 - 3214',
            '44244x4424442444',
            '0525362587961578'
        ]
        self.credit_card = CreditCard()

    def test_verify_must_start_only_valid(self):
        for n in self.valid_numbers:
            c = CreditCard()
            c.current_number = n
            self.assertTrue(c.verify_must_start(), '{0}'.format(n))

    def test_verify_must_start_only_invalid(self):
        numbers = [
            '72536258796157867',
            '9122-2368-7954-3214',
            '32536258796157867'
        ]
        for n in numbers:
            c = CreditCard()
            c.current_number = n
            self.assertFalse(c.verify_must_start(), '{0}'.format(n))

    def test_verify_must_contains_16_digits_valid(self):
        for n in self.valid_numbers:
            c = CreditCard()
            c.current_number = n
            self.assertTrue(c.verify_must_contains_16_digits(), '{0}'.format(n))

    def test_verify_must_contains_16_digits_invalid(self):
        numbers = [
            '72536258796157867',
            '9122-2368-7954-32149',
            '32536258796157867'
        ]
        for n in numbers:
            c = CreditCard()
            c.current_number = n
            self.assertFalse(c.verify_must_contains_16_digits(), '{0}'.format(n))

    def test_verify_must_contains_only_0_9_valid(self):
        for n in self.valid_numbers:
            c = CreditCard()
            c.current_number = n
            self.assertTrue(c.verify_must_contains_only_0_9(), '{0}'.format(n))

    def test_verify_must_contains_only_0_9_invalid(self):
        numbers = [
            '72536258t796157867',
            '9122-2368-7954-32149p',
            '325362587961p57867'
        ]
        for n in numbers:
            c = CreditCard()
            c.current_number = n
            self.assertFalse(c.verify_must_contains_only_0_9(), '{0}'.format(n))

    def test_verify_group_separated_valid(self):
        valid_numbers = [
            '4253625879615786',
            '4424-4244-2444-2444',
            '5122-2368-7954-3214'
        ]
        for n in valid_numbers:
            c = CreditCard()
            c.current_number = n
            self.assertTrue(c.verify_group_separated(), '{0}'.format(n))

    def test_verify_group_separated_invalid(self):
        numbers = [
            '725-36258-7961-57867',
            '9122-2368-7954-32149p',
            '3-253625-87961p57-867',
            '3-253625-87961-p57-867'
        ]
        for n in numbers:
            c = CreditCard()
            c.current_number = n
            self.assertFalse(c.verify_group_separated(), '{0}'.format(n))

    def test_verify_contains_other_separator_valid(self):
        valid_numbers = [
            '4253-6258-7961-5786',
            '4424-4244-2444-2444',
            '5122-2368-7954-3214'
        ]
        for n in valid_numbers:
            c = CreditCard()
            c.current_number = n
            self.assertTrue(c.verify_contains_other_separator(), '{0}'.format(n))

    def test_verify_contains_other_separator_invalid(self):
        numbers = [
            '725 36258_7961+57867',
            '9122$2368#7954@32149p',
            '3 253625^87961p57=867'
        ]
        for n in numbers:
            c = CreditCard()
            c.current_number = n
            self.assertFalse(c.verify_contains_other_separator(), '{0}'.format(n))

    def test_verify_more_consecutive_repeated_digit_valid(self):
        valid_numbers = [
            '4253-6258-7961-5786',
            '4424-4244-2444-2444',
            '5122-2368-7954-3214'
        ]
        for n in valid_numbers:
            c = CreditCard()
            c.current_number = n
            self.assertTrue(c.verify_more_consecutive_repeated_digit(), '{0}'.format(n))

    def test_verify_more_consecutive_repeated_digit_invalid(self):
        numbers = [
            '44443677777777961+57867',
            '112$236666654@355p',
            '3 253625^888888888857=867'
            '9999999999999999999999999'
        ]
        for n in numbers:
            c = CreditCard()
            c.current_number = n
            self.assertFalse(c.verify_more_consecutive_repeated_digit(), '{0}'.format(n))

    def test_is_valid_valid(self):
        valid = [('1', True), ('2', True), ('3', True), ('4', True), ('5', True)]
        c = CreditCard()
        self.assertTrue(c.is_valid(valid))

    def test_is_valid_invalid(self):
        invalid = [('1', True), ('2', False), ('3', True), ('4', True), ('5', True)]
        c = CreditCard()
        self.assertFalse(c.is_valid(invalid))

    def test_all_valid(self):
        results = CreditCard(numbers=self.valid_numbers).validate()
        for r in results:
            self.assertTrue(r['is_valid'], '{0}<>{1}'.format(r['number'], r['is_valid']))

    def test_all_invalid(self):
        results = CreditCard(numbers=self.invalid_numbers).validate()
        for r in results:
            self.assertFalse(r['is_valid'], '{0}<>{1}'.format(r['number'], r['is_valid']))
