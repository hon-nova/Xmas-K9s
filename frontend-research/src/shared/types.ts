export type Event = {
   id: string,
   ticketmasterId?: string,
   name: string,
   url: string,
   images: string[],
   startDateSales: string,
   endDateSales: string,
   startDateEvent: string,
   info: string,
   pleaseNote: string,
   venueName: string,
   venueCity: string,
   venueState: string,
   venueStateCode: string,
   venueCountry: string,
   venueAddress: string,
   venuePostalCode: string,
}

export type OrderedEvent = Event & {
   userId: string
   status: boolean
}

export type User = {
   id: string
   username: string 
   email:string
   password:string
   avatar:string
   role:string
   createdAt:string  
}
   
  
