import { useEffect, useState } from 'react';
import axios from 'axios';

function Home() {
  const token = localStorage.getItem('token');
  const [card, setCard] = useState(null);
  const [result, setResult] = useState('');
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  useEffect(() => {
    if (!token) {
      window.location.href = '/register';
      return;
    }

    // Start game
    axios.get('http://127.0.0.1:8000/start_game/', {
      withCredentials: true
    }).then(res => {
      setCard(res.data.card);
    }).catch(err => {
      console.error('Start game failed:', err);
    });
  }, []);

  const handleGuess = (guess) => {
    axios.post('http://127.0.0.1:8000/guess_card/', { guess }, {
      withCredentials: true
    }).then(res => {
      setResult(res.data.result);
      setCard(res.data.next_card);
      setScore(res.data.score);
      setGameOver(res.data.game_over);
      if (res.data.game_over) {
        alert(`Game Over! Your score: ${res.data.score}`);
      }
    }).catch(err => {
      console.error('Guess failed:', err);
    });
  };

  const logout = () => {
    localStorage.removeItem('token');
    window.location.href = '/register';
  };

  return (
    <div>
      <button style={{ float: 'right' }} onClick={logout}>Logout</button>
      <h1>Higher & Lower</h1>
      <div style={{ padding: '20px', border: '1px solid black', textAlign: 'center' }}>
        <p>Current Card: {card}</p>
        {!gameOver && (
          <>
            <button onClick={() => handleGuess('higher')}>Higher</button>
            <button onClick={() => handleGuess('lower')}>Lower</button>
          </>
        )}
        {result && <p>{result}</p>}
        <p>Score: {score}</p>
      </div>
    </div>
  );
}

export default Home;
