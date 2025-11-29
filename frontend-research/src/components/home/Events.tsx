import type { Event } from "../../shared/types"
import {  useEffect, useState } from 'react'
import { useEventStore } from './../../stores/eventsStore'
import { useUserStore } from "../../stores/userStore"
import { events_format } from '../../utils/helpers'
import { EventCard } from "./Event"


export function Events(){

   const { fetchEvents, events } = useEventStore()
   const { user, setUser } = useUserStore()
   const [msg, setMsg ] =  useState("")
   
   console.log(`be adding event msg: `, msg)  
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
   const states_set = new Set(events.map((event:any) => event.venue_state))
   const states_list = Array.from(states_set)
   useEffect(()=>{
      fetchEvents()
   },[])
      useEffect(()=>{
      fetchUser()     
   },[])
   async function fetchUser(){
      const res = await fetch(`${import.meta.env.VITE_AUTH_BACKEND_URL}/api/bot/me`,{
         method:"GET",
         credentials: "include"
      })
      const data = await res.json()
      setUser(data)
   }
   const BOT_URL = import.meta.env.VITE_BOT_BACKEND_URL
   console.log(`user from bot at Events component: `, user)

   async function addToUserAccount(ticketId:string){
      alert(`Adding event with ticket ID: ${ticketId} to your account.`)
      console.log(`Adding event with ticketId: ${ticketId} to user account`)
      if (!user?.id){
         alert("Please log in to add event to your account.")
      }
      const res = await fetch(`${BOT_URL}/api/bot/events/add`,{
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',       
         },
         credentials:"include",
         body: JSON.stringify({ ticketmasterId: ticketId }),    
      })
      const data = await res.json()
      const msg_be = data.message
      if (msg_be){
         setMsg(msg_be)
      } else {
         setMsg("Something went wrong. Please try again. ")
      }
     
   }
   return (
      <div className="">
         {msg && <p className="mb-4 italic text-green-600 font-bold">{msg}</p>}
         <div>
            {states_list.map((state) => (
               <div key={state}>
                  <input type="checkbox"  name={state} value={state} checked/>
                  <label className="ml-2">{state || "N/A"}</label>
               </div>
            ))}
         </div>
         <p className="italic"><span className="font-bold">Events</span> ({events.length})</p>
         <div className="events">
            {events && events.length >0 && events_format(events).map((xmas_event:Event)=>(
           <EventCard 
            key={xmas_event.id} event={xmas_event }
            addToAccount={addToUserAccount} />
        ))}
         </div>
      </div>

   )
}