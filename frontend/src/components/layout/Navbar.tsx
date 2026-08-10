import { useNavigate } from "react-router-dom"

export default function Navbar() {
  const navigate = useNavigate()

  const token = localStorage.getItem("token")

  function handleLogout() {
    localStorage.removeItem("token")
    navigate("/")
  }

  return (
    <nav className="flex items-center justify-between px-8 py-6">
      <div className="text-xl font-semibold">
        MatchAI
      </div>

      <div className="flex gap-4">
      {token ? (
        <>
          <button
            onClick={() => navigate("/profile")}
            className="text-sm"
          >
            Profile
          </button>

          <button
            onClick={handleLogout}
            className="text-sm"
          >
            Logout
          </button>
        </>
      ) : (
          <>
            <button
              onClick={() => navigate("/login")}
              className="text-sm"
            >
              Login
            </button>

            <button
              onClick={() => navigate("/signup")}
              className="rounded-full bg-black px-5 py-2 text-sm text-white"
            >
              Sign Up
            </button>
          </>
        )}
      </div>
    </nav>
  )
}