import {Menu} from "antd"
import {BarChartOutlined, ReconciliationOutlined} from "@ant-design/icons"
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState} from "react";

function SideMenu() {

    const location = useLocation();
    const [selectedKeys, setSelectedKeys] = useState("/");
    

    useEffect(() => {
        const pathName = location.pathname;
        setSelectedKeys(pathName);
    }, [location.pathname]);

    const navigate = useNavigate();

    return (
    <div className="SideMenu">
        <Menu 
        className="SideMenuVertical"
        mode="vertical"
        onClick={(item) => {
            navigate(item.key)
        }}
        selectedKeys={[selectedKeys]}
        items={[
            {
                label:"Análisis",
                icon:<BarChartOutlined />,
                key:"/analisis"
            },
            {
                label: "Comparar",
                icon: <ReconciliationOutlined />,
                key:"/comparar",
            },
        ]}
        ></Menu>
    </div>
    );
}
export default SideMenu