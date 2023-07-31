import { Routes, Route } from "react-router-dom"
import Analisis from "../../Pages/Analisis"
import Comparar from "../../Pages/Comparar"
import Estadisticas from "../../Pages/Estadisticas"

function AppRoutes() {
    return (
        <Routes>
            <Route path = "/" element={<Analisis />}></Route>
            <Route path = "/analisis" element={<Analisis />}></Route>
            <Route path = "/comparar" element={<Comparar />}></Route>
            <Route path = "/analisis/:id" element={<Estadisticas />}></Route>
        </Routes>
    );
}
export default AppRoutes