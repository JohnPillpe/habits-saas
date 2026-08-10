import { createBrowserRouter } from "react-router-dom"

import Landing from "@/pages/Landing"
import JobDetails from "@/pages/JobDetails"
import Login from "@/pages/Login"
import Signup from "@/pages/Signup"
import Profile from "@/pages/Profile"

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Landing />,
  },
  {
    path: "/jobs/:id",
    element: <JobDetails />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "/signup",
    element: <Signup />,
  },
  {
    path: "/profile",
    element: <Profile />,
  },

])