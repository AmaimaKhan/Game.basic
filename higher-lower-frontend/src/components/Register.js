import { useState } from 'react';
import axios from 'axios';

function Register() {
  const [form, setForm] = useState({ username: '', password: '' });

  const submit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/api/register/', form);
      // Redirect to home after success
      window.location.href = '/';
    } catch (err) {
  console.error(err.response || err.message || err);
  alert('Registration failed: ' + (err.response?.data?.error || 'Unknown error'));
}
    
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto' }}>
      <h2>Register</h2>
      <form onSubmit={submit}>
        <input
          type="text"
          placeholder="Username"
          value={form.username}
          onChange={(e) => setForm({ ...form, username: e.target.value })}
          required
          style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
          required
          style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 20px' }}>
          Register
        </button>
      </form>
      <p style={{ marginTop: '10px' }}>
        Already have an account? <a href="/login">Sign in</a>
      </p>
    </div>
  );
}

export default Register;
