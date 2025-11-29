import  style  from "../../styles/style.module.css";
export function Footer(){

   return (
      <div className={`${style.bgNavXmasBlue} ${style.bgXmasStars} fixed bottom-0 w-full`}>        
         <div className="p-5">                
            <ul className="flex flex-col">
               <li>COMP4016 Applied DevOps with Kubernetes - BCIT (Winter 2025)</li>
               <li>Prof: Prabhjot Lalli</li>
               <li>Student: Hon Nguyen</li>
            </ul>
         </div>
</div>
   )
}