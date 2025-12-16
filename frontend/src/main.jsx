import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { CoverageProvider } from './contexts/CoverageContext'
import './index.css'
import AppRoutes from './routes'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <CoverageProvider>
        <AppRoutes />
      </CoverageProvider>
    </BrowserRouter>
  </StrictMode>,
)
