import {
    createContext,
    useContext,
    useState,
    ReactNode,
  } from "react"
  
  type Filters = {
    keyword: string
    country: string
    city: string
    published: string
    workType: string
  }
  
  type JobContextType = {
    jobs: any[]
    setJobs: React.Dispatch<React.SetStateAction<any[]>>
  
    filters: Filters
    setFilters: React.Dispatch<React.SetStateAction<Filters>>
  }
  
  const JobContext = createContext<JobContextType | null>(null)
  
  export function JobProvider({
    children,
  }: {
    children: ReactNode
  }) {
    const [jobs, setJobs] = useState<any[]>([])
  
    const [filters, setFilters] = useState<Filters>({
      keyword: "",
      country: "",
      city: "",
      published: "",
      workType: "",
    })
  
    return (
      <JobContext.Provider
        value={{
          jobs,
          setJobs,
          filters,
          setFilters,
        }}
      >
        {children}
      </JobContext.Provider>
    )
  }
  
  export function useJobs() {
    const context = useContext(JobContext)
  
    if (!context) {
      throw new Error("useJobs must be used inside JobProvider")
    }
  
    return context
  }