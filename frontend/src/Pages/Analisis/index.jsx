import { useEffect, useState } from "react";
import axios from 'axios';
import { Table } from "antd";
import Container from "react-bootstrap/esm/Container";
import { Link } from "react-router-dom";
import { FileSearchOutlined } from "@ant-design/icons";
import Button from "react-bootstrap/esm/Button";

function Analisis() {
    const [loading, setLoading] = useState(false);
    const [stays, setStays] = useState([]);
    
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

    return(
        <Container className="m-auto">
            <h1 className="fs-4 text-start">Alojamientos</h1>
            {stays.length && <Table
                loading = {loading}
                dataSource={stays}
                columns={[
                    {
                        title: '',
                        dataIndex: "stay_id"
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
                        title: 'Análisis',
                        dataIndex: "stay_id",
                        render: link => <Link to={`/analisis/${link}`}><Button variant="link"> <FileSearchOutlined /> </Button></Link>
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

export default Analisis;