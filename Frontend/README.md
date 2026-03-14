# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## UniAid Frontend

Frontend application for UniAid, a platform that helps international students and parents connect with mentors, alumni, and professors for guidance about universities, cities, and student life.

Built with: React, Vite, Material UI, Redux Toolkit, React Router.

### 1. Requirements

- Node.js: https://nodejs.org — verify with `node -v` and `npm -v`

### 2. Clone and enter Frontend

```bash
git clone https://github.com/bhattrahul525/UniAid.git
cd UniAid/Frontend
```

### 3. Install and run

```bash
npm install
npm run dev
```

Open http://localhost:5173/

### 4. Project structure

- `public` — static assets
- `src/components`, `src/pages`, `src/routes`, `src/store`, `src/slices`

### 5. Backend

Default API: http://localhost:8000 — ensure the backend is running for API features.
