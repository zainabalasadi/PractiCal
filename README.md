# PractiCal
Calendar application with Natural Language Processing for event creation.

## Setup Instructions
1. Activate virtual environment
```
source venv/bin/activate
```
2. Install requirements
```
pip3 install -r requirements.txt
```
3. Navigate to static folder and install npm dependencies
```
npm install
```
4. Start the development watch server from the static folder
```
npm run watch
```
If you get an error here similar to **npm WARN babel-loader@8.0.2 requires a peer of @babel/core@⁷.0.0 but none was installed.**, then you should downgrade your babel-loader to 7.x as follows:
```
npm install babel-loader@^7 --save-dev
```
5. Open a terminal at the root directory and start the python server
```
python run.py
```