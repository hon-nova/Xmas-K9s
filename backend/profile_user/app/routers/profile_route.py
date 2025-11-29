from core.schema import LoginFilter, EventFilter
from core.model import User
from core.config import settings
from core.utils import user_events
from fastapi import APIRouter, Response, Depends

profile_router = APIRouter(prefix="/api/profile", tags=["profile"])


from core.auth import get_current_user
@profile_router.get("/auth",response_model=LoginFilter)
def auth_me(user: User = Depends(get_current_user)):
   
   base= LoginFilter.model_validate(user) 
   print(f"auth_me: {base}")
      
   return base

@profile_router.get("/events")
def get_user_events(user: User = Depends(get_current_user)):      
 
   events = user_events(user.id)  
   events_return = []

   for event in events:
      base = EventFilter.model_validate(event, from_attributes=True)  
      events_return.append(base)

   print(f"IMPORTANT profile_router: base events: {events_return}")
   return {"events": events_return if events_return else []}
   # return {"events": ["test", "123"]}
   
@profile_router.post("/logout")
def logout(response: Response):
    """
    Logs the user out by clearing the auth cookie.
    """
    response.delete_cookie(
        key="k8s_token",
        domain=".xmas-k9s.tech", 
        httponly=True,
        secure=True,
        samesite="none"
    )
    return {"message": "Logged out successfully"}

@profile_router.get("/secretValue")
def get_config_value():   
   try:
      return {
         "PROFILE":"yes",        
         "DATABASE_URL": settings.DATABASE_URL,      
      }
   except Exception as e:
      print(f"EXCEPTION: {e}")
