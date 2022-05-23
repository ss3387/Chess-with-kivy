import chess

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.turn = {chess.WHITE: 'white', chess.BLACK: 'black'}
        self.results = {'1-0': 'White won', '0-1': 'Black won', '1/2-1/2': 'It\'s a draw'}
    
    def add_move(self, move: str, update_board):
        if chess.Move.from_uci(move) in self.board.legal_moves:
            san = self.board.san(chess.Move.from_uci(move))
            self.board.push_uci(move)
            
            update_board(self.board.unicode, san, self.turn[self.board.turn])
        if self.board.is_game_over():
            pass
