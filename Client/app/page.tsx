import Header from "@/components/header"
import ContractEstimationForm from "@/components/contract-estimation-form"
import Dashboard from "@/components/dashboard"
import OverallWinChart from "@/components/overall-win-chart"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto p-4">
        <h2 className="text-3xl font-bold mb-8">Contract Estimation and Dashboard</h2>

        {/* Form and Bar Chart */}
        <div className="grid gap-8 md:grid-cols-2 mb-8">
          <ContractEstimationForm />
          <Dashboard />
        </div>

        {/* Overall Win Chart */}
        <div className="max-w-xl mx-auto">
          <OverallWinChart />
        </div>
      </main>
    </div>
  )
}

