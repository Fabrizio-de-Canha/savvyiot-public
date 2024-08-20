import { useLocation, Navigate } from "react-router-dom"

export const setToken = (token: string) => {
    localStorage.setItem('token_local', token)
}

export const fetchToken = () => {
    return localStorage.getItem('token_local')
}

export function RequireToken({ children }: any) {

    let auth = fetchToken()
    let location = useLocation()

    if (!auth) {
        return <Navigate to='/login' state={{ from: location }} />;
    }

    return children;
}

export function RequireAdminToken({ children }: any) {

    let auth = fetchToken()
    let location = useLocation()

    let cookieValue = document.cookie.replace(/(?:(?:^|.*;\s*)claims\s*\=\s*([^;]*).*$)|^.*$/, "$1");

    if (!auth || cookieValue!=="True") {
        return <Navigate to='/login' state={{ from: location }} />;
    }

    return children;
}