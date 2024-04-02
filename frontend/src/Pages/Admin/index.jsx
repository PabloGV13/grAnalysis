import { Component, useEffect, useState } from "react";
import axios from 'axios';
import { Table } from "antd";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row"
import Col from "react-bootstrap/esm/Col";
import { Link } from "react-router-dom";
import { DeleteOutlined, PlusCircleOutlined } from "@ant-design/icons";
import Button from "react-bootstrap/esm/Button";

function Admin() {
    
    const [loading, setLoading] = useState(false);
    const [users, setUsers] = useState([]);
    const [stays, setStays] = useState([]);
    const [requestedStays, setRequestedStays] = useState([]);
    const [analysedStays , setAnalysedStays] = useState([]);

    
    useEffect(() => {
        setLoading(true)
        Promise.all([
            axios.get('/api/users'),
            axios.get('/api/stays'),
            axios.get('/api/stays/get_request_stay')
        ]).then(response => {
            console.log(response)
            setUsers(response[0].data);
            setStays(response[1].data);
            setRequestedStays(response[2].data)
            setLoading(false);
 
        }).catch(error => {
            
            console.error('Error fetchin data', error);

        }); 
    }, []);

   
    const handleDeleteUser = (userId) => {
        axios.delete(`/api/delete/user/`+userId)
            .then(response => {
                console.log(response.data);
                // Actualizar la lista de usuarios después de eliminar el usuario
                setUsers(users.filter(user => user.user_id !== userId));
            })
            .catch(error => {
                console.error('Error deleting user', error);
            });
    };

    const handleDeleteStay = (stayId) => {
        axios.delete('/api/delete/stay/'+stayId)
            .then(response => {
                console.log(response.data);
                setStays(stays.filter(stay => stay.stay_id !== stayId));
            })
            .catch(error =>  {
                console.error('Error deleting stay', error);
            });    
    };

    const handleNewAnalysis = (stayId) => {
        axios.post('/api/stays/post_stay_analysis/'+stayId)
        .then(response =>{
            console.log("Analisis solicitado correctamente:", response.data);
        })
        .catch(error => {
            console.error('Error during stay analysis', error);
        });
    };

    return( 

        <Container className="m-auto">
            <Row>
                <Col>
                    <h1 className="fs-4 text-start">Alojamientos</h1>
                    {(stays.length !== 0) && <Table
                        loading = {loading}
                        dataSource={stays}
                        columns={[
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
                                title: 'Localización',
                                dataIndex: "location"
                            },
                            {
                                title: 'Actualizar análisis',
                                render: (_, record) => {return <PlusCircleOutlined onClick={() => handleNewAnalysis(record.stay_id)} />;}
                            }
                            
                        ]}
                        paginaion={{
                            pageSize: 5,
                        }}
                    >
                    </Table>}
                </Col>
                <Col>
                    <h1 className="fs-4 text-start">Usuarios</h1>
                        {(users.length !== 0) && <Table
                            loading = {loading}
                            dataSource={users}
                            columns={[
                                {
                                    title: 'Nombre de usuario',
                                    dataIndex: "username"
                                },
                                {
                                    title: 'Email',
                                    dataIndex: "email",
                                },
                                {
                                    title: 'Eliminar usuario',
                                    render: (_, record) => {
                                        if (!(record.is_staff)) {
                                            return <DeleteOutlined onClick={() => handleDeleteUser(record.user_id)} />;
                                        }
                                        else{
                                            return null;
                                        }
                                        // Si el usuario es administrador, no mostrar el ícono de eliminar
                                    }
                                    
                                },
                                
                            ]}
                            paginaion={{
                                pageSize: 5,
                            }}
                        >
                        </Table>}
                        
                </Col>
            </Row>
            <Row>
            <h1 className="fs-4 text-start">Solicitudes</h1>
                    {(users.length !== 0) && <Table
                        loading = {loading}
                        dataSource={requestedStays}
                        columns={[
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
                                title: 'Localización',
                                dataIndex: "location"
                            },
                            {
                                title: 'Realizar análisis',
                                render: (_, record) => {return <PlusCircleOutlined onClick={() => handleNewAnalysis(record.stay_id)} />;}
                            },
                            
                        ]}
                        paginaion={{
                            pageSize: 5,
                        }}
                    >
                    </Table>}
            </Row>
           

        </Container>        
    );


}

export default Admin;