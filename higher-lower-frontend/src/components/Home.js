function Home() {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = '/register';
    return null;
  }

  const logout = () => {
    localStorage.removeItem('token');
    window.location.href = '/register';
  };

  return (
    <div>
      <button style={{ float: 'right' }} onClick={logout}>Logout</button>
      <h1>Higher & Lower</h1>
      <div style={{ padding: '20px', border: '1px solid black' }}>
        <p>This is your game block</p>
      </div>
    </div>
  );
}

export default Home;
