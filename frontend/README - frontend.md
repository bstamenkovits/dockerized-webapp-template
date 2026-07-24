# Frontend

This is the frontend of the webapp, it is written in TypeScript, and uses React (with Vite and React Router).

## Setup
The frontend is built to the `dist` directory, and then mounted by the backend. You only really need to build the 
frontend once. 

For development you can run the frontend either locally or in a Docker container. In either case create a file called `.env` in the root of the repo, and add the following: [todo]

### Docker
[ToDo]

### Local 
For local development you can install the dependencies locally on your machine.

1) Navigate to the frontend directory
```aiignore
cd frontend 
```

2) Install dependencies 
```aiignore
npm install
```

3) Build the frontend `dist` directory
```aiignore
npm run build
```

 The webpages should now be available when running the backend (see `README - backend.md`)

> **Alternatively**  
> For development purposes you can run the local Vite dev server (with HMR)
> ```aiignore
> npm run dev
> ```
>
> You can now access the app at `http://localhost:5173`
