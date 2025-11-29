import { Events } from "./Events"
import { Footer } from "./Footer"
import { NavBar } from "./NavBar"
import { useUserStore } from "../../stores/userStore"
import { useEffect } from "react"
import style from "../../styles/style.module.css"
import { ChatBot } from "./ChatBot"

export function Home(){

   const { user,setUser } = useUserStore()
   console.log("Home: user from store: ", user)   
   
   useEffect(()=>{
      fetchUser()     
   },[])
   async function fetchUser(){
      const res = await fetch(`${import.meta.env.VITE_AUTH_BACKEND_URL}/api/auth/me`,{
         method:"GET",
         credentials: "include"
      })
      const data = await res.json()
      setUser(data)
   }
   return (
      <div className="">
         <NavBar />
         <div className="mx-3">
            <h1>Hi {user?.username ? <span className={`${style.textXmasBlue}`}>{user.username}</span> : "Guest"}, <span className="flex text-center justify-center text-lg font-semibold">Welcome to Xmas-K9s Project!</span></h1>
            <main className="flex-1 p-6 pb-32">       
               <Events/>
               <ChatBot />
            </main>             
         </div>
         <Footer />
      </div>
   )
}