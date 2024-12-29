import chess
import bot

board = chess.Board()
turn = chess.WHITE
while True:
    turn_ip = input("사용자의 차례를 선택하세요: ")
    if turn_ip == "w" or turn_ip == "W":
        turn = chess.WHITE
        break
    elif turn_ip == "b" or turn_ip == "B":
        turn = chess.BLACK
        break
    else:
        print("올바르지 않은 입력입니다.")

while True:
    if board.turn == turn:
        while True:
            move_ip = input("수를 두세요: ")
            try:
                move = chess.Move.from_uci(move_ip)
                if board.is_legal(move):
                    board.push(move)
                    print("수를 두었습니다:", move)
                    break
                else:
                    print("수가 올바르지 않습니다.")
            except chess.InvalidMoveError:
                print("입력 형식이 잘못되었습니다.")
    else:
        move = bot.move(board)
        board.push(move)
        print("봇이 수를 두었습니다:", move)

    if board.can_claim_draw() or board.is_stalemate():
        print("무승부입니다.")
        break
    elif board.is_checkmate():
        print("백 승입니다." if board.turn == chess.BLACK else "흑 승입니다.")
        break
    else:
        print()
