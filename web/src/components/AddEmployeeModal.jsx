import { useEffect, useState } from 'react';
import { Building2, UserPlus, X } from 'lucide-react';
import toast from 'react-hot-toast';
import api, { createEmployee } from '../services/api';
import { useAuth } from '../context/AuthContext';

const canChooseDepartment = (role) => role === 'SuperAdmin';

export default function AddEmployeeModal({ open, onClose }) {
  const { user } = useAuth();
  const [departments, setDepartments] = useState([]);
  const [submitting, setSubmitting] = useState(false);
  const [form, setForm] = useState({ full_name: '', email: '', employee_id: '', password: '', department_id: '' });

  useEffect(() => {
    if (!open || !canChooseDepartment(user?.role)) return;
    api.get('/departments/').then(({ data }) => setDepartments(data)).catch(() => {
      toast.error('Unable to load departments');
    });
  }, [open, user?.role]);

  useEffect(() => {
    if (!open) return;
    setForm({ full_name: '', email: '', employee_id: '', password: '', department_id: user?.role === 'SuperAdmin' ? '' : String(user?.department_id || '') });
  }, [open, user]);

  if (!open) return null;

  const update = (event) => setForm((current) => ({ ...current, [event.target.name]: event.target.value }));

  async function submit(event) {
    event.preventDefault();
    setSubmitting(true);
    try {
      await createEmployee({
        ...form,
        role: 'Employee',
        employee_id: form.employee_id || null,
        department_id: Number(form.department_id),
      });
      toast.success('Employee account created successfully');
      onClose();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Could not create employee account');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 p-4" role="dialog" aria-modal="true" aria-labelledby="add-employee-title">
      <div className="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl">
        <div className="flex items-start justify-between border-b border-slate-100 px-6 py-5">
          <div>
            <div className="mb-2 inline-flex rounded-lg bg-blue-50 p-2 text-blue-700"><UserPlus size={20} /></div>
            <h2 id="add-employee-title" className="text-xl font-bold text-slate-900">Add employee</h2>
            <p className="mt-1 text-sm text-slate-500">Create an Employee account with secure sign-in access.</p>
          </div>
          <button type="button" onClick={onClose} aria-label="Close" className="rounded-lg p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-800"><X size={20} /></button>
        </div>
        <form onSubmit={submit} className="space-y-4 px-6 py-5">
          <div className="grid gap-4 sm:grid-cols-2">
            <label className="text-sm font-medium text-slate-700">Full name
              <input required name="full_name" value={form.full_name} onChange={update} className="mt-1.5 w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" placeholder="Employee name" />
            </label>
            <label className="text-sm font-medium text-slate-700">Employee ID <span className="font-normal text-slate-400">(optional)</span>
              <input name="employee_id" value={form.employee_id} onChange={update} className="mt-1.5 w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" placeholder="EMP-1001" />
            </label>
          </div>
          <label className="block text-sm font-medium text-slate-700">Official email
            <input required type="email" name="email" value={form.email} onChange={update} className="mt-1.5 w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" placeholder="name@department.gov.in" />
          </label>
          <label className="block text-sm font-medium text-slate-700">Temporary password
            <input required minLength="8" type="password" name="password" value={form.password} onChange={update} className="mt-1.5 w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" placeholder="At least 8 characters" />
          </label>
          {canChooseDepartment(user?.role) ? (
            <label className="block text-sm font-medium text-slate-700">Department
              <select required name="department_id" value={form.department_id} onChange={update} className="mt-1.5 w-full rounded-lg border border-slate-300 px-3 py-2.5 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100">
                <option value="">Select department</option>
                {departments.map((department) => <option value={department.id} key={department.id}>{department.name}</option>)}
              </select>
            </label>
          ) : (
            <div className="flex items-center gap-2 rounded-lg bg-slate-50 px-3 py-3 text-sm text-slate-600"><Building2 size={17} className="text-blue-600" /> Employee will be added to your department.</div>
          )}
          <div className="flex justify-end gap-3 border-t border-slate-100 pt-5">
            <button type="button" onClick={onClose} className="rounded-lg px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button>
            <button disabled={submitting} className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"><UserPlus size={17} />{submitting ? 'Creating…' : 'Create employee'}</button>
          </div>
        </form>
      </div>
    </div>
  );
}
