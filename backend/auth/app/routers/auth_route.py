import os
from fastapi import APIRouter,Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from core.model import  User
from core.session import get_db
from core.config import settings

from auth.app.schemas import RegisterRequest, RegisterResponse, RegisterFilter,LoginRequest, LoginResponse, LoginFilter
from auth.app.services import hash_password, verify_password, create_user, create_access_token

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])
import logging
logger = logging.getLogger("uvicorn.error") 

@auth_router.post("/register")
def register(payload: RegisterRequest,db: Session = Depends(get_db)) -> RegisterResponse |dict:
   try:      
      user_db = db.query(User).filter(User.email == payload.email).first()
      if user_db:
         return {
            "detail":"Username or email already exists. Log in instead."
         }       
            
      create_user(**payload.model_dump())       
      
      hashed_pwd = hash_password(payload.password)
      
      new_user = User(
         username=payload.username,
         email = payload.email,
         password=hashed_pwd
         )
      db.add(new_user)
      db.commit()
      db.refresh(new_user)
            
      base = RegisterFilter.model_validate(new_user)
      data = base.model_dump()
      data['message'] = "Registered successfully!"
      response = RegisterResponse(**data)         

      return response        
      
   except HTTPException:       
      raise
   except Exception as e:       
      raise HTTPException(status_code=500, detail=f"Exception: {str(e)}, Internal server error")
   
@auth_router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
   try:     
      user_db = db.query(User).filter(User.email == payload.email).first()
      logging.error(f"user_db: {user_db}")
      if not user_db:
         return {
            "detail":"User Not Found!"
         } 
        
      if not verify_password(payload.password,user_db.password):
         return {
            "detail": "Password is incorrect!"
         }
              
      base = LoginFilter.model_validate(user_db)
      data = base.model_dump()
      
      jwt_data =  {
         "sub":str(user_db.id),
         "username":user_db.username
      }
      
      access_token = create_access_token(jwt_data)
      print(f"Generated access_token: {access_token}")
      
      data['token']=access_token
      data['message'] ="Login Success"
      
      from fastapi.encoders import jsonable_encoder    
      data = jsonable_encoder(data)  
      
      response = JSONResponse(content=data)
      cookie_domain = ".xmas-k9s.tech" if os.getenv("ENV") == "prod" else None      
      response.set_cookie(
         key="k8s_token",
         value=access_token,
         domain=cookie_domain,
         httponly=True,         
         secure=False if cookie_domain is None else True,
         samesite="lax" if cookie_domain is None else "none",
         max_age=60*60*24*30
      )   
      
      # cookie_domain = ".xmas-k9s.tech"  
      # response.set_cookie(
      #    key="k8s_token",
      #    value=access_token,
      #    domain=cookie_domain,    # must match all subdomains
      #    httponly=True,           # prevents JS access
      #    secure=True,             # required for HTTPS
      #    samesite="none",         # allows cross-subdomain p
      #    max_age=60*60*24*30
      # )
      
      return response      
      
   except Exception as e:
      print(f"EXCEPTION /login: {str(e)}")
      raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


from core.auth import get_current_user
@auth_router.get("/me",response_model=LoginFilter)
def get_me(user: User = Depends(get_current_user)):
   
   base= LoginFilter.model_validate(user) 
   print(f"get_me: {base}")
      
   return base

@auth_router.post("/logout")
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


@auth_router.get("/secretValue")
def get_config_value():   
   try:
      return {
         "AUTH":"yes",        
         "DATABASE_URL": settings.DATABASE_URL,      
      }
   except Exception as e:
      print(f"EXCEPTION: {e}")