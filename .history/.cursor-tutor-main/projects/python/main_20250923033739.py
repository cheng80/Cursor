"""Command-line Tic Tac Toe game."""
from __future__ import annotations

import itertools
from typing import List

# 3x3 보드에서 가능한 모든 승리 조합을 미리 정의합니다.
WIN_CONDITIONS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # 가로 줄
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # 세로 줄
    (0, 4, 8), (2, 4, 6),             # 대각선
)


def display_board(board: List[str]) -> None:
    """Render the board, showing numbers for empty cells."""
    # 빈 칸에는 숫자를 보여줘서 선택 가능한 위치를 직관적으로 표시합니다.
    cells = [cell if cell else str(index + 1) for index, cell in enumerate(board)]
    print()
    print(f" {cells[0]} | {cells[1]} | {cells[2]}")
    print("---+---+---")
    print(f" {cells[3]} | {cells[4]} | {cells[5]}")
    print("---+---+---")
    print(f" {cells[6]} | {cells[7]} | {cells[8]}")
    print()


def check_winner(board: List[str], marker: str) -> bool:
    """Return True when marker occupies any winning condition."""
    # 정의된 승리 조합 중 하나라도 현재 플레이어의 말로 채워지면 승리입니다.
    return any(all(board[index] == marker for index in line) for line in WIN_CONDITIONS)


def get_move(board: List[str], marker: str) -> int:
    """Prompt the current player until a valid move is chosen."""
    # 입력값이 1~9 범위인지, 이미 놓인 말이 있는지 차례대로 검증합니다.
    while True:
        choice = input(f"플레이어 {marker}, 놓을 위치를 선택하세요 (1-9): ")
        if not choice.isdigit():
            print("숫자를 입력해주세요.")
            continue
        index = int(choice) - 1
        if index not in range(9):
            print("1에서 9 사이의 숫자를 선택해주세요.")
            continue
        if board[index]:
            print("이미 선택된 칸입니다. 다른 칸을 선택하세요.")
            continue
        return index


def play_round() -> None:
    """Play a single round of Tic Tac Toe."""
    board: List[str] = [""] * 9
    # itertools.cycle을 사용해 X와 O 플레이어를 번갈아가며 제공합니다.
    players = itertools.cycle(("X", "O"))

    print("틱택토 게임에 오신 것을 환영합니다!\n세 칸을 연결하면 승리입니다.")

    for turn in range(9):
        marker = next(players)
        display_board(board)
        move = get_move(board, marker)
        board[move] = marker

        # 다섯 번째 턴부터 승패가 결정될 수 있으므로 매번 확인합니다.
        if turn >= 4 and check_winner(board, marker):
            display_board(board)
            print(f"플레이어 {marker}의 승리입니다!\n")
            return

    display_board(board)
    print("무승부입니다. 다시 도전해보세요!\n")


def prompt_play_again() -> bool:
    """Ask the players if they want to play another round."""
    # y/n 입력을 명확히 받을 때까지 반복합니다.
    while True:
        answer = input("다시 플레이하시겠습니까? (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("y 또는 n으로 답변해주세요.")


def show_start_screen() -> None:
    """Introduce the rules and wait for the players to start."""
    print(
        """
================ 틱택토 =================
• 두 플레이어가 번갈아가며 말을 둡니다. X가 먼저 시작합니다.
• 숫자 1~9는 아래 보드의 위치를 나타냅니다.

  1 | 2 | 3
 ---+---+---
  4 | 5 | 6
 ---+---+---
  7 | 8 | 9

• 가로, 세로, 대각선으로 세 칸을 연결하면 승리합니다.
• 잘못된 입력은 다시 요청하니 걱정하지 마세요.
=======================================
"""
    )
    input("시작하려면 Enter 키를 누르세요...")


def main() -> None:
    """Entry point for the CLI Tic Tac Toe game."""
    show_start_screen()

    # 사용자가 종료를 선택할 때까지 라운드를 반복합니다.
    while True:
        play_round()
        if not prompt_play_again():
            print("게임을 종료합니다. 플레이해주셔서 감사합니다!")
            break


if __name__ == "__main__":
    main()
