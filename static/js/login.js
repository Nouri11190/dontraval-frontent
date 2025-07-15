document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const res = await fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (res.ok && data.access_token) {
    localStorage.setItem('token', data.access_token);
    window.location.href = '/dashboard';
  } else {
    alert(data.message || 'Login failed');
  }
});
