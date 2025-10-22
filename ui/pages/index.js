import Head from 'next/head'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <Head>
        <title>GSBG - Home</title>
      </Head>
      <div className="max-w-3xl w-full bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-3xl font-semibold mb-4">Welcome to GSBG Lead Portal</h1>
        <p className="text-gray-600 mb-6">Modern dashboard for lead intelligence and prioritization.</p>
        <div className="flex gap-4">
          <Link href="/admin-login"><a className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700">Admin Login</a></Link>
          <a className="px-4 py-2 bg-gray-200 rounded text-gray-700">Public Form (existing)</a>
        </div>
      </div>
    </div>
  )
}
