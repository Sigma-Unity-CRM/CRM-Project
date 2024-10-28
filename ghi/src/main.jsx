import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
    },
])

const rootElement = document.getElementById('root')
if (!rootElement) throw new Error('root element was not found')

console.table(import.meta.env)

const root = ReactDOM.createRoot(rootElement)
root.render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
)
