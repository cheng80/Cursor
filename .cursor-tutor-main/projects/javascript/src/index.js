///////////////////////
// Welcome to Cursor //
///////////////////////

/*
Step 1: Try generating a react component that lets you play tictactoe with Cmd+K or Ctrl+K on a new line.
  - Then integrate it into the code below and run with npm start

Step 2: Try highlighting all the code with your mouse, then hit Cmd+k or Ctrl+K. 
  - Instruct it to change the game in some way (e.g. add inline styles, add a start screen, make it 4x4 instead of 3x3)

Step 3: Hit Cmd+L or Ctrl+L and ask the chat what the code does

Step 4: To try out cursor on your own projects, go to the file menu (top left) and open a folder.
*/


import React from 'react';
import ReactDOM from 'react-dom/client';

function TicTacToe() {
  const [board, setBoard] = React.useState(Array(9).fill(null));
  const [xIsNext, setXIsNext] = React.useState(true);

  const calculateWinner = (squares) => {
    const lines = [
      [0, 1, 2],
      [3, 4, 5], 
      [6, 7, 8],
      [0, 3, 6],
      [1, 4, 7],
      [2, 5, 8],
      [0, 4, 8],
      [2, 4, 6]
    ];

    for (let i = 0; i < lines.length; i++) {
      const [a, b, c] = lines[i];
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a];
      }
    }
    return null;
  };

  const handleClick = (i) => {
    const boardCopy = [...board];
    if (calculateWinner(boardCopy) || boardCopy[i]) return;
    boardCopy[i] = xIsNext ? 'X' : 'O';
    setBoard(boardCopy);
    setXIsNext(!xIsNext);
  };

  const renderSquare = (i) => {
    return (
      <button 
        style={{
          width: '60px',
          height: '60px',
          margin: '4px',
          fontSize: '24px'
        }}
        onClick={() => handleClick(i)}
      >
        {board[i]}
      </button>
    );
  };

  const winner = calculateWinner(board);
  const status = winner 
    ? `승자: ${winner}` 
    : `다음 플레이어: ${xIsNext ? 'X' : 'O'}`;

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      marginTop: '50px'
    }}>
      <h1>틱택토 게임</h1>
      <div style={{marginBottom: '20px'}}>{status}</div>
      <div>
        <div style={{display: 'flex'}}>
          {renderSquare(0)}
          {renderSquare(1)}
          {renderSquare(2)}
        </div>
        <div style={{display: 'flex'}}>
          {renderSquare(3)}
          {renderSquare(4)}
          {renderSquare(5)}
        </div>
        <div style={{display: 'flex'}}>
          {renderSquare(6)}
          {renderSquare(7)}
          {renderSquare(8)}
        </div>
      </div>
      <button 
        style={{
          marginTop: '20px',
          padding: '10px 20px',
          fontSize: '16px'
        }}
        onClick={() => setBoard(Array(9).fill(null))}
      >
        게임 재시작
      </button>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <TicTacToe />
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
