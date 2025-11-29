import { useUserStore } from "../../stores/userStore"
import { useState, useEffect } from "react"
import type { Event } from "../../shared/types"
import style from "../../styles/style.module.css"
import { events_format, date_format} from "../../utils/helpers"
import { ProfileNav } from "./ProfileNav"

export function Profile() {

   const { user,setUser } = useUserStore()
   console.log("Profile: user from store: ", user)
   const [myEvents, setMyEvents] = useState<Event[]>([])
   
   console.log("playground PROFILE: myEvents: ", myEvents)
   
      async function fetchUser(){
      const res = await fetch(`${import.meta.env.VITE_PROFILE_BACKEND_URL}/api/profile/auth`,{
         method:"GET",
         credentials: "include"
      })
      const data = await res.json()
      console.log("PROFILE: fetchUser: ", data)
      setUser(data)
   }
   useEffect(()=>{
      fetchUser()     
   },[])

   async function fetchUserEvents(){
      const res = await fetch(`${import.meta.env.VITE_PROFILE_BACKEND_URL}/api/profile/events`,{
         method:"GET",
         credentials: "include"
      })
      const data = await res.json()
      console.log("PROFILE: events: ", data.events)
      setMyEvents(data.events)
   }
   useEffect(()=>{
      fetchUserEvents()
   },[])


   return(
      <div className="rounded-xl shadow-lg space-y-6">
      {/* Profile Header */}
      <div className="main">
         <div className="nav"><ProfileNav /></div>
         <div className="main-content">
            {user && user.username ? 
            (<div>
               <div className="text-center">
                  <h1 className="text-3xl textXmasBlue mb-2">🎄 My Christmas Profile</h1>
                  <p className="text-gray-600">Welcome back, festive friend!</p>
               </div>

         {/* Event List */}
               <div className="text-center my-2">
                  <h2 className="text-2xl textXmasBlue mb-4">🎅 Upcoming Events 🦌</h2>
                  <ul className="divide-y divide-gray-200">
                     {myEvents && myEvents.length>0 && events_format(myEvents).map((event,index) => (
                        <li key={event?.id} className="py-3">
                        <p className={`${style.textXmasBlue} font-semibold text-lg cursor-pointer italic`}>{index+1}. <span className={`${style.textXmasBlue} font-semibold text-lg cursor-pointer italic underline`}>{event?.name} (on {date_format(event?.startDateEvent)})</span></p>
                        <p className="py-4 font-bold">TicketMaster ID: {event?.ticketmasterId}</p>
                        <p className="text-sm text-gray-500">
                           Venue: {event.venueName} — {event.venueAddress}, {event.venueCity}, {event.venueState}, {event.venueCountry}
                        </p>
                        </li>
                     ))}
                  </ul>
               </div>
            </div>) : 
            (<div className="flex justify-center my-5 text-lg align-items-center text-center"><p>You're not logged in.</p></div>)}
         </div>
      </div>
        
    </div>
   )
}