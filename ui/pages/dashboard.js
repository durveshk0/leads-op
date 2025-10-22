import { useEffect, useState } from 'react'
import LeadRow from '../components/LeadRow'

function prioritize(leads){
  return leads.sort((a,b)=>{
    const order = { 'Hot': 3, 'Warm': 2, 'Cold': 1 }
    return (order[b.classification] || 0) - (order[a.classification] || 0)
  })
}

export default function Dashboard(){
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    fetch('http://localhost:8000/api/leads')
      .then(r=>r.json())
      .then(data=>{
        const p = prioritize(data)
        // transform back to array-like shape for LeadRow (compat with backend)
        setLeads(p.map(l=>[l.id, l.name, l.email, l.message, l.score, l.classification, null, l.created_at]))
      })
      .catch(()=>{})
      .finally(()=>setLoading(false))
  },[])

  return (
    <div className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
        <div className="bg-white rounded shadow p-4">
          {loading ? <div>Loading...</div> : (
            <table className="w-full text-left">
              <thead>
                <tr className="border-b"><th className="px-4 py-2">Name</th><th className="px-4 py-2">Email</th><th className="px-4 py-2">Score</th><th className="px-4 py-2">Classification</th><th className="px-4 py-2">Created</th></tr>
              </thead>
              <tbody>
                {leads.map((l,idx)=><LeadRow key={idx} lead={l} />)}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
