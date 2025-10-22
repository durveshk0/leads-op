export default function LeadRow({lead}){
  const color = lead[5] === 'Hot' ? 'bg-red-100' : lead[5] === 'Warm' ? 'bg-yellow-100' : 'bg-green-100'
  return (
    <tr className={`border-b ${color}`}>
      <td className="px-4 py-2">{lead[1]}</td>
      <td className="px-4 py-2">{lead[2]}</td>
      <td className="px-4 py-2">{lead[4]}</td>
      <td className="px-4 py-2">{lead[5]}</td>
      <td className="px-4 py-2">{lead[7]}</td>
    </tr>
  )
}
