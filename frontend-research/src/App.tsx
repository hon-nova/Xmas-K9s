
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
// import './App.css'
// import { ChatBot as Bot } from './components/ChatBot'
import { Home } from './components/home/Home'
import { Login } from './components/auth/Login'
import { Register } from './components/auth/Register'
import { Profile } from './components/profile/Profile'

function App() { 

  return (
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
         
        </Routes>
      </Router>
  )
}

export default App
