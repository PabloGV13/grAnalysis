import { useEffect, useState } from "react";
import axios from 'axios';
import { Table, Checkbox } from "antd";
import Container from "react-bootstrap/esm/Container";
import { Link } from "react-router-dom";
import { FileSearchOutlined } from "@ant-design/icons";
import Button from "react-bootstrap/esm/Button";

function Comparar() {
    const [loading, setLoading] = useState(false);
    const [stays, setStays] = useState([]);
    const [selectedStays, setSelectedStays] = useState([]);
    
    useEffect(() => {
        setLoading(true)
        axios.get('/api/analisis')
            .then(response => {
                console.log(response)
                setStays(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetchin stays', error);
            }); 
    }, []);

    const handleStaySelection = (stayId, checked) => {
        if (checked) {
          setSelectedStays([...selectedStays, stayId]);
        } else {
          setSelectedStays(selectedStays.filter((id) => id !== stayId));
        }
      };

    return(
        <Container className="m-auto">
            <h1 className="fs-4 text-start">Selecciona dos alojamientos a comparar:</h1>
            {stays.length && <Table
                loading = {loading}
                dataSource={stays}
                columns={[
                    {
                        title: '',
                        dataIndex: "stay_id",
                    },
                    {
                        title: 'Nombre',
                        dataIndex: "name"
                    },
                    {
                        title: 'URL',
                        dataIndex: "url",
                        render: value => <a href={value} target="_blank">{value}</a> 
                    },
                    {
                        title: '',
                        dataIndex: "stay_id",
                        render: (stayId) => (
                            <Checkbox
                                checked={selectedStays.includes(stayId)}
                                onChange={(e) => handleStaySelection(stayId, e.target.checked)} 
                            />
                        ),
                    },
                ]}
                paginaion={{
                    pageSize: 5,
                }}
            >
            </Table>}

        </Container>
    );


}

export default Comparar;