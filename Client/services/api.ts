// services/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Types
export interface ContractFormData {
  contractSize: string
  distance: string
  projectSize: string
  projectType: string
  otherContractors: string
}

export interface BidData {
  name: string
  winPercentage: number
}

// API functions
export async function submitContractData(data: ContractFormData): Promise<any> {
  try {
    const response = await fetch(`${API_BASE_URL}/contracts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Error submitting contract data:", error)
    throw error
  }
}

export async function fetchBidData(): Promise<BidData[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/bids`)

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error("Error fetching bid data:", error)
    // Return sample data as fallback for demonstration
    return [
      { name: "Project A", winPercentage: 75 },
      { name: "Project B", winPercentage: 60 },
      { name: "Project C", winPercentage: 80 },
      { name: "Project D", winPercentage: 45 },
      { name: "Project E", winPercentage: 90 },
    ]
  }
}

