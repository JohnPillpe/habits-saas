import { useState } from "react"
import { useNavigate, useLocation } from "react-router-dom"

import { login } from "@/services/auth"

export default function Login() {

  const navigate = useNavigate()
  const location = useLocation()

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  async function handleLogin(e: React.FormEvent) {

    e.preventDefault()

    try {

      const data = await login(email, password)

      localStorage.setItem(
        "token",
        data.access_token,
      )

      navigate(location.state?.from || "/")

    } catch {

      alert("Invalid credentials")

    }

  }

  return (

    <div className="mx-auto mt-20 max-w-md">

      <h1 className="mb-8 text-3xl font-bold">
        Login
      </h1>

      <form
        onSubmit={handleLogin}
        className="space-y-4"
      >

        <input
          className="w-full rounded border p-3"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="w-full rounded border p-3"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="w-full rounded bg-black p-3 text-white"
        >
          Login
        </button>

      </form>

    </div>

  )

}