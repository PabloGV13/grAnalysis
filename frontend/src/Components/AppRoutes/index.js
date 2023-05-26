import { BrowserRouter, Routes, Route } from "react-router-dom"
import Analisis from "../../Pages/Analisis"
import Comparar from "../../Pages/Comparar"
import Principal from "../../Pages/Principal"
function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path = "/" element={<Principal />}></Route>
                <Route path = "/analisis" element={<Analisis />}></Route>
                <Route path = "/comparar" element={<Comparar />}></Route>
            </Routes>
        </BrowserRouter>
    );
}
export default AppRoutes