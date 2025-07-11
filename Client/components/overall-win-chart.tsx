"use client"

import { useEffect, useState } from "react"
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts"
import { fetchBidData, type BidData } from "@/services/api"

export default function OverallWinChart() {
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

  // Calculate overall win percentage
  const calculateOverallPercentage = (data: BidData[]): number => {
    if (data.length === 0) return 0
    const sum = data.reduce((acc, item) => acc + item.winPercentage, 0)
    return Math.round(sum / data.length)
  }

  const overallPercentage = calculateOverallPercentage(bidData)

  // Data for the donut chart
  const chartData = [
    { name: "Win Rate", value: overallPercentage },
    { name: "Remaining", value: 100 - overallPercentage },
  ]

  // Colors for the chart segments
  const COLORS = ["#8884d8", "#f3f4f6"]

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-semibold mb-4">Overall Bid Win Outlook</h2>

      {loading ? (
        <div className="flex justify-center items-center h-[300px]">
          <div className="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent"></div>
        </div>
      ) : error ? (
        <div className="flex justify-center items-center h-[300px] text-red-500">{error}</div>
      ) : bidData.length === 0 ? (
        <div className="flex justify-center items-center h-[300px] text-gray-500">No bid data available</div>
      ) : (
        <div className="relative h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={0}
                dataKey="value"
                startAngle={90}
                endAngle={-270}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value}%`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
            <div className="text-3xl font-bold">{overallPercentage}%</div>
            <div className="text-sm text-gray-500">Win Rate</div>
          </div>
        </div>
      )}
    </div>
  )
}

