from datetime import datetime
from trello import TrelloClient
import unittest
import os
import datetime


class TrelloClientTestCase(unittest.TestCase):
    """
	Tests for TrelloClient API. Note these test are in order to preserve dependencies, as an API
	integration cannot be tested independently.
	"""

    def setUp(self):
        self._trello = TrelloClient(api_key='f8fd231446c1fd27f49e0d8f933252f3',
                                    api_secret='338b8eef2cc489ce5cfc9f2252c73f5cf51b44a41cc6cb790be20feb9ed19f2d',token='8004f00bc94627ac6eb98333492a76315821ed06e9d04eec4b6480d1f575758b',token_secret='a528cdd05a0dd7314f45995fdf457c45')

    def test01_list_boards(self):
        self.assertEquals(
            len(self._trello.list_boards()),
            int(4))

    def test10_board_attrs(self):
        boards = self._trello.list_boards()
        for b in boards:
            self.assertIsNotNone(b.id, msg="id not provided")
            self.assertIsNotNone(b.name, msg="name not provided")
            self.assertIsNotNone(b.description, msg="description not provided")
            self.assertIsNotNone(b.closed, msg="closed not provided")
            self.assertIsNotNone(b.url, msg="url not provided")

    def test20_board_all_lists(self):
        boards = self._trello.list_boards()
        for b in boards:
            try:
                b.all_lists()
            except Exception as e:
                self.fail("Caught Exception getting lists")

    def test21_board_open_lists(self):
        boards = self._trello.list_boards()
        for b in boards:
            try:
                b.open_lists()
            except Exception as e:
                self.fail("Caught Exception getting open lists")

    def test22_board_closed_lists(self):
        boards = self._trello.list_boards()
        for b in boards:
            try:
                b.closed_lists()
            except Exception as e:
                self.fail("Caught Exception getting closed lists")

    def test30_list_attrs(self):
        boards = self._trello.list_boards()
        for b in boards:
            for l in b.all_lists():
                self.assertIsNotNone(l.id, msg="id not provided")
                self.assertIsNotNone(l.name, msg="name not provided")
                self.assertIsNotNone(l.closed, msg="closed not provided")
            break  # only need to test one board's lists

    def test50_list_cards(self):
        boards = self._trello.list_boards()
        for b in boards:
            for l in b.all_lists():
                for c in l.list_cards():
                    self.assertIsNotNone(c.id, msg="id not provided")
                    self.assertIsNotNone(c.name, msg="name not provided")
                    self.assertIsNotNone(c.description, msg="description not provided")
                    self.assertIsNotNone(c.closed, msg="closed not provided")
                    self.assertIsNotNone(c.url, msg="url not provided")
                break
            break
        pass

    def test51_fetch_cards(self):
        """
        Tests fetching all attributes for all cards
        """
        boards = self._trello.list_boards()
        for b in boards:
            for l in b.all_lists():
                for c in l.list_cards():
                    c.fetch()

                    self.assertIsInstance(c.date_last_activity, datetime, msg='date not provided')
                    self.assertTrue(len(c.board_id) > 0, msg='board id not provided')
                break
            break
        pass


    def test52_get_cards(self):
        boards = [board for board in self._trello.list_boards() if board.name == 'Proy Industria']
        self.assertEquals(len(boards), 1, msg="Test board not found")

        board = boards[0]
        cards = board.get_cards()
        self.assertEqual(len(cards), 3, msg="Unexpected number of cards in testboard")

        for card in cards:
            if card.name == 'Testing from Python':
                self.assertEqual(card.description, 'Description goes here')
            elif card.name == 'Testing from Python - no desc':
                self.assertEqual(card.description, '')
            elif card.name == 'Card with comments':
                self.assertEqual(card.description, '')
            else:
                self.fail(msg='Unexpected card found')


if __name__ == "__main__":
    unittest.main()
