import { useState, ReactNode } from "react"

type Props = {
  title: string
  children: ReactNode
  defaultOpen?: boolean
}

export default function Accordion({
  title,
  children,
  defaultOpen = false,
}: Props) {

  const [open, setOpen] = useState(defaultOpen)

  return (
    <div className="rounded-xl border bg-white">

      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center justify-between p-5 text-left"
      >
        <span className="text-lg font-semibold">
          {title}
        </span>

        <span className="text-xl">
          {open ? "−" : "+"}
        </span>
      </button>

      {open && (
        <div className="border-t p-5">
          {children}
        </div>
      )}

    </div>
  )
}