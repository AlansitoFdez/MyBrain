import Link from "next/link"

export default function NotFound() {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center">
      <div className="text-center">
        <p className="text-8xl mb-4">🧠</p>
        <h1 className="text-2xl font-semibold text-slate-900 mb-2">
          Página no encontrada
        </h1>
        <p className="text-slate-400 text-sm mb-6">
          Esta página no existe en tu segundo cerebro
        </p>
        <Link
          href="/auth"
          className="px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white text-sm rounded-lg transition-colors"
        >
          Volver al inicio
        </Link>
      </div>
    </div>
  )
}