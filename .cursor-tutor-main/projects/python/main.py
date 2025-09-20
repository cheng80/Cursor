#####################
# Welcome to Cursor #
#####################

'''
Step 1: Try generating with Cmd+K or Ctrl+K on a new line. Ask for CLI-based game of TicTacToe.

Step 2: Hit Cmd+L or Ctrl+L and ask the chat what the code does. 
   - Then, try running the code

Step 3: Try highlighting all the code with your mouse, then hit Cmd+k or Ctrl+K. 
   - Instruct it to change the game in some way (e.g. add colors, add a start screen, make it 4x4 instead of 3x3)

Step 4: To try out cursor on your own projects, go to the file menu (top left) and open a folder.
'''

import tkinter as tk
from tkinter import messagebox, font
import sys

class TicTacToeGUI:
    """
    Tkinter를 사용한 틱택토 게임 GUI 클래스
    게임의 모든 UI와 로직을 관리합니다.
    """
    
    def __init__(self):
        """
        게임 GUI를 초기화하는 생성자
        게임 상태와 UI 요소들을 설정합니다.
        """
        # 메인 윈도우 생성
        self.root = tk.Tk()
        self.root.title("틱택토 게임")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # 게임 상태 변수들
        self.board = [""] * 9  # 3x3 게임판을 1차원 리스트로 표현
        self.current_player = "X"  # 현재 플레이어 (X 또는 O)
        self.moves = 0  # 총 이동 횟수
        self.game_over = False  # 게임 종료 여부
        
        # UI 요소들을 저장할 변수들
        self.buttons = []  # 게임판 버튼들을 저장할 리스트
        self.status_label = None  # 현재 상태를 표시할 라벨
        self.restart_button = None  # 게임 재시작 버튼
        
        # GUI 생성
        self.create_widgets()
        
        # 게임 시작 메시지 표시
        self.show_welcome_message()
    
    def create_widgets(self):
        """
        게임의 모든 UI 위젯들을 생성하고 배치하는 함수
        """
        # 제목 라벨
        title_label = tk.Label(
            self.root, 
            text="틱택토 게임", 
            font=("Arial", 24, "bold"),
            fg="blue"
        )
        title_label.pack(pady=20)
        
        # 현재 상태를 표시할 라벨
        self.status_label = tk.Label(
            self.root,
            text=f"플레이어 {self.current_player}의 차례입니다",
            font=("Arial", 16),
            fg="green"
        )
        self.status_label.pack(pady=10)
        
        # 게임판 프레임 생성
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=20)
        
        # 3x3 게임판 버튼들 생성
        for i in range(3):
            for j in range(3):
                # 각 버튼의 위치 인덱스 계산 (0-8)
                button_index = i * 3 + j
                
                # 게임판 버튼 생성
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Arial", 20, "bold"),
                    width=6,
                    height=3,
                    command=lambda idx=button_index: self.make_move(idx),
                    bg="lightgray",
                    activebackground="lightblue"
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                
                # 버튼을 리스트에 저장
                self.buttons.append(button)
        
        # 게임 방법 안내 라벨
        instruction_label = tk.Label(
            self.root,
            text="빈 칸을 클릭하여 말을 놓으세요!\n가로, 세로, 대각선으로 3개를 먼저 완성하면 승리!",
            font=("Arial", 12),
            fg="gray"
        )
        instruction_label.pack(pady=10)
        
        # 게임 재시작 버튼
        self.restart_button = tk.Button(
            self.root,
            text="새 게임 시작",
            font=("Arial", 14, "bold"),
            command=self.restart_game,
            bg="orange",
            fg="black",  # 글자색을 검은색으로 변경
            activebackground="darkorange"
        )
        self.restart_button.pack(pady=20)
        
        # 종료 버튼
        quit_button = tk.Button(
            self.root,
            text="게임 종료",
            font=("Arial", 12),
            command=self.quit_game,
            bg="red",
            fg="black",  # 글자색을 검은색으로 변경
            activebackground="darkred"
        )
        quit_button.pack(pady=5)
    
    def show_welcome_message(self):
        """
        게임 시작 시 환영 메시지를 표시하는 함수
        """
        messagebox.showinfo(
            "게임 시작",
            "틱택토 게임에 오신 것을 환영합니다!\n\n"
            "게임 방법:\n"
            "• 두 플레이어가 번갈아가며 X와 O를 놓습니다\n"
            "• 가로, 세로, 대각선으로 같은 모양을 먼저 완성하면 승리!\n"
            "• 빈 칸을 클릭하여 말을 놓으세요"
        )
    
    def disable_game_buttons(self):
        """
        게임 종료 후 게임판 버튼들만 비활성화하는 함수
        재시작 버튼과 종료 버튼은 활성화 상태로 유지
        """
        for button in self.buttons:
            # command를 None으로 설정하고 state를 disabled로 설정하여 클릭 이벤트 완전 무효화
            button.config(command=None, bg="lightgray", state="disabled")
    
    def enable_game_buttons(self):
        """
        게임 재시작 시 게임판 버튼들만 활성화하는 함수
        """
        for i, button in enumerate(self.buttons):
            # 각 버튼에 올바른 command 함수 재할당하고 state를 normal로 설정
            button.config(command=lambda idx=i: self.make_move(idx), bg="lightgray", state="normal")
    
    def make_move(self, position):
        """
        플레이어가 선택한 위치에 말을 놓는 함수
        position: 선택된 위치 (0-8)
        """
        # 게임이 종료되었거나 이미 말이 놓인 위치라면 무시
        if self.game_over or self.board[position] != "":
            return
        
        # 선택한 위치에 현재 플레이어의 말 놓기
        self.board[position] = self.current_player
        self.buttons[position].config(
            text=self.current_player,
            fg="blue" if self.current_player == "X" else "red"
        )
        self.moves += 1
        
        # 승리 조건 확인
        if self.check_winner(self.current_player):
            self.game_over = True
            self.status_label.config(
                text=f"🎉 플레이어 {self.current_player}가 승리했습니다!",
                fg="red"
            )
            # 게임 종료 후 게임판 버튼들만 비활성화
            self.disable_game_buttons()
            messagebox.showinfo("게임 종료", f"플레이어 {self.current_player}가 승리했습니다!")
            return
        
        # 무승부 확인
        if self.moves == 9:
            self.game_over = True
            self.status_label.config(
                text="무승부입니다!",
                fg="orange"
            )
            # 게임 종료 후 게임판 버튼들만 비활성화
            self.disable_game_buttons()
            messagebox.showinfo("게임 종료", "무승부입니다!")
            return
        
        # 플레이어 교체
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(
            text=f"플레이어 {self.current_player}의 차례입니다",
            fg="green"
        )
    
    def check_winner(self, player):
        """
        현재 플레이어가 승리했는지 확인하는 함수
        player: 확인할 플레이어 (X 또는 O)
        return: 승리 여부 (True/False)
        """
        # 가로, 세로, 대각선 승리 조건들
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # 가로 3줄
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # 세로 3줄
            [0, 4, 8], [2, 4, 6]              # 대각선 2줄
        ]
        
        # 각 승리 조건을 확인
        for condition in win_conditions:
            if all(self.board[i] == player for i in condition):
                # 승리한 줄의 버튼들을 하이라이트
                for i in condition:
                    self.buttons[i].config(bg="yellow")
                return True
        return False
    
    def restart_game(self):
        """
        게임을 초기 상태로 재시작하는 함수
        """
        # 게임 상태 초기화
        self.board = [""] * 9
        self.current_player = "X"
        self.moves = 0
        self.game_over = False
        
        # 게임판 버튼들만 초기화 및 활성화
        for button in self.buttons:
            button.config(text="", bg="lightgray", fg="black", state="normal")
        
        # 상태 라벨 초기화
        self.status_label.config(
            text=f"플레이어 {self.current_player}의 차례입니다",
            fg="green"
        )
        
        # 게임 버튼들을 활성화 (command 함수 재할당)
        self.enable_game_buttons()
    
    def quit_game(self):
        """
        게임을 종료하는 함수
        """
        if messagebox.askyesno("게임 종료", "정말로 게임을 종료하시겠습니까?"):
            self.root.quit()
            sys.exit()
    
    def run(self):
        """
        게임 GUI를 실행하는 함수
        """
        self.root.mainloop()
    
    def disable_all_buttons(self):
        """
        게임 종료 후 모든 게임판 버튼을 비활성화하는 함수
        """
        for button in self.buttons:
            button.config(state="disabled", bg="lightgray")
    
    def enable_all_buttons(self):
        """
        게임 재시작 시 모든 게임판 버튼을 활성화하는 함수
        """
        for button in self.buttons:
            button.config(state="normal", bg="lightgray")

def main():
    """
    메인 실행 함수
    틱택토 GUI 게임을 시작합니다.
    """
    # GUI 게임 인스턴스 생성 및 실행
    game = TicTacToeGUI()
    game.run()

# 프로그램 시작점
if __name__ == "__main__":
    main()
