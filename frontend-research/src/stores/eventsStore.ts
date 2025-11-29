import { create } from "zustand"
// import { persist, createJSONStorage } from "zustand/middleware"
import type { Event } from "../shared/types"

type EventState = {
  events: Event[]
  loading: boolean
  error: string | null 
  fetchEvents: () => Promise<void>  
//   addEvent: (id:string)=>void

}
const BOT_BACKEND_URL= import.meta.env.VITE_BOT_BACKEND_URL
console.log(`EVENTS_BACKEND_URL: ${BOT_BACKEND_URL}`)
export const useEventStore = create<EventState>(  
    (set) => ({
      events: [],
      loading: false,
      error: null,        
      fetchEvents: async () => {
                 
         set({ loading: true, error: null })
         try {           
            const res = await fetch(`${BOT_BACKEND_URL}/api/bot/events`)
            const data = await res.json()
            // console.log("useEventStore: fetchEvents data: ", data.events)
            set({ 
               events: data.events,              
             })
         } catch (err) {
            if(err instanceof Error){
               set({ error: err.message })
            }
         
        } finally {
          set({ loading: false })
        }
      },
      
    })
    
  )