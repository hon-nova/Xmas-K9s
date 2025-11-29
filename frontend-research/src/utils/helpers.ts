import type { Event } from "../shared/types"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function events_format(events:any[]){
   // eslint-disable-next-line @typescript-eslint/no-explicit-any
   const events_return = events.map((e: any)=>{
      return {
         id: e.id,
         ticketmasterId: e.ticketmaster_id,
         name: e.name,
         url: e.url,
         images: e.images,
         startDateSales: e.start_date_sales,
         endDateSales: e.end_date_sales,
         startDateEvent: e.start_date_event,
         info: e.info,
         pleaseNote: e.please_note, 
         venueName: e.venue_name,
         venueCity: e.venue_city,
         venueCountry: e.venue_country,
         venueState: e.venue_state,
         venueStateCode: e.venue_state_code,
         venueAddress: e.venue_address,
         venuePostalCode: e.venue_postal_code,

      }
   })
   return events_return as Event[]
}
export function date_format(dateString: string){
   
   const dt = new Date(dateString)
   const formatted = dt.toLocaleDateString('en-CA', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
   })
   // "Dec 24, 2025"
   // console.log(formatted);
      return formatted
   }
   // test
   // console.log(date_format("2025-12-24T00:00:00"));
