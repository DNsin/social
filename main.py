from datetime import datetime
from typing import Optional, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel, ConfigDict
from router import router_cred, router


app = FastAPI()
app.include_router(router_cred)
app.include_router(router)







if __name__ != "__main__":
    pass
else:
    app.run()
