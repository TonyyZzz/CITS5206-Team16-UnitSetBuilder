# CITS5206-Team16-UnitSetBuilder
Information Technology Capstone Project - Unit Set Builder - Team 16

## Backend Setup

### 1. Git Clone

Using the HTTPS link retrieved from the project GitHub repository and run the following command in Terminal to clone project source code to your server or your local host machine.

```bash
git clone https://github.com/TonyyZzz/CITS5206-Team16-UnitSetBuilder.git
```

### 2.Create the python virtual environment
```bash
Python -m venv venv #Create new virtual env
source venv/bin/activate # activate virtual env
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Initialize and Migrate database
```bash
flask db init # initialize database
flask db upgrade # implement all migrations
```

### 5. Launch Application
```bash
flask run
```

### 6. Enjoy the application