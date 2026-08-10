const API = "http://127.0.0.1:8000"

export async function login(
  email: string,
  password: string,
) {
  const form = new URLSearchParams()

  form.append("username", email)
  form.append("password", password)

  const response = await fetch(`${API}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: form,
  })

  if (!response.ok) {
    throw new Error("Invalid credentials")
  }

  return response.json()
}