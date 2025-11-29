import { useState } from 'react'
import { useNavigate } from "react-router-dom" 
import style from '../../styles/style.module.css'


type Msg = {
   error: string,
   success: string
}
export function Login() {
   const [email, setEmail] = useState('')
   const [password, setPassword] = useState('')
   const navigate = useNavigate()

   const [msg, setMsg] = useState<Msg>({error: '',success:''})
   
   const AUTH_URL =import.meta.env.VITE_AUTH_BACKEND_URL   
   console.log(`AUTH_URL:  ${AUTH_URL}`)
  

   const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault()
      
      console.log('Email:', email)
      console.log('Password:', password)
      
      async function loginUser(){
         const res = await fetch(`${AUTH_URL}/api/auth/login`,{
            method:"POST",
            headers:{
               "Content-Type":"application/json",               
            },
            body: JSON.stringify({email,password}),
            credentials: "include"
         })
      
         const result = await res.json()
         console.log(`IMPORTANT: result /login: `)
         console.log(result)

         if (result?.message!=="Login Success"){
            console.log(result.message)
            setMsg((pre:Msg)=>({...pre,error: result?.detail}))         
            setTimeout(()=>{
               setMsg((pre:Msg)=>({...pre,error: ""}))
            },4000)
            return; 
            }              
         
         setMsg((pre:Msg)=>({...pre, success:result?.message}))         
         setTimeout(()=>{
            navigate('/')
         },2000)  
      }
      loginUser()
      setEmail("")
      setPassword("")
   }

  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-200">
      <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
        <h2 className={`${style.textXmasBlue} text-2xl font-bold mb-6 text-center curo`}>Login</h2>
        <div className='h-[50px]'>
            {msg && msg?.error && (
            <div className="bg-red-100 text-red-700 p-2 rounded mb-4 text-center">{msg.error}</div>
         )}
            {msg && msg?.success && (
            <div className="bg-green-100 text-green-700 p-2 rounded mb-4 text-center">{msg.success}</div>
         )}
        </div>        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-neutral-700 mb-1">
              Email Address
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-4 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-neutral-700 mb-1">
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-4 py-2 border border-neutral-300 rounded-md focus:outline-none focus:ring-2 focus:ring-amber-600"
              required
            />
          </div>
          <button
            type="submit"
            className={`${style.bgXmasBlue} w-full text-whitesmoke py-2 rounded font-semibold hover:bg-amber-500 transition-colors cursor-pointer`}
          >Sign In</button>
        </form>
        <p className="mt-4 text-center text-neutral-500 text-sm">
          Don't have an account? <a href="/register" className={`${style.textXmasBlue} font-bold hover:underline`}>Sign Up</a>
        </p>
       
      </div>
    </div>
  )
}