import {Menu} from "antd"
import {BarChartOutlined, ReconciliationOutlined, CompassOutlined } from "@ant-design/icons"
import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState} from "react";

function SideMenu(props) {

    const location = useLocation();
    const [selectedKeys, setSelectedKeys] = useState("/");
    const {isAdmin} = props;

    useEffect(() => {
        const pathName = location.pathname;
        setSelectedKeys(pathName);
    }, [location.pathname]);

    const navigate = useNavigate();

    const items = [
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
        {
            label:"Mapa",
            icon: <CompassOutlined/>,
            key:"/mapa"
        },
    ];

    if(isAdmin)
        items.push([{
            label:"Mapa admin 1",
            icon: <CompassOutlined/>,
            key:"/mapa"
        },
        {
            label:"Mapa admin 2",
            icon: <CompassOutlined/>,
            key:"/mapa"
        }
    ]);

    return (
    <div className="SideMenu">
        <Menu 
        className="SideMenuVertical"
        mode="vertical"
        onClick={(item) => {
            navigate(item.key)
        }}
        selectedKeys={[selectedKeys]}
        items={items}
        ></Menu>
    </div>
    );
}
export default SideMenu