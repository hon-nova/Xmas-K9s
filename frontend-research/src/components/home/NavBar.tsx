import  style  from "../../styles/style.module.css"
import { Link } from "react-router-dom"
import { useUserStore } from "../../stores/userStore"
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export function NavBar(){

   const { user,setUser, logout } = useUserStore()
   const navigate = useNavigate()
   function onLogout(){
      logout()
      navigate("/")
   }
   useEffect(()=>{
      fetchUser()     
   },[])
   async function fetchUser(){
      const res = await fetch(`${import.meta.env.VITE_AUTH_BACKEND_URL}/api/auth/me`,{
         method:"GET",
         credentials: "include"
      })
      const data = await res.json()
      console.log("Home: fetchUser data: ", data)
      setUser(data)
   }
   
   return (
  <div className={`${style.bgNavXmasBlue} ${style.bgXmasStars}`}>
    <div className="p-8">
      <div className="flex flex-row gap-4 align-center justify-end">
        {user && user?.username ? (         
            <button
              onClick={() => onLogout()}
              className={`${style.xmasButton}`}> Logout
            </button>         
        ) : (                  
            <Link to="/login" className={`${style.xmasButton}`}>
              Login
            </Link>         
        )}
        <Link to="/profile" className={`${style.xmasButton}`}>
          Profile
        </Link>
      </div>
    </div>
  </div>
)

}