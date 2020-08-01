import sys
from io import StringIO
from contextlib import contextmanager

from aigames.games.ttt.board import Outcome
from aigames.games.ttt.board import Board
from aigames.games.ttt.player import PlayerFactory
from aigames.games.ttt.player import ConsolePlayer
from aigames.games.ttt.player import RandomPlayer


def test_outcome():
    assert Outcome.DRAW.is_finished()
    assert not Outcome.NOT_FINISHED.is_finished()
    assert Outcome.PLAYER1.is_finished()
    assert Outcome.PLAYER1.is_finished()


def test_board():
    player1_win = [
        (0B000011111, 0B000000111, 0B000011000),
        (0B011111000, 0B000111000, 0B011000000),
        (0B111000011, 0B111000000, 0B000000011),
        (0B001011011, 0B001001001, 0B000010010),
        (0B010110110, 0B010010010, 0B000100100),
        (0B100101101, 0B100100100, 0B000001001)
    ]
    for s in player1_win:
        b = Board(s[0], s[1], s[2])
        assert b.check_win(True)
        assert not b.check_win(False)
        assert b.check_outcome().is_finished()
    for s in player1_win:
        b = Board(s[0], s[2], s[1])
        assert not b.check_win(True)
        assert b.check_win(False)
        assert b.check_outcome().is_finished()

    b = Board(0B000011111, 0B000010101, 0B000001010)
    assert b.value_at(1) == 1
    assert b.value_at(2) == 2
    assert b.value_at(6) == 0
    assert b.check_outcome() == Outcome.NOT_FINISHED
    assert [m for m in b.get_valid_moves()] == [6, 7, 8, 9]
    assert b.get_valid_moves_list() == [6, 7, 8, 9]
    assert b.is_valid_move(6)
    assert not b.is_valid_move(5)
    b.move(False, 6)
    assert b.bit_board == 0B000111111
    assert b.bit_p1 == 0B000010101
    assert b.bit_p2 == 0B000101010
    b.undo_move(6)
    assert b.bit_board == 0B000011111
    assert b.bit_p1 == 0B000010101
    assert b.bit_p2 == 0B000001010
    b.move(False, 6)
    b.move(True, 7)
    assert b.bit_board == 0B001111111
    assert b.bit_p1 == 0B001010101
    assert b.bit_p2 == 0B000101010

    b = Board(0B111111111, 0B101100011, 0B010011100)
    assert b.check_outcome() == Outcome.DRAW


def test_player_factory():
    pf = PlayerFactory()
    assert "ConsolePlayer" in pf.player_types
    assert "RandomPlayer" in pf.player_types

    cp = pf.CreatePlayer("ConsolePlayer", True)
    assert cp.is_player1
    rp = pf.CreatePlayer("RandomPlayer", False)
    assert not rp.is_player1


@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig


def test_console_player():
    b = Board()
    p = ConsolePlayer(True)
    with replace_stdin(StringIO("1")):
        assert p.get_player_input(b) == 1
    with replace_stdin(StringIO("2")):
        assert p.get_player_input(b) == 2


def test_random_player():
    b = Board()
    p = RandomPlayer(True)
    moves = b.get_valid_moves_list()
    assert p.get_player_input(b) in moves
    assert p.get_player_input(b) in moves
    assert p.get_player_input(b) in moves
