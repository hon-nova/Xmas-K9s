from pydantic import BaseModel  # v2

class User(BaseModel):
   name: str
   year: int

u = User(name="Hon", year=20)
u_dict = u.model_dump()        # replaces u.dict()
# print(f"u_dict: {u_dict}") # {'name': 'Hon', 'year': 20}
u_json = u.model_dump_json()   # replaces u.json()
print(f"u_json: {u_json}") #  {"name":"Hon","year":20}
validated = User.model_validate({"name": "Hon", "year": 20})
