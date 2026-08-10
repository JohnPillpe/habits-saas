import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { RouterProvider } from "react-router-dom"

import "./index.css"

import { router } from "./router"
import { JobProvider } from "./context/JobContext"

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <JobProvider>
      <RouterProvider router={router} />
    </JobProvider>
  </StrictMode>,
)