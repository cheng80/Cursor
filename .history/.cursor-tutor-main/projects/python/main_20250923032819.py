"""Command-line Tic Tac Toe game."""
from __future__ import annotations

import itertools
from typing import List

# All winning line indices on the 3x3 board
WIN_CONDITIONS = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def display_board(board: List[str]) -> None:
    """Render the board, showing numbers for empty cells."""
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
    return any(all(board[index] == marker for index in line) for line in WIN_CONDITIONS)


def get_move(board: List[str], marker: str) -> int:
    """Prompt the current player until a valid move is chosen."""
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
    players = itertools.cycle(("X", "O"))

    print("틱택토 게임에 오신 것을 환영합니다!\n세 칸을 연결하면 승리입니다.")

    for turn in range(9):
        marker = next(players)
        display_board(board)
        move = get_move(board, marker)
        board[move] = marker

        if turn >= 4 and check_winner(board, marker):
            display_board(board)
            print(f"플레이어 {marker}의 승리입니다!\n")
            return

    display_board(board)
    print("무승부입니다. 다시 도전해보세요!\n")


def prompt_play_again() -> bool:
    """Ask the players if they want to play another round."""
    while True:
        answer = input("다시 플레이하시겠습니까? (y/n): ").strip().lower()
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("y 또는 n으로 답변해주세요.")


def main() -> None:
    """Entry point for the CLI Tic Tac Toe game."""
    while True:
        play_round()
        if not prompt_play_again():
            print("게임을 종료합니다. 플레이해주셔서 감사합니다!")
            break


if __name__ == "__main__":
    main()
