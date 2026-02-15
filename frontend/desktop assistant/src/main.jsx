import { StrictMode } from 'react'
import './index.css'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter,RouterProvider } from 'react-router-dom'
import App from './App.jsx'
import Error from './Error.jsx'
import About from './About.jsx'
import Updates from './Updates.jsx'
const router = createBrowserRouter([
      {
        path : '/',
        element : <App/>,
        errorElement : <Error/>
      },
      {
        path : "/about",
        element : <About/>,
        errorElement : <Error/>
      },
      {
        path : "/updates",
        element : <Updates/>,
        errorElement : <Error/>
      }
    ])
createRoot(document.getElementById('root')).render(
  <RouterProvider router={router}/>
)
