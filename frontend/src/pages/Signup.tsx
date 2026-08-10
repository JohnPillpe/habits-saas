import { useState } from "react"
import { useNavigate } from "react-router-dom"

const API = "http://127.0.0.1:8000"

export default function Signup() {
  const navigate = useNavigate()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault()

    try {
      const response = await fetch(`${API}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Registration failed")
      }

      alert("Account created. Please log in.")

      navigate("/login")
    } catch (error: any) {
      alert(error.message || "Registration failed")
    }
  }

  return (
    <div className="mx-auto mt-20 max-w-md">
      <h1 className="mb-8 text-3xl font-bold">
        Create Account
      </h1>

      <form
        onSubmit={handleSignup}
        className="space-y-4"
      >
        <input
          className="w-full rounded border p-3"
          placeholder="Email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          className="w-full rounded border p-3"
          placeholder="Password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          className="w-full rounded bg-black p-3 text-white"
        >
          Create Account
        </button>
      </form>

      <button
        onClick={() => navigate("/login")}
        className="mt-4 text-sm underline"
      >
        Already have an account? Login
      </button>
    </div>
  )
}