import shutil
import uuid
from fastapi import FastAPI, Request, Depends,Form,HTTPException, Body,UploadFile,File
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import engine, SessionLocal, get_db, Base
import models
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,RedirectResponse
from utils import *
from starlette.middleware.sessions import SessionMiddleware
from jose import jwt,JWTError
from sqlalchemy.orm import joinedload



app = FastAPI()
templates = Jinja2Templates(directory='templates')
Base.metadata.create_all(bind=engine)

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.add_middleware(SessionMiddleware, secret_key="e8Lj5R$Zv@n8!sWm3P#q")
@app.get("/get_home")
def root(request: Request, db : Session = Depends(get_db)):
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:
            return templates.TemplateResponse("home.html", {"request": request,"current_user":username})
    except:
         return RedirectResponse("/sign",status_code=303)    

@app.get("/get_product")
def root(request: Request, db : Session = Depends(get_db)):
    order = db.query(models.order).filter(models.order.Status=='Active').all()
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:
            results=db.query(models.Cart).all()
            return templates.TemplateResponse("2index.html", {"request": request, "products" : order,"current_user":username,"cart_items":results})
    except JWTError:
         return RedirectResponse("/sign",status_code=303)    

@app.get("/get_about")  
def root(request: Request, db : Session = Depends(get_db)):
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:
            return templates.TemplateResponse("about.html", {"request": request,"current_user":username})
    except:
         return RedirectResponse("/sign",status_code=303)
 
@app.get("/get_profile")  
def root(request: Request, db : Session = Depends(get_db)):
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:
            find=db.query(models.login).filter(models.login.User==username).first()
            find2=db.query(models.order33).filter(models.order33.name==username).all()
            product=[]
            for i in find2:
                product.append(db.query(models.order).filter(models.order.id==i.product_id).first())
            print(product)
            print(find2)
            return templates.TemplateResponse("profile.html", {"request": request ,"find":find,"find2":find2,"product":product})
    except JWTError:
         return RedirectResponse("/sign",status_code=303)            

@app.get("/get_contact")
def root(request: Request, db : Session = Depends(get_db)):
    order = db.query(models.order22).first()
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:        
            return templates.TemplateResponse("complaint.html", {"request": request, "order" : order,"current_user":username})
    except:
         return RedirectResponse("/sign",status_code=303)    

@app.get("/get_view/{id}")
def root(id:int,request: Request, db : Session = Depends(get_db)):
    getting= db.query(models.order).filter(models.order.Status=='Active',models.order.id==id).first()
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:
            return templates.TemplateResponse("productview.html", {"request": request, "order" : getting,"username":username})
    except:
         return RedirectResponse("/sign",status_code=303)   
      
@app.get("/get_admin")
def root(request: Request, db : Session = Depends(get_db)):
    order = db.query(models.order).filter(models.order.Status=='Active').all()
    order22=db.query(models.order22).all()
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str= payload.get("user_name")
        usermail: str= payload.get("user_email")
        
        if username is None or usermail is None:
            return RedirectResponse("/sign",status_code=303)
        else:
            return templates.TemplateResponse("adminpanel.html", {"request": request, "order" : order,"order22":order22})
    except:
         return RedirectResponse("/sign",status_code=303) 
@app.post("/form_post")
def root_post(request: Request,db: Session = Depends(get_db),product_name: str = Form(...),brand: str = Form(...),price: str = Form(...),stock_status: str = Form(...),description: str = Form(...),image:UploadFile=File(...),audio:UploadFile=File(...),video: UploadFile = File(...)):
    # image

    upload_img = image.content_type
    print(upload_img)    
    extention = upload_img.split('/')[-1]
    token_image = str(uuid.uuid4())+'.'+str(extention)
    file_location = f"./templates/images/{token_image}"
    with open (file_location,'wb+') as file_object:
     shutil.copyfileobj(image.file,file_object)
    
    # video
    
    upload_video = video.content_type
    print(upload_video)    
    extention = upload_video.split('/')[-1]
    token_video = str(uuid.uuid4())+'.'+str(extention)
    file_location = f"./templates/videos/{token_video}"
    with open (file_location,'wb+') as file_object:
     shutil.copyfileobj(video.file,file_object)


    # aduio
    
    upload_audio = audio.content_type
    print(upload_audio)    
    extention = upload_audio.split('/')[-1]
    token_audio = str(uuid.uuid4())+'.'+str(extention)
    file_location = f"./templates/audios/{token_audio}"
    with open (file_location,'wb+') as file_object:
     shutil.copyfileobj(audio.file,file_object)

    datas=models.order(product_name=product_name,brand=brand,price=price,stock_status=stock_status,description=description,image=token_image,video=token_video,audio=token_audio,Status='ACTIVE')
    db.add(datas)
    db.commit()
    db.refresh(datas)
    error="Done"
    json_compatible_item_data = jsonable_encoder(error)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/sign")
