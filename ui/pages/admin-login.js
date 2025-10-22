import { useState } from 'react'
import { useRouter } from 'next/router'

export default function AdminLogin(){
  const [email, setEmail] = useState('')
  const [err, setErr] = useState('')
  const router = useRouter()

  async function submit(e){
    e.preventDefault()
    setErr('')
    const res = await fetch('http://localhost:8000/admin-login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ email })
    })
    if(res.status === 303){
      router.push('/dashboard')
    } else {
      setErr('Not authorized')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <form onSubmit={submit} className="max-w-md w-full bg-white p-8 rounded-xl shadow">
        <h2 className="text-2xl font-semibold mb-4">Admin Login</h2>
        {err && <div className="text-red-600 mb-2">{err}</div>}
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder="Email" className="w-full p-3 border rounded mb-4" />
        <button className="w-full bg-indigo-600 text-white py-3 rounded">Login</button>
      </form>
    </div>
  )
}
