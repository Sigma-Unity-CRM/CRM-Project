import { Outlet } from 'react-router-dom'

export default function App() {
    return (
        <div>
            <header></header>
            <div>
                <Outlet />
            </div>
        </div>
    )
}
