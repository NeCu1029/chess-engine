import chess
import random
import pos


def base(board: chess.BaseBoard):
    res = 0
    bs = str(board).split()
    for i in range(64):
        if bs[i] in pos.score:
            res += pos.score[bs[i]][i]
        elif bs[i].upper() in pos.score:
            r, c = divmod(i, 8)
            j = 8 * (7 - r) + c
            res -= pos.score[bs[i].upper()][j]
    return res


def val(
    board: chess.Board, alpha: int = -1000000, beta: int = 1000000, depth: int = 3
) -> int:
    if depth == 0:
        return base(board)
    if board.is_stalemate():
        return 30 * (1 - 2 * board.turn)

    res = 1000000 * (1 - 2 * board.turn)
    check = []
    capture = []
    nothing = []
    for move in board.legal_moves:
        board.push(move)
        if board.is_check():
            check.append(move)
            board.pop()
            continue
        board.pop()
        if board.is_capture(move):
            capture.append(move)
        else:
            nothing.append(move)

    for move in check + capture + nothing:
        board.push(move)
        if board.is_stalemate():
            cur = -30 * (1 - 2 * board.turn)
        elif board.is_checkmate():
            cur = 500000 * (1 - 2 * board.turn)
        else:
            cur = val(board, alpha, beta, depth - 1)
        board.pop()

        if board.turn:
            res = max(res, cur)
            alpha = max(alpha, cur)
        else:
            res = min(res, cur)
            beta = min(beta, cur)
        if alpha >= beta:
            break

    return res


def move(board: chess.Board) -> chess.Move:
    if len(board.piece_map()) <= 12:
        pos.score = pos.end
    best_val = 1000000 * (1 - 2 * board.turn)
    best_move = []

    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            board.pop()
            return move
        cur = val(board)
        board.pop()
        if board.turn:
            if best_val < cur:
                best_val = cur
                best_move = [move]
            elif best_val == cur:
                best_move.append(move)
        else:
            if best_val > cur:
                best_val = cur
                best_move = [move]
            elif best_val == cur:
                best_move.append(move)

    return random.choice(best_move)
