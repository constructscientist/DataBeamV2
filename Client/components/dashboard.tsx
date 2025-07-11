"use client"

import { useEffect, useState } from "react"
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "@/components/ui/chart"
import { fetchBidData, type BidData } from "@/services/api"

export default function Dashboard() {
  const [bidData, setBidData] = useState<BidData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadBidData() {
      try {
        const data = await fetchBidData()
        setBidData(data)
        setError(null)
      } catch (err) {
        setError("Failed to load bid data. Please try again later.")
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadBidData()
  }, [])

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-semibold mb-4">Bid Win Percentage Dashboard</h2>

      {loading ? (
        <div className="flex justify-center items-center h-[400px]">
          <div className="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent"></div>
        </div>
      ) : error ? (
        <div className="flex justify-center items-center h-[400px] text-red-500">{error}</div>
      ) : bidData.length === 0 ? (
        <div className="flex justify-center items-center h-[400px] text-gray-500">No bid data available</div>
      ) : (
        <div className="w-full h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={bidData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="winPercentage" fill="#8884d8" name="Win Percentage" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}

