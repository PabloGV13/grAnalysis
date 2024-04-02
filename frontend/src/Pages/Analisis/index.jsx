import { useEffect, useState } from "react";
import axios from 'axios';
import { Table } from "antd";
import Container from "react-bootstrap/esm/Container";
import Modal from 'react-bootstrap/Modal';
import { Link } from "react-router-dom";
import { FileSearchOutlined } from "@ant-design/icons";
import Button from "react-bootstrap/esm/Button";

function Analisis() {
    const [loading, setLoading] = useState(false);
    const [stays, setStays] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [newStayURL, setnewStayURL] = useState(); 

    const handleCloseForm = () => setShowForm(false);
    const handleShowForm = () => setShowForm(true);

    const handleSaveStay = () => {
        axios.post('/api/stays/post_request_stay', {url: newStayURL})
        .then(response => {
            console.log("Alojamiento solicitado correctamente:", response.data);
            handleCloseForm();
        })
        .catch(error => {
            console.error('Error requesting stay:', error);
        });
    }

    useEffect(() => {
        setLoading(true)
        axios.get('/api/stays')
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
                        title: 'Puntucación',
                        dataIndex: "polarity"
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
            
            <Button onClick={handleShowForm}>
            Solicitar nuevo alojamiento
            </Button>

            <Modal show={showForm} onHide={handleCloseForm} animation={false} aria-labelledby="contained-modal-title-vcenter"
            centered>
                <Modal.Header closeButton>
                    <Modal.Title>Nuevo alojamiento</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Escriba a continuación la URL de booking del alojamiento a analizar:
                    <br></br>
                    <br></br>
                    <input type="text" value={newStayURL} onChange={(e) => setnewStayURL(e.target.value)} style={{width: "460px"}}/>
                </Modal.Body>
                <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseForm}>
                    Close
                </Button>
                <Button variant="primary" onClick={handleSaveStay}>
                    Solicitar
                </Button>
                </Modal.Footer>
            </Modal>

        </Container>
    );


}

export default Analisis;