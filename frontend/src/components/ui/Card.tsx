import { cn } from "@/lib/utils";

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
}

export default function Card({ children, className, hover = false }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border border-gray-800 bg-gray-900/50 p-6",
        hover && "transition-all hover:border-gray-700 hover:bg-gray-900",
        className
      )}
    >
      {children}
    </div>
  );
}
