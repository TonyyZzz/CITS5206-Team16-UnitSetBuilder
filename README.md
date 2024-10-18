# CITS5206-Team16-UnitSetBuilder

Information Technology Capstone Project - Unit Set Builder - Team 16

### Application Objective

The Unit Set Builder aims to address the challenges faced by our client, whose current system is outdated and cumbersome to use. This application streamlines the management of course structures, enhancing the efficiency of daily operations. Key features of the Unit Set Builder include:

- Login/Logout into website
- Search courses
- Create and manage course structure (known as Unit Set)
- Create reusable specialisation where can be used by multiple courses
- Drag and Drop to manage the sturcuture of the course

### How to set up the application on you location machine

**1. Git Clone**

Using the HTTPS link retrieved from the project GitHub repository and run the following command in Terminal to clone project source code to your server or your local host machine.

```bash
git clone https://github.com/TonyyZzz/CITS5206-Team16-UnitSetBuilder.git
```

**2.Create python virtual environment**

```bash
Python -m venv venv #Create new virtual env
source venv/bin/activate # activate virtual env
```

**3. Activate virutal environemnt**

**macOS/Linux**
```bash
source venv/bin/activate

```
**Windows**
```bash
.\venv\Scripts\activate
```

**3. Install Required Packages**
```bash
pip install -r requirements.txt
```

**4. Set up app configurations**
```bash
echo FLASK_APP=app:create_app\(\"development\"\) > .env
echo FLASK_ENV=development >> .env
```

**5. Initialize and Migrate database**
```bash
flask db init
flask db migrate -m "init"
flask db upgrade
```

**6. Load existing data**
```bash
flask loaddata
```

**7. Launch Application**
```bash
flask run
```

**Enjoy the application!**

### Deployment

The application is currently deployed using `Heroku`. To access the deployed website with this [link](https://unitsetbuilder-a33e3d2c8e96.herokuapp.com/). The detailed deployment steps refer to [User Manual](https://github.com/TonyyZzz/CITS5206-Team16-UnitSetBuilder/blob/main/deliverables/User_Manual.pdf).
