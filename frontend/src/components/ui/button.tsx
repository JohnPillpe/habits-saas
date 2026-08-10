import * as React from "react"
import { cn } from "@/lib/utils"

function Button({
  className,
  ...props
}: React.ComponentProps<"button">) {
  return (
    <button
      className={cn(
        "rounded-lg bg-black px-5 py-2 text-sm font-medium text-white transition hover:opacity-80",
        className
      )}
      {...props}
    />
  )
}

export { Button }