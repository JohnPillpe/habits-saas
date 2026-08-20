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
      "Content-Type":
        "application/x-www-form-urlencoded",
    },
    body: form,
  })

  if (!response.ok) {
    let message = "Invalid credentials"

    try {
      const data = await response.json()

      if (data.detail) {
        message = data.detail
      }
    } catch {
      // Keep default message.
    }

    throw new Error(message)
  }

  return response.json()
}


/* ============================================================
   FORGOT PASSWORD
   ============================================================ */

export async function forgotPassword(
  email: string,
) {
  const response = await fetch(
    `${API}/forgot-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email.trim(),
      }),
    },
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Could not send password reset link.",
    )
  }

  return data
}


/* ============================================================
   RESET PASSWORD
   ============================================================ */

export async function resetPassword(
  token: string,
  password: string,
) {
  const response = await fetch(
    `${API}/reset-password`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token,
        password,
      }),
    },
  )

  const data = await response.json()

  if (!response.ok) {
    throw new Error(
      data.detail ||
        "Could not reset password.",
    )
  }

  return data
}

/* ============================================================
   CHANGE PASSWORD
   ============================================================ */

   export async function changePassword(
    currentPassword: string,
    newPassword: string,
  ) {
    const token = localStorage.getItem("token")
  
    if (!token) {
      throw new Error("You must be logged in.")
    }
  
    const response = await fetch(
      `${API}/change-password`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      },
    )
  
    const data = await response.json()
  
    if (!response.ok) {
      throw new Error(
        data.detail ||
          "Could not change password.",
      )
    }
  
    return data
  }