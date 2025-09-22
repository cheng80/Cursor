"""Tkinter 기반 틱택토 게임."""
from __future__ import annotations

import sys
import tkinter as tk
from tkinter import messagebox


class TicTacToeGUI:
    """틱택토 게임의 GUI를 구성하고 게임 흐름을 제어하는 클래스."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("틱택토")
        self.root.resizable(False, False)
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(50, self.root.focus_force)
        self.root.after(1500, lambda: self.root.attributes("-topmost", False))

        self.board = [""] * 9
        self.current_player = "X"
        self.moves = 0
        self.game_active = False

        self.buttons: list[tk.Button] = []
        self.status_label: tk.Label | None = None
        self.start_frame: tk.Frame | None = None
        self.board_frame: tk.Frame | None = None

        self._create_start_screen()

    def _create_start_screen(self) -> None:
        """게임 방법을 소개하는 시작 화면을 구성합니다."""
        self.start_frame = tk.Frame(self.root, padx=24, pady=24)
        self.start_frame.pack()

        title = tk.Label(
            self.start_frame,
            text="틱택토 게임에 오신 것을 환영합니다",
            font=("Arial", 20, "bold"),
        )
        title.pack(pady=(0, 12))

        instructions = (
            "• X가 먼저 시작하고 번갈아가며 말을 둡니다.\n"
            "• 아래 보드를 참고해 원하는 칸의 버튼을 클릭하세요.\n"
            "• 가로, 세로, 대각선으로 세 칸을 먼저 연결하면 승리합니다!"
        )
        guide = tk.Label(
            self.start_frame,
            text=instructions,
            justify="left",
            anchor="w",
            font=("Arial", 12),
            padx=8,
        )
        guide.pack(fill="x", pady=(0, 12))

        preview_wrapper = tk.Frame(self.start_frame)
        preview_wrapper.pack(pady=(0, 16))

        preview_label = tk.Label(
            preview_wrapper,
            text="보드 미리보기",
            font=("Arial", 11, "bold"),
        )
        preview_label.pack()

        board_preview = tk.Frame(preview_wrapper, relief=tk.RIDGE, bd=2, padx=6, pady=6)
        board_preview.pack(pady=(6, 0))

        for row in range(3):
            for col in range(3):
                number = row * 3 + col + 1
                cell = tk.Label(
                    board_preview,
                    text=str(number),
                    width=4,
                    height=2,
                    font=("Arial", 18, "bold"),
                    relief=tk.RAISED,
                    bd=2,
                    bg="#f7f9fb",
                )
                cell.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        start_button = tk.Button(
            self.start_frame,
            text="게임 시작",
            font=("Arial", 14, "bold"),
            width=12,
            command=self._start_game,
        )
        start_button.pack(pady=(18, 0))

        self._center_on_pointer_monitor()

    def _start_game(self) -> None:
        """시작 화면을 제거하고 본 게임 화면을 초기화합니다."""
        if self.start_frame:
            self.start_frame.destroy()
            self.start_frame = None
        self._create_game_widgets()
        self._reset_board()
        self.game_active = True

    def _create_game_widgets(self) -> None:
        """게임 진행에 필요한 위젯을 생성합니다."""
        self.status_label = tk.Label(
            self.root,
            text=f"플레이어 {self.current_player}의 차례입니다",
            font=("Arial", 16),
            fg="green",
        )
        self.status_label.pack(pady=(10, 5))

        self.board_frame = tk.Frame(self.root, padx=10, pady=10)
        self.board_frame.pack()

        self.buttons.clear()
        for row in range(3):
            for col in range(3):
                index = row * 3 + col
                button = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    command=lambda idx=index: self._handle_move(idx),
                    disabledforeground="black",
                )
                button.grid(row=row, column=col, padx=4, pady=4)
                self.buttons.append(button)

        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack()

        restart_button = tk.Button(
            control_frame,
            text="다시 시작",
            font=("Arial", 12, "bold"),
            width=10,
            command=self._reset_board,
        )
        restart_button.pack(side=tk.LEFT, padx=6)

        quit_button = tk.Button(
            control_frame,
            text="종료",
            font=("Arial", 12, "bold"),
            width=10,
            command=self.root.destroy,
        )
        quit_button.pack(side=tk.LEFT, padx=6)

        self._center_on_pointer_monitor()

    def _handle_move(self, position: int) -> None:
        """선택된 위치에 현재 플레이어의 말을 두고 승패를 확인합니다."""
        if not self.game_active or self.board[position]:
            return

        marker = self.current_player
        self.board[position] = marker
        color = "blue" if marker == "X" else "red"
        self.buttons[position].config(
            text=marker,
            state="disabled",
            disabledforeground=color,
        )
        self.moves += 1

        if self._check_winner(marker):
            self._finish_game(f"플레이어 {marker}의 승리입니다!")
            return

        if self.moves == 9:
            self._finish_game("무승부입니다.")
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        if self.status_label:
            self.status_label.config(text=f"플레이어 {self.current_player}의 차례입니다")

    def _check_winner(self, marker: str) -> bool:
        """현재 플레이어가 승리 조건을 만족하는지 판별합니다."""
        win_conditions = (
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        )
        for line in win_conditions:
            if all(self.board[index] == marker for index in line):
                for idx in line:
                    self.buttons[idx].config(bg="#f9e79f")  # 승리 라인을 강조
                return True
        return False

    def _finish_game(self, message: str) -> None:
        """게임을 종료하고 결과를 알려줍니다."""
        self.game_active = False
        for button in self.buttons:
            button.config(state="disabled")
        if self.status_label:
            self.status_label.config(text=message, fg="blue")
        # UI 상태를 먼저 갱신한 뒤 결과 팝업을 띄워 화면 반영이 늦지 않도록 합니다.
        self.root.update_idletasks()
        messagebox.showinfo("게임 종료", message)

    def _reset_board(self) -> None:
        """보드를 초기 상태로 되돌리고 새 게임을 시작합니다."""
        self.board = [""] * 9
        self.current_player = "X"
        self.moves = 0
        self.game_active = True

        for button in self.buttons:
            button.config(
                text="",
                state="normal",
                bg="SystemButtonFace",
                disabledforeground="black",
                fg="black",
            )

        if self.status_label:
            self.status_label.config(
                text=f"플레이어 {self.current_player}의 차례입니다",
                fg="green",
            )

    def _center_on_pointer_monitor(self) -> None:
        """마우스가 위치한 모니터 중앙에 창을 배치합니다."""
        self.root.update_idletasks()
        width = self.root.winfo_width() or self.root.winfo_reqwidth()
        height = self.root.winfo_height() or self.root.winfo_reqheight()

        monitor = self._get_pointer_monitor_geometry()
        if monitor:
            origin_x, origin_y, monitor_width, monitor_height = monitor
            x = origin_x + (monitor_width - width) // 2
            y = origin_y + (monitor_height - height) // 2
        else:
            pointer_x, pointer_y = self.root.winfo_pointerxy()
            x = pointer_x - width // 2
            y = pointer_y - height // 2

        self.root.geometry(f"+{x}+{y}")

    def _get_pointer_monitor_geometry(self) -> tuple[int, int, int, int] | None:
        """포인터가 위치한 모니터의 (x, y, width, height)를 반환합니다."""
        if sys.platform == "darwin":
            try:
                from AppKit import NSEvent, NSScreen
            except Exception:
                return None

            screens = NSScreen.screens()
            if not screens:
                return None

            mouse_location = NSEvent.mouseLocation()
            pointer_x = mouse_location.x
            pointer_y = mouse_location.y

            total_height = max(
                screen.frame().origin.y + screen.frame().size.height for screen in screens
            )

            for screen in screens:
                frame = screen.frame()
                if (
                    frame.origin.x <= pointer_x < frame.origin.x + frame.size.width
                    and frame.origin.y <= pointer_y < frame.origin.y + frame.size.height
                ):
                    left = int(frame.origin.x)
                    top = int(total_height - (frame.origin.y + frame.size.height))
                    width = int(frame.size.width)
                    height = int(frame.size.height)
                    return left, top, width, height
            return None

        if sys.platform.startswith("win"):
            try:
                import ctypes
                from ctypes import wintypes
            except Exception:
                return None

            class RECT(ctypes.Structure):
                _fields_ = (
                    ("left", wintypes.LONG),
                    ("top", wintypes.LONG),
                    ("right", wintypes.LONG),
                    ("bottom", wintypes.LONG),
                )

            class MONITORINFO(ctypes.Structure):
                _fields_ = (
                    ("cbSize", wintypes.DWORD),
                    ("rcMonitor", RECT),
                    ("rcWork", RECT),
                    ("dwFlags", wintypes.DWORD),
                )

            class POINT(ctypes.Structure):
                _fields_ = (("x", wintypes.LONG), ("y", wintypes.LONG))

            user32 = ctypes.windll.user32
            pt = POINT()
            if not user32.GetCursorPos(ctypes.byref(pt)):
                return None

            MONITOR_DEFAULTTONEAREST = 2
            monitor_handle = user32.MonitorFromPoint(pt, MONITOR_DEFAULTTONEAREST)
            if not monitor_handle:
                return None

            info = MONITORINFO()
            info.cbSize = ctypes.sizeof(MONITORINFO)
            if not user32.GetMonitorInfoW(monitor_handle, ctypes.byref(info)):
                return None

            left = info.rcMonitor.left
            top = info.rcMonitor.top
            width = info.rcMonitor.right - info.rcMonitor.left
            height = info.rcMonitor.bottom - info.rcMonitor.top
            return left, top, width, height

        return None

    def run(self) -> None:
        """Tkinter 메인 루프를 실행합니다."""
        self.root.mainloop()


def main() -> None:
    """GUI 틱택토 게임의 진입 함수."""
    app = TicTacToeGUI()
    app.run()


if __name__ == "__main__":
    main()