def login_page(request: Request):   
    return templates.TemplateResponse('login.html', context={'request': request}) 
@app.get("/pay")
def login_page(request: Request):   
    return templates.TemplateResponse('pay.html', context={'request': request}) 

 
@app.post("/signup")
async def signup(request:Request,db:Session=Depends(get_db),signup_username:str=Form(...),signup_email:str=Form(...),signup_number:str=Form(...),signup_password:str=Form(...)):
    find=db.query(models.login).filter(models.login.User ==signup_username,models.login.Email==signup_email).first()
    if find is not None:
        error= "This user name and email is already exist"   
        json_compatible_item_data = jsonable_encoder(error)
        return JSONResponse(content=json_compatible_item_data)
    else:
        data=models.login(User=signup_username,Email=signup_email,Phone_Number=signup_number,Password=signup_password)
        db.add(data)
        db.commit()
        error= "Done"   
        json_compatible_item_data = jsonable_encoder(error)
        return JSONResponse(content=json_compatible_item_data)
    return RedirectResponse(url="/pay")
@app.post("/logcheck")
async def logcheck(request: Request, login_email: str = Form(...), login_password: str = Form(...)):
    db = SessionLocal()
    user = db.query(models.login).filter(models.login.Email == login_email, models.login.Password == login_password).first()
    if user:
        access_token_expires = timedelta(minutes=BaseConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"user_name": user.User,"user_email":user.Email},expires_delta=access_token_expires)
        sessid = access_token
        request.session["user"] = sessid
        return JSONResponse(content={"message": "Done"})
    else:
        return JSONResponse(content={"message": "Invalid credentials"})
    return RedirectResponse(url="/pay")

@app.put("/put_form/{g}")
def get_form(g:int,request:Request,db:Session = Depends(get_db)):
    data1=db.query(models.order).filter(models.order.id==g).first()
    json_compatible_item_data = jsonable_encoder(data1)
    return JSONResponse(content=json_compatible_item_data)

@app.get('/del_data/{id}') 
def get_form(id:int,request:Request,db:Session = Depends(get_db)):
    db.query(models.order).filter(models.order.id==id).update({"Status": "INACTIVE"})    
    db.commit()
    error = "Done"
    json_compatible_item_data = jsonable_encoder(error)
    return JSONResponse(content=json_compatible_item_data) 

@app.post("/form_postcomp")
def root_post(request: Request,db: Session = Depends(get_db),description: str = Form(...),image:UploadFile=File(...)):
    # image

    upload_img = image.content_type
    print(upload_img)    
    extention = upload_img.split('/')[-1]
    token_image = str(uuid.uuid4())+'.'+str(extention)
    file_location = f"./templates/images/{token_image}"
    with open (file_location,'wb+') as file_object:
     shutil.copyfileobj(image.file,file_object)
     
    datas=models.order22(description=description,image=token_image)
    db.add(datas)
    db.commit()
    db.refresh(datas)
    error="Done"
    json_compatible_item_data = jsonable_encoder(error)
    return JSONResponse(content=json_compatible_item_data)
     
@app.put("/put_formcomp/{g}")
def get_form(g:int,request:Request,db:Session = Depends(get_db)):
    data1=db.query(models.order22).filter(models.order22.id==g).first()
    json_compatible_item_data = jsonable_encoder(data1)
    return JSONResponse(content=json_compatible_item_data)    



#filter query code:--------------->



