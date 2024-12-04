# HttpClient

This is the http client, which you can capture the website information, including text, image and hyperlink by entering url and method. Besides, we create a server for test.

## How to use it

* Clone or download the repository

### Install the requirement

 >  pip install -r requirements.txt

### Running Server

``` 
# Server/Profile/
python manage.py runserver 127.0.0.1:8000
# Visit Server Website
http://127.0.0.1:8000/
```

### Running Client

``````
# Client/Client
python manage.py runserver 127.0.0.1:8001
# Visit Client Website
http://127.0.0.1:8001/
``````

### Set Request

> URL: http://127.0.0.1:8000/
>
> HTTP Method：GET/HEAD/POST
>
> POST Data(if needed)：name=your_name&email=your_email&phone=your_phone&address=your_address

