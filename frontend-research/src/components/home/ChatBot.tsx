import { useState, useEffect, useRef } from "react"
import { useUserStore } from "../../stores/userStore"
import santaIcon from "../../assets/santa.png"
import style from "../../styles/style.module.css"

export function ChatBot() {

   const BOT_URL = import.meta.env.VITE_BOT_BACKEND_URL
   const [uMsg, setUMsg] = useState("")
   const [open, setOpen] = useState(false)
   const [isIconOpen,setIsIconOpen] = useState(true)
   
   // eslint-disable-next-line @typescript-eslint/no-explicit-any
   const [convo, setConvo] = useState<any[]>([])
   const { user, setUser } = useUserStore()
   console.log(`User in ChatBot from AUTH:`, user)
   console.log("convo:", convo)   

   async function fetchUser(){
      const res = await fetch(`${import.meta.env.VITE_BOT_BACKEND_URL}/api/bot/me`,{
         method:"GET",
         credentials: "include"
      })
      const data = await res.json()
      // console.log("Home: fetchUser data: ", data)
      setUser(data)
   }
   useEffect(()=>{
      fetchUser()     
   },[])

    function handleOpenStatus(){
      setOpen(!open)
      setIsIconOpen(!isIconOpen)
   }

  // 🧠 Persistent chat session
  const chatSessionIdRef = useRef<string>(crypto.randomUUID())

   async function sendToBot(){   
         
      if (inputRef.current) {
         inputRef.current.focus(); //1st first time
      }      
      const res = await fetch(`${BOT_URL}/api/bot/`,{
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',       
         },
         credentials:"include",
         body: JSON.stringify({ userMsg: uMsg, chat_session_id: chatSessionIdRef.current }),
      })
      const data = await res.json()
      console.log("Bot response:", data.convo)

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      setConvo((prev:any) => [...prev, { role: "user", text: uMsg }])
      
      if (data.convo && data.convo.length > 0) {
         const latestBotMsg = data.convo[data.convo.length - 1]
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
         setConvo((prev:any) => [...prev, latestBotMsg])
      }
   } 
 
   function submitChat(e: React.FormEvent<HTMLFormElement>){
      e.preventDefault()
      sendToBot()
      setUMsg("")
   }
   const inputRef = useRef<HTMLInputElement>(null)
   const bottomRef = useRef<HTMLDivElement | null>(null);

   useEffect(() => {
      if (inputRef.current) {
         inputRef.current.focus(); //2nd time
         }
   }, [])
   useEffect(() => {
      requestAnimationFrame(() => {
         bottomRef.current?.scrollIntoView({ behavior: "smooth" });
      })
   }, [convo])

   
  return (
    <div>
       {/* Floating button */}
      {isIconOpen &&       
       <button
        onClick={handleOpenStatus}
         className="fixed bottom-25 right-6 hover:bg-green-100 rounded-full p-3"
         aria-label="Open Santa Chatbot" >
         <img src={santaIcon} alt="Santa Chatbot" className="w-12 h-12" />
      </button>      
      }   
      {/* Chat window */}
      {open && ( 
      <div className="fixed bottom-30 right-4 w-120 h-[540px] bg-white border rounded-lg shadow-lg flex flex-col  overflow-y-auto">
         {/* Header */}
          <div className={`${style.bgNavXmasBlue} text-white p-2 flex justify-between items-center`}>
            <span> <img src={santaIcon} alt="Santa Chatbot" className="w-9 h-9" /></span>
            <button onClick={handleOpenStatus}>✕</button>           
          </div>
         
          <div className="flex flex-col h-[500px] bg-white rounded-lg overflow-hidden">
         {/* Chat messages scrollable area */}
         <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {convo && convo.length > 0 && convo.map((msg, idx) => {
               const user_talk = msg.role === "user";
               return (
               <div
                  key={idx}
                  className={`p-2 rounded-xl max-w-[75%] ${user_talk ? `${style.bgLightXmasBlue} ml-auto text-left`: "bg-gray-100 mr-auto text-left"}`}  >
                  <b>{msg.role === "user" ? "You:" : "Bot:"}</b> {msg.text}
               </div>
               );
            })}
              <div ref={bottomRef} />
         </div>

         {/* Sticky input at bottom */}
         <form onSubmit={submitChat} className="p-2 bg-white">
            <input
               type="text"
               name="uMsg"
               value={uMsg}
               onChange={(e) => setUMsg(e.target.value)}
               placeholder="Type your message..."
               className="w-full rounded-full px-4 py-3 bg-gray-100 border border-white/10 focus:outline-none backdrop-blur-sm"
            />
         </form>
         </div>         
      </div>)}     
    </div>
  )
 }
