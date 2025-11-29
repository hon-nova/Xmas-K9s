import  style  from "../../styles/style.module.css"
import { Link } from "react-router-dom"
import { useUserStore } from "../../stores/userStore"
// import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export function ProfileNav(){

   const { user,logout } = useUserStore()
   const navigate = useNavigate()
   function onLogout(){
      logout()
      navigate("/")
   } 
   
   return (
  <div className={`${style.bgNavXmasBlue} ${style.bgXmasStars}`}>
    <div className="p-8">
      <div className="flex flex-row gap-4 align-center justify-between">
          <Link to="/" className={`${style.xmasButton}`}>
          Home
         </Link>
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
       
      </div>
    </div>
  </div>
)

}