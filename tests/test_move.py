import unittest
import chess
from components.move import Move
from components.opening import Opening, OpeningSet
from components.board import Board
from components.game import Game
from components.screen import Screen  


class TestMove(unittest.TestCase):
    def setUp(self):
        self.board = chess.Board()

    def test_convert_to_chess_from_posn(self):
        move = Move(start_posn=(4, 1), end_posn=(4, 3), board=self.board)
        self.assertIsNotNone(move.chess_move)
        self.assertEqual(move.chess_move.from_square, chess.E2)
        self.assertEqual(move.chess_move.to_square, chess.E4)

    def test_convert_to_chess_from_san(self):
        move = Move(san="e4", board=self.board)
        self.assertIsNotNone(move.chess_move)
        self.assertEqual(move.chess_move.from_square, chess.E2)
        self.assertEqual(move.chess_move.to_square, chess.E4)

    def test_invalid_san(self):
      self.board.push_san("e4")
      move = Move(san = "e4", board = self.board)
      self.assertIsNone(move.chess_move)

    def test_equal_moves(self):
        move1 = Move(start_posn=(4, 1), end_posn=(4, 3), board=self.board)
        move2 = Move(san="e4", board=self.board)
        self.assertEqual(move1, move2)

    def test_unequal_moves(self):
        move1 = Move(start_posn=(4, 1), end_posn=(4, 3), board=self.board)
        move2 = Move(start_posn=(0, 1), end_posn=(0, 3), board=self.board)
        self.assertNotEqual(move1, move2)

    def test_get_san(self):
        move = Move(san = "e4", board = self.board)
        self.assertEqual(move.get_san(), "e4")
    
    def test_execute(self):
        move = Move(san = "e4", board = self.board)
        move.execute(self.board)
        self.assertEqual(self.board.piece_at(chess.E4), chess.Piece.from_symbol("P"))

    def test_undo(self):
      move = Move(san = "e4", board = self.board)
      move.execute(self.board)
      move.undo(self.board)
      self.assertIsNone(self.board.piece_at(chess.E4))


class TestOpening(unittest.TestCase):
    def setUp(self):
        self.opening_sequence = " /e4/c5/Nf3/Nc6"
        self.opening = Opening(self.opening_sequence, chess.WHITE)
    
    def test_convert_to_moves(self):
      self.assertEqual(len(self.opening.moves), 4)
      self.assertEqual(self.opening.moves[0].get_san(), "e4")
      self.assertEqual(self.opening.moves[1].get_san(), "cxc5")
      self.assertEqual(self.opening.moves[2].get_san(), "Nf3")
      self.assertEqual(self.opening.moves[3].get_san(), "Nxc6")

    def test_get_next_move(self):
        self.assertEqual(self.opening.get_next_move().get_san(), "e4")
        self.opening.move_forward()
        self.assertEqual(self.opening.get_next_move().get_san(), "c5")
    
    def test_check_move(self):
        board = chess.Board()
        move1 = Move(san = "e4", board = board)
        move2 = Move(san = "c4", board = board)
        self.assertTrue(self.opening.check_move(move1))
        self.assertFalse(self.opening.check_move(move2))

    def test_move_forward(self):
      self.opening.move_forward()
      self.assertEqual(self.opening.get_next_move().get_san(), "c5")
    
    def test_reset_current_index(self):
      self.opening.move_forward()
      self.opening.reset_current_index()
      self.assertEqual(self.opening.get_next_move().get_san(), "e4")
    
    def test_save_pgn(self):
        self.opening.save_pgn("test.pgn")



class TestGame(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.screen = Screen()
        self.game = Game(self.board, self.screen)
        self.opening_sequence = "Test Opening/e4/c5/Nf3/Nc6"
        self.opening = Opening(self.opening_sequence, chess.WHITE)
        self.game.load_opening(self.opening)
    
    def test_load_opening(self):
      self.assertIsNotNone(self.game.opening)

    def test_manage_current_user_move(self):
      self.game.manage_current_user_move((4,1)) #e2
      self.game.manage_current_user_move((4,3)) #e4
      self.assertEqual(self.board.piece_at(chess.E4), chess.Piece.from_symbol("P"))

    def test_make_user_move(self):
      board = chess.Board()
      move = Move(san = "e4", board = board)
      self.assertTrue(self.game.make_user_move(move))
      self.assertEqual(self.board.piece_at(chess.E4), chess.Piece.from_symbol("P"))
    
    def test_make_trainer_move(self):
      self.game.make_trainer_move()
      self.assertEqual(self.board.piece_at(chess.C5), chess.Piece.from_symbol("p"))
      
    def test_complete_opening(self):
      self.game.complete_opening()
      self.assertEqual(self.game.num_correct, 1)

    def test_start_practice(self):
      self.game.start_practice()
      self.assertTrue(self.game.practice_mode)
    
    def test_change_mode(self):
      self.game.change_mode()
      self.assertTrue(self.game.practice_mode)
      self.game.change_mode()
      self.assertFalse(self.game.practice_mode)

    def test_reset_opening_state(self):
      self.game.manage_current_user_move((4, 1))  # e2
      self.game.manage_current_user_move((4, 3)) #e4
      self.game.reset_opening_state()
      self.assertIsNone(self.board.piece_at(chess.E4))
      
    def test_pieces(self):
        self.assertEqual(len(self.game.pieces), 32)



if __name__ == '__main__':
    unittest.main()
