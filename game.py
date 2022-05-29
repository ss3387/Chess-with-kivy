import chess
import chess.engine

class Game:
    def __init__(self, update_board, against_computer: bool, level: int):
        self.board = chess.Board()
        self.turn = {chess.WHITE: 'white', chess.BLACK: 'black'}
        self.update_board = update_board
        self.update_board(self.board.unicode(), None, self.turn[self.board.turn])
        self.result_phrases = {
                '1-0': 'Checkmate. White is victorious',
                '0-1': 'Checkmate. Black is victorious',
                '1/2-1/2': 'It\'s a draw!'
            }
        self.board.outcome
        self.against_computer = against_computer
        if self.against_computer:
            self.initiate_chess_engine(level)
    
    def add_move(self, move: str):
        if chess.Move.from_uci(move) in self.board.legal_moves:
            san = self.board.san(chess.Move.from_uci(move))
            self.board.push_uci(move)
            self.update_board(self.board.unicode(), san, self.turn[self.board.turn])
        if self.board.turn == chess.BLACK and self.against_computer == True:
            result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
            self.board.push(result.move)
            self.update_board(self.board.unicode(), san, self.turn[self.board.turn])
        if self.board.is_game_over():
            self.update_board(self.board.unicode(), san, self.turn[self.board.turn], msg=self.results[self.board.result()])
    
    def undo(self, instance):
        try:
            self.board.pop()
            if self.against_computer:
                self.board.pop()
            self.update_board(self.board.unicode(), 'undo', self.turn[self.board.turn])
        except:
            pass
    
    def initiate_chess_engine(self, level: int):
        self.engine = chess.engine.SimpleEngine.popen_uci(r"C:\chess_with_kivy\stockfish_14.1_win_x64_avx2.exe")
        self.engine.configure({'Skill Level': level})
