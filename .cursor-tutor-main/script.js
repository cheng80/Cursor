const canvas = document.getElementById('board');
const ctx = canvas.getContext('2d');
const resetButton = document.getElementById('reset');
const currentPlayerDisplay = document.getElementById('current-player');

const BOARD_SIZE = 15;
const CELL_SIZE = canvas.width / (BOARD_SIZE + 1);
const STONE_RADIUS = CELL_SIZE * 0.4;

let board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
let currentPlayer = 1; // 1: 흑돌, 2: 백돌
let gameOver = false;

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 바둑판 그리기
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    
    for (let i = 0; i < BOARD_SIZE; i++) {
        // 가로선
        ctx.beginPath();
        ctx.moveTo(CELL_SIZE, CELL_SIZE * (i + 1));
        ctx.lineTo(CELL_SIZE * BOARD_SIZE, CELL_SIZE * (i + 1));
        ctx.stroke();
        
        // 세로선
        ctx.beginPath();
        ctx.moveTo(CELL_SIZE * (i + 1), CELL_SIZE);
        ctx.lineTo(CELL_SIZE * (i + 1), CELL_SIZE * BOARD_SIZE);
        ctx.stroke();
    }
    
    // 돌 그리기
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            if (board[i][j] !== 0) {
                const x = CELL_SIZE * (j + 1);
                const y = CELL_SIZE * (i + 1);
                
                ctx.beginPath();
                ctx.arc(x, y, STONE_RADIUS, 0, Math.PI * 2);
                ctx.fillStyle = board[i][j] === 1 ? '#000' : '#fff';
                ctx.fill();
                ctx.strokeStyle = '#000';
                ctx.stroke();
            }
        }
    }
}

function checkWin(row, col) {
    const directions = [
        [[0, 1], [0, -1]], // 수평
        [[1, 0], [-1, 0]], // 수직
        [[1, 1], [-1, -1]], // 대각선
        [[1, -1], [-1, 1]]  // 대각선
    ];
    
    for (const direction of directions) {
        let count = 1;
        
        for (const [dx, dy] of direction) {
            let r = row + dx;
            let c = col + dy;
            
            while (
                r >= 0 && r < BOARD_SIZE &&
                c >= 0 && c < BOARD_SIZE &&
                board[r][c] === currentPlayer
            ) {
                count++;
                r += dx;
                c += dy;
            }
        }
        
        if (count >= 5) return true;
    }
    
    return false;
}

function handleClick(e) {
    if (gameOver) return;
    
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const col = Math.round(x / CELL_SIZE) - 1;
    const row = Math.round(y / CELL_SIZE) - 1;
    
    if (
        row >= 0 && row < BOARD_SIZE &&
        col >= 0 && col < BOARD_SIZE &&
        board[row][col] === 0
    ) {
        board[row][col] = currentPlayer;
        
        if (checkWin(row, col)) {
            gameOver = true;
            alert(`${currentPlayer === 1 ? '흑돌' : '백돌'} 승리!`);
            return;
        }
        
        currentPlayer = currentPlayer === 1 ? 2 : 1;
        currentPlayerDisplay.textContent = currentPlayer === 1 ? '흑돌' : '백돌';
        drawBoard();
    }
}

function resetGame() {
    board = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(0));
    currentPlayer = 1;
    gameOver = false;
    currentPlayerDisplay.textContent = '흑돌';
    drawBoard();
}

canvas.addEventListener('click', handleClick);
resetButton.addEventListener('click', resetGame);

drawBoard(); 