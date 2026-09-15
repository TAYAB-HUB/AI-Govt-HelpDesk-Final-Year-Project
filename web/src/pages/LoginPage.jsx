import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import toast from 'react-hot-toast';
import { ArrowRight, Eye, EyeOff, LockKeyhole, ShieldCheck, Sparkles } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await login(email, password);
      toast.success('Login successful!');
      navigate('/');
    } catch (error) {
      toast.error(error.response?.data?.detail || error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page min-h-screen p-5 sm:p-8">
      <div className="login-orb login-orb-one" />
      <div className="login-orb login-orb-two" />
      <section className="login-shell">
        <aside className="login-aside">
          <div className="brand-mark"><ShieldCheck aria-hidden="true" /></div>
          <p className="login-kicker"><Sparkles size={15} aria-hidden="true" /> Digital public service</p>
          <h1>Help that moves public service forward.</h1>
          <p className="login-aside-copy">A secure workspace for employees, officers, and department administrators.</p>
          <div className="login-trust"><LockKeyhole size={18} aria-hidden="true" /><span>Protected access for authorised personnel</span></div>
        </aside>

        <div className="login-card">
          <div className="login-mobile-mark"><ShieldCheck aria-hidden="true" /></div>
          <div className="login-heading">
            <p className="login-eyebrow">Welcome back</p>
            <h2>Sign in to Helpdesk</h2>
            <p>Use your official account to continue.</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <label>
              <span>Email address</span>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@department.gov.in"
                autoComplete="email"
                required
              />
            </label>

            <label>
              <span>Password</span>
              <div className="password-field">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((visible) => !visible)}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                  title={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff size={19} /> : <Eye size={19} />}
                  <span>{showPassword ? 'Hide' : 'Show'}</span>
                </button>
              </div>
            </label>

            <button type="submit" disabled={loading} className="login-submit">
              <span>{loading ? 'Signing in…' : 'Sign in securely'}</span>
              {!loading && <ArrowRight size={19} aria-hidden="true" />}
            </button>
          </form>

          <p className="login-register">New to the portal? <Link to="/register">Create an account</Link></p>
        </div>
      </section>
    </main>
  );
}