@app.get("/filter")
def rentalpoints(fdata:str,request:Request,db:Session=Depends(get_db)):
    login_status=0
    fdata=list(fdata.split(','))
    print(fdata)
    result=None
    query = db.query(models.order).filter(models.order.Status == "Active")

    if "High-Low" in fdata:
        query = query.order_by(models.order.price.desc())
    elif "Low-High" in fdata:
        query = query.order_by(models.order.price)

    if "brembo" in fdata:
        query = query.filter(models.order.brand == "Brembo")
    elif "michelin" in fdata:
        query = query.filter(models.order.brand == "Michelin")
    elif "bosch" in fdata:
        query = query.filter(models.order.brand == "Bosch")
    elif "Motul" in fdata:
        query = query.filter(models.order.brand == "Motul")        

    elif "honda" in fdata:
        query = query.filter(models.order.brand == "Honda")
    elif "bmw" in fdata:
        query = query.filter(models.order.brand == "Bmw")

    elif "kawasaki" in fdata:
        query = query.filter(models.order.brand == "Kawasaki")
    elif "ktm" in fdata:
        query = query.filter(models.order.brand == "Ktm")
    elif "yamaha" in fdata:
        query = query.filter(models.order.brand == "Yamaha")

    result = query.all()

    return templates.TemplateResponse('2index.html', context={'request': request,"order":result,"ffdata":fdata}) 

@app.post("/form_postpayment")
def root_post(request: Request,db: Session = Depends(get_db),name: str = Form(...),Address: str = Form(...),Pincode: str = Form(...),Mobile_number: str = Form(...),quantity: str = Form(...),grand_total : str=Form(...),Product_id : str= Form(...)):
    
        datas=models.order33(name=name,Address=Address,Pincode=Pincode,Mobile_number=Mobile_number,quantity=quantity,price=grand_total,product_id=Product_id)
        db.add(datas)
        db.commit()
        db.refresh(datas)
        error="Done"
        json_compatible_item_data = jsonable_encoder(error)
        return JSONResponse(content=json_compatible_item_data)
    
@app.put("/put_formprofile/{g}")
def get_form(g:int,request:Request,db:Session = Depends(get_db)):
    data1=db.query(models.login).filter(models.login.id==g).first()
    json_compatible_item_data = jsonable_encoder(data1)
    return JSONResponse(content=json_compatible_item_data)    

@app.post('/update_value')
def root_post(request: Request,db: Session = Depends(get_db),edit_id:str = Form(...),Email: str = Form(...),phonenum: str = Form(...),newpass: str = Form(...),currpass:str=Form(...)):    
    find=db.query(models.login).filter(models.login.id==edit_id,models.login.Password==currpass).first()
    if find is not None:
        db.query(models.login).filter(models.login.id==edit_id).update({'Email': Email,'Phone_Number':phonenum,'Password':newpass})
        db.commit()
        error="Done"
        json_compatible_item_data = jsonable_encoder(error)
        return JSONResponse(content=json_compatible_item_data)
        
        



@app.post('/add_cart/{product_id}')
def add_to_cart_route(product_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str = payload.get("user_name")
        usermail: str = payload.get("user_email")
         
        if username is None or usermail is None:
            return RedirectResponse("/sign", status_code=303)
        else:   
            # Check if the product exists in the cart
            cart_entry = db.query(models.Cart).filter(models.Cart.product_id == product_id, models.Cart.user_name == username).first()
            if cart_entry:
                # Toggle cart status
                cart_entry.cart_Status = 'yes' if cart_entry.cart_Status == 'no' else 'no'
            else:
                # If the product is not in the cart, add it
                cart_entry = models.Cart(product_id=product_id, user_name=username, cart_Status='yes')
                db.add(cart_entry)
            db.commit()
            return RedirectResponse("/get_product", status_code=303)
            
    except:
        return RedirectResponse("/sign", status_code=303)
        
        


@app.get("/cart")
def login_page(request: Request,db: Session = Depends(get_db)):
    try:
        token = request.session["user"]
        payload = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.ALGORITHM] )
        username: str = payload.get("user_name")
        usermail: str = payload.get("user_email")
            
        if username is None or usermail is None:
            return RedirectResponse("/sign", status_code=303)
        else:   
            # Check if the produ
            results = db.query(models.Cart).filter(models.Cart.user_name==username, models.Cart.cart_Status=='yes').all()
            product_ids = [cart.product_id for cart in results]
            orders = db.query(models.order).filter(models.order.id.in_(product_ids)).all()
            return templates.TemplateResponse('cart.html', context={'request': request,'products':orders,"current_user":username}) 
    except JWTError:
        return RedirectResponse("/sign", status_code=303)

