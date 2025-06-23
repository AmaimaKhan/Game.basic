import { useState } from 'react';
import axios from 'axios';

function Login() {
  const [form, setForm] = useState({ username: '', password: '' });

  const submit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/token/', form);
      localStorage.setItem('token', res.data.access);
      window.location.href = '/';
    } catch (err) {
      alert("Login failed. Check credentials.");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={submit}>
        <input placeholder="Username" onChange={e => setForm({...form, username: e.target.value})} />
        <input type="password" placeholder="Password" onChange={e => setForm({...form, password: e.target.value})} />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;
