// import { useState } from "react";

// const BOARD_SIZE = 9;

// export default function Board() {
//     const [board, setBoard] = useState(
//         Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(null))
//     );

//     const [isBlackTurn, setIsBlackTurn] = useState(true); //true:黒 false:白

//     const handleClick = (x, y) => {
//         if (board[y][x] !== null) return; //石がない時

//         const newBoard = board.map((row) => row.slice());

//         newBoard[y][x] = isBlackTurn ? "●" : "○";

//         setBoard(newBoard);
//         setIsBlackTurn(!isBlackTurn);

//         console.log(`(${x}, ${y}) に ${isBlackTurn ? "●" : "○"} を置きました`);
//     };

//     return (
//         <div style={{ display: "inline-block", border: "2px solid black" }}>
//             {board.map((row, y) => (
//                 <div key={y} style={{ display: "flex"}}>
//                     {row.map((cell, x) => (
//                         <div
//                             key={x}
//                             onClick={() => handleClick(x, y)}
//                             style={{
//                                 width: "40px",
//                                 height: "40px",
//                                 border: "1px solid #555",
//                                 display: "flex",
//                                 alignItems: "center",
//                                 justifyContent: "center",
//                                 cursor: "pointer",
//                                 backgroundColor: cell === "●" ? "black" : cell === "○" ? "white" : "transparent",
//                             }}
//                         >
//                             {cell}
//                         </div>
//                     ))}
//                 </div>
//             ))}
//         </div>
//     );
// }
import { useState } from "react";

const BOARD_SIZE = 15; // 15x15の五目並べ盤

export default function Board() {
  const [board, setBoard] = useState(
    Array(BOARD_SIZE)
      .fill(null)
      .map(() => Array(BOARD_SIZE).fill(null))
  );
  const [isBlackTurn, setIsBlackTurn] = useState(true);

  const [winner, setWinner] = useState(null);

  const checkWin = (board, x, y, color) => {
    const directions = [
        [1, 0],
        [0, 1],
        [1, 1],
        [1, -1],
    ];

    for (const [dx, dy] of directions) {
        let count = 1;

        let nx = x + dx;
        let ny = y + dy;
        while (
            nx >= 0 && nx < BOARD_SIZE &&
            ny >= 0 && ny < BOARD_SIZE &&
            board[ny][nx] === color
        ) {
            count++;
            nx += dx;
            ny += dy;
        }

        nx = x - dx;
        ny = y - dy;
        while (
            nx >= 0 && nx < BOARD_SIZE &&
            ny >= 0 && ny < BOARD_SIZE &&
            board[ny][nx] === color
        ) {
            count++;
            nx -= dx;
            ny -= dy;
        }

        if (count >= 5) return true;
    }

    return false;
  };

  const resetGame = () => {
    setBoard(
        Array(BOARD_SIZE).fill(null).map(() => Array(BOARD_SIZE).fill(null))
    );
    setIsBlackTurn(true);
    setWinner(null);
  }

  const getAIMove = async (currentBoard) => {
    console.log("getAI呼ばれたよ");
    try {
        const response = await fetch("http://localhost:5001/ai-move", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ board: currentBoard}),
        });

        if (!response.ok) {
            throw new Error("AIリクエスト失敗");
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("AIとの通信に失敗しました:", error);
        return null;
    }
  };

  const handleClick = async (x, y) => {
    if (board[y][x] !== null || winner !== null) return;

    const newBoard = board.map((row) => row.slice());
    const playerColor = isBlackTurn ? "black" : "white";
    const aiColor = isBlackTurn ? "white" : "black;"
    
    newBoard[y][x] = playerColor;
    setBoard(newBoard);

    if (checkWin(newBoard, x, y, playerColor)) {
        setWinner(playerColor);
        return;
    }

    const aiMove = await getAIMove(newBoard);

    if (!aiMove) return;

    const { x: aiX, y: aiY } = aiMove;
    if (newBoard[aiX][aiY] !== null) return;

    const nextBoard = newBoard.map((row) => row.slice());
    nextBoard[aiY][aiX] = aiColor;
    setBoard(nextBoard);

    if (checkWin(nextBoard, aiX, aiY, isBlackTurn ? "white" : "black")) {
        setWinner(aiColor);
    } else {
        setIsBlackTurn(isBlackTurn);
    }
  };

  

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "center", marginTop: "2rem" }}>
        <div
          style={{
            position: "relative",
            width: `${(BOARD_SIZE - 1) * 40}px`,
            height: `${(BOARD_SIZE - 1) * 40}px`,
            backgroundColor: "#dca",
            border: "2px solid #333",
          }}
        >
          {/* グリッド線（SVG） */}
          <svg
            width={(BOARD_SIZE - 1) * 40}
            height={(BOARD_SIZE - 1) * 40}
            style={{ position: "absolute", top: 0, left: 0 }}
          >
            {/* 縦線 */}
            {Array(BOARD_SIZE)
              .fill(0)
              .map((_, i) => (
                <line
                  key={`v-${i}`}
                  x1={i * 40}
                  y1={0}
                  x2={i * 40}
                  y2={(BOARD_SIZE - 1) * 40}
                  stroke="#555"
                  strokeWidth="2"
                />
              ))}
            {/* 横線 */}
            {Array(BOARD_SIZE)
              .fill(0)
              .map((_, i) => (
                <line
                  key={`h-${i}`}
                  x1={0}
                  y1={i * 40}
                  x2={(BOARD_SIZE - 1) * 40}
                  y2={i * 40}
                  stroke="#555"
                  strokeWidth="2"
                />
              ))}
          </svg>

          {/* 交点クリックと石表示 */}
          {board.map((row, y) =>
            row.map((cell, x) => (
              <div
                key={`${x}-${y}`}
                onClick={() => handleClick(x, y)}
                style={{
                  position: "absolute",
                  top: `${y * 40}px`,
                  left: `${x * 40}px`,
                  width: "20px",
                  height: "20px",
                  transform: "translate(-50%, -50%)",
                  cursor: winner ? "default" : "pointer",
                }}
              >
                {cell && (
                  <div
                    style={{
                      width: "20px",
                      height: "20px",
                      borderRadius: "50%",
                      backgroundColor: cell,
                    }}
                  />
                )}
              </div>
            ))
          )}
        </div>
      </div>

      {/* 勝者表示 */}
      {winner && (
        <div
          style={{
            textAlign: "center",
            marginTop: "1.5rem",
            fontSize: "1.5rem",
            fontWeight: "bold",
          }}
        >
          {winner === "black" ? "● 黒の勝ち！" : "○ 白の勝ち！"}
        </div>
      )}
      <div style={{ textAlign: "center", marginTop: "1rem"}}>
        <button
         onClick={resetGame}
         style={{
            padding: "0.5rem 1rem",
            fontSize: "1rem",
            cursor: "pointer",
         }}
        >
            リセット
        </button>
      </div>
    </div>
  );
}
