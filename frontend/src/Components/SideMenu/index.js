import {Menu} from "antd"
import {BarChartOutlined, ReconciliationOutlined} from "@ant-design/icons"

function SideMenu() {
    return (
    <div className="SideMenu">
        <Menu 
        onClick={(item)=>{
            //item.key
        }}
        items={[
            {
                label:"Análisis",
                icon:<BarChartOutlined />,
                key:"/",
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