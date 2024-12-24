# Real_Time_Quiz_App
🎯 This is a real-time quiz app where you can 🖊️ create, edit, and delete quizzes effortlessly. 📊 Track your progress as you play and, best of all, you can even join the fun as a guest 👤 without needing to log in. 🚀 Dive into the excitement now! 📝

1. **Install Python**  
   Make sure Python is installed on your system. Download it from the [official Python website](https://www.python.org/downloads/).

   ```bash
   # Check if Python is installed
   python --version

2. **setup Django**

 ```bash
   #  Django is installed
   pip install django

   # Verify the installation
   django-admin --version
```

### 2️⃣ Set Up Your Virtual Environment (Optional)
To avoid dependency issues, it is recommended to create a virtual environment. Here's how:
1. Open the extracted folder in **VS Code**.
2. In the terminal, create the virtual environment:
   ```bash
   python -m venv env
   ```
3. Activate the virtual environment:
   ```bash
   .\env\Scripts\activate.ps1
   ```

### 3️⃣ Install Dependencies
Once inside the virtual environment, install Django:
```bash
pip install django
```

### 4️⃣ Navigate to the Project Directory
Change to the `quiz` directory where the `manage.py` file is located:
```bash
cd quiz
```

### 5️⃣ Migrate the Database
Apply database migrations using the following commands:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Create a Superuser 
You can create a superuser to manage the database via Django's admin panel: 
```bash
python manage.py createsuperuser
```
- Follow the prompts to add a username and password of your choice. To access the admin panel you can visit to http://127.0.0.1:8000/admin/ url and see database.


### Run the Superuser 
To run the server run the below command in terminal after run the command to access the website you can visit to http://127.0.0.1:8000/
```bash
python manage.py runserver
```
