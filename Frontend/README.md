UniAid Frontend

Frontend application for UniAid, a platform that helps international students and parents connect with mentors, alumni, and professors for guidance about universities, cities, and student life.

This project is built with:

React

Vite

Material UI

Redux Toolkit

React Router

1. Requirements

Before running the project, install:

Node.js

Download and install:

https://nodejs.org

Then verify installation:

node -v
npm -v

If both commands print versions, you are ready.

2. Clone the Repository
git clone https://github.com/bhattrahul525/UniAid.git

Move into the frontend folder:

cd UniAid/Frontend
3. Install Dependencies

Run:

npm install

This will install all required packages.

4. Start the Development Server

Run:

npm run dev

You will see output like:

VITE vX.X.X  ready in XXX ms

➜  Local:   http://localhost:5173/

Open the URL in your browser.

5. Project Structure
Frontend
│
├ public
│
├ src
│   ├ components
│   ├ pages
│   ├ routes
│   ├ store
│   └ slices
│
├ index.html
├ package.json
├ vite.config.js
└ README.md
6. Common Commands

Install dependencies

npm install

Run development server

npm run dev

Build production version

npm run build

Preview production build

npm run preview
7. Troubleshooting
Node modules error

If something breaks, delete dependencies and reinstall:

rm -rf node_modules
npm install
Port already in use

Run:

npm run dev -- --port 5174
8. Important Notes

Do NOT commit these files to Git:

node_modules
.env
dist
9. Backend Integration

The frontend expects the backend API to run locally.

Default backend URL:

http://localhost:8000

Make sure the backend server is running before using features that require API calls.