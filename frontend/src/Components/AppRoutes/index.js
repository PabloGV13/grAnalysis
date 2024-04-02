import { Routes, Route } from "react-router-dom"
import Analisis from "../../Pages/Analisis"
import Comparar from "../../Pages/Comparar"
import Estadisticas from "../../Pages/Estadisticas"
import Comparacion from "../../Pages/Comparacion"
import Mapa from "../../Pages/Mapa"
import Admin from "../../Pages/Admin"

function AppRoutes() {
    return (
        <Routes>
            <Route path = "/" element={<Analisis />}></Route>
            <Route path = "/analisis" element={<Analisis />}></Route>
            <Route path = "/comparar" element={<Comparar />}></Route>
            <Route path = "/analisis/:id" element={<Estadisticas />}></Route>
            <Route path = "/comparar/:firstStayId/:secondStayId" element={<Comparacion />}></Route>
            <Route path = "/mapa" element={<Mapa/>}></Route>
            <Route path = "/admin" element={<Admin/>}></Route>
        </Routes>
    );
}
export default AppRoutes