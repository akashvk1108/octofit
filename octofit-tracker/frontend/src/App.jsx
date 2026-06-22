import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'

function App() {
  return (
    <div className="container py-4">
      <nav className="mb-4 d-flex gap-2">
        <Link to="/" className="btn btn-primary">Home</Link>
        <Link to="/dashboard" className="btn btn-outline-primary">Dashboard</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </div>
  )
}

export default App
