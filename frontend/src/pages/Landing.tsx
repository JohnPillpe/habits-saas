import Navbar from "@/components/layout/Navbar"
import Hero from "@/components/landing/Hero"
import SearchTabs from "@/components/landing/SearchTabs"

export default function Landing() {
  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      <Hero />
      <SearchTabs />
    </div>
  )
}