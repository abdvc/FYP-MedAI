# FYP-MedAI
## Description
An open-source Medical Assistant using AI and AI explainability techniques.

## Features
* Doctors can login and enter medical data for a disease they wish to diagnose
* Get a prediction and explanation for the prediction after data entry
* Doctors can look up patients in the hospital database
* Admin can create new login users
* Admin can insert new ML models into the system

## System requirements
* Python 3.7.0+
* pip 20.0.1+
* SQLite 3.21.0+
* Microsoft Visual C++ Build Tools

## Dependencies
Dependencies are listed in [requirements.txt](https://github.com/abdvc/FYP-MedAI/blob/master/requirements.txt). 

## Build instructions
### Clone project
Clone the repository using:
```
   git clone https://github.com/abdvc/FYP-MedAI
```

### Download materials
Download and install Python from the [link](https://www.python.org/downloads/). Ensure that your Python download is the same as your machine (64-bit or 32-bit).

Download and install Microsoft Visual C++ Build Tools from the [link](https://visualstudio.microsoft.com/visual-cpp-build-tools/).

Download and install pip from the [link](https://pip.pypa.io/en/stable/installing/).

### Install dependencies
Install application dependencies using:
```
    pip install -r requirements.txt
```

## Run application
To run the application you need to run **app.py** in the base directory
  ```
      cd FYP-MedAI
      app.py
  ```

After the application is running, go to the url displayed on the command prompt. The default url is: 
  ```
      http://127.0.0.1:5000/
  ```
You shall be redirected to the login page. You can login using either the admin or doctor credentials.

#### Admin
Email: admin@admin.com

Password: admin

#### Doctor
Email: test@test.com

Password: test

## License
This application is licensed under GNU General Public License v3.0. The license is available at [LICENSE.md](https://github.com/abdvc/FYP-MedAI/blob/master/LICENSE).

## Developers
Abdullah Humayun

Abdul Razzaque Soomro

Danysh Soomro
