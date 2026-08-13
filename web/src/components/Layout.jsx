import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, MessageSquare, Ticket, Home, UserPlus, ShieldCheck } from 'lucide-react';
import AddEmployeeModal from './AddEmployeeModal';

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isEmployeeModalOpen, setEmployeeModalOpen] = useState(false);
  const canAddEmployee = ['SuperAdmin', 'DeptAdmin', 'Officer'].includes(user?.role);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { icon: Home, label: 'Dashboard', path: '/', roles: ['Employee', 'Officer', 'DeptAdmin', 'SuperAdmin'] },
    { icon: MessageSquare, label: 'Chat', path: '/chat', roles: ['Employee', 'Officer', 'DeptAdmin', 'SuperAdmin'] },
    { icon: Ticket, label: 'Tickets', path: '/tickets', roles: ['Employee', 'Officer', 'DeptAdmin', 'SuperAdmin'] },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Top Navigation */}
      <nav className="sticky top-0 z-40 border-b border-slate-200 bg-white/95 shadow-sm backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex h-[72px] justify-between">
            <div className="flex items-center">
              <Link to="/" className="flex items-center gap-3">
                <span className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-blue-700 to-indigo-800 text-white shadow-md"><ShieldCheck size={22} /></span>
                <span><span className="block text-base font-bold tracking-tight text-slate-900">AI Govt Helpdesk</span><span className="block text-[10px] font-semibold uppercase tracking-[0.16em] text-blue-700">Service portal</span></span>
              </Link>
              <div className="hidden md:flex ml-10 items-center gap-1">
                {navItems.filter(item => item.roles.includes(user.role)).map(item => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className="flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-blue-700"
                  >
                    <item.icon size={18} />
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>

            <div className="flex items-center gap-2 sm:gap-4">
              {canAddEmployee && (
                <button onClick={() => setEmployeeModalOpen(true)} className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
                  <UserPlus size={17} />
                  <span className="hidden sm:inline">Add employee</span>
                </button>
              )}
              <div className="hidden text-right sm:block">
                <p className="text-sm font-semibold text-slate-800">{user.full_name}</p>
                <p className="text-xs text-slate-500">{user.role === 'Officer' ? 'Officer (HR)' : user.role}</p>
              </div>
              <button
                onClick={handleLogout}
                title="Logout"
                className="flex items-center gap-2 rounded-lg p-2.5 text-slate-500 transition hover:bg-slate-100 hover:text-slate-800"
              >
                <LogOut size={18} />
                <span className="hidden lg:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="py-8 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
      <AddEmployeeModal open={isEmployeeModalOpen} onClose={() => setEmployeeModalOpen(false)} />
    </div>
  );
}
