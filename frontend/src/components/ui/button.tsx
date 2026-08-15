import * as React from "react"
import { cn } from "@/lib/utils"

function Button({
  className,
  ...props
}: React.ComponentProps<"button">) {
  return (
    <button
      className={cn(
        `
        rounded-lg
        border-2
        border-[#14151A]
        bg-[#2B4ACC]
        px-5
        py-2.5
        text-sm
        font-medium
        text-white
        shadow-[3px_3px_0_#14151A]
        transition-all
        duration-100
        hover:translate-x-[2px]
        hover:translate-y-[2px]
        hover:shadow-[1px_1px_0_#14151A]
        disabled:cursor-not-allowed
        disabled:opacity-60
        `,
        className
      )}
      {...props}
    />
  )
}

export { Button }