import logo from './logo.svg';
import './App.css';
import Board from './components/Board';

function App() {
  return (
    <div style={{ textAlign: "center", marginTop: "2rem" }}>
      <h1>五目並べ</h1>
      <Board />
    </div>
  );
}

export default App;
