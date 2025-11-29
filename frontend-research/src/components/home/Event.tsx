import type { Event } from "../../shared/types"
import { Link } from "react-router-dom"
import style from '../../styles/style.module.css'
import { date_format } from "../../utils/helpers"

type EventProps = {
   event: Event,
   addToAccount: (ticketId:string) => Promise<void>
}

export function EventCard({ event, addToAccount }: EventProps){
  
   return (
      <div className={`${style.card} grid grid-cols-12 border mb-4 p-4`}>
         <div className={`${style.cardLeft} col-span-4 rounded`}>
            <h2 className={`${style.textXmasBlue} text-lg font-semibold`}>{event?.name}</h2>
           
            <p className="text-lm text-gray-600">{event.venueCity} {event.venueState}, {event.venueCountry}</p>
            <p>Venue: {event.venueName} - {event.venueAddress} {event.venuePostalCode} </p>
            <p className="text-lm font-bold">Start: {date_format(event.startDateEvent)}</p>
            <p className="font-bold text-sm py-2">Ticket ID: <span className="italic text-gray-500">{event?.ticketmasterId}</span></p>
            {event.info && <p className="text-xs italic mt-2">{event.info.slice(0, 200)}</p>}
            <Link
               to={event.url}
               target="_blank"
               rel="noopener noreferrer"
               className="block my-3 text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
               Visit →
            </Link>
            <button     
               onClick={() =>{if (event.ticketmasterId){
                  addToAccount(event.ticketmasterId)
               }}}
               className={`${style.bgNavXmasBlue} font-bold text-lg rounded-lg p-4 cursor-pointer hover:text-green-700`}>Join Event</button>
         </div>
         <div className={`${style.cardRight} flex justify-center col-span-8 border border-gray-100 bg-neutral-100 p-8`}>
            {event.images[0] && 
            <img 
               className="w-200 h-80 object-cover rounded-lg shadow-md"
               src={event.images[1]} alt="xmas" />}           
         </div>
      </div>
   )
}