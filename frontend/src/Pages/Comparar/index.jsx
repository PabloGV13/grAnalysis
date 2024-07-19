import { useEffect, useState } from "react";
import axios from 'axios';
import { Table, Checkbox } from "antd";
import Container from "react-bootstrap/esm/Container";
import { Link } from "react-router-dom";
import { FileSearchOutlined } from "@ant-design/icons";
import Button from "react-bootstrap/esm/Button";
import { useNavigate } from "react-router-dom";

function Comparar() {
    const [loading, setLoading] = useState(false);
    const [stays, setStays] = useState([]);
    const [selectedStays, setSelectedStays] = useState([]);
    const navigate = useNavigate()
    
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

    const handleStaySelection = (stayId) => {
        if (selectedStays.includes(stayId)) {
          setSelectedStays(selectedStays.filter((id) => id != stayId));
        } else {
          if(selectedStays.length < 2){
            setSelectedStays([...selectedStays,stayId]);
          }
        }
      };

    const handleClick = () => {
        if (selectedStays.length == 2){
            const [id1,id2] = selectedStays;
            if(id1 < id2){
                navigate("/comparar/"+id1+"/"+id2)
            }
            else{
                navigate("/comparar/"+id2+"/"+id1)
            }
        }
    };

    return(
        <Container className="m-auto" fluid style={{ padding: '20px' }}>
            <h1 className="fs-4 text-start">Selecciona dos alojamientos a comparar:</h1>
            {stays.length && <Table
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
                        title: 'Puntuación',
                        dataIndex: "polarity"
                    },
                    {
                        title: '',
                        dataIndex: "stay_id",
                        render: (stayId) => (
                            <Checkbox
                                checked={selectedStays.includes(stayId)}
                                onChange={() => handleStaySelection(stayId)}
                            >
                               <span class="visually-hidden">Label for the input</span>
                            </Checkbox>
                        ),
                    },
                ]}
                paginaion={{
                    pageSize: 5,
                }}
            >
            </Table>}

            <Button onClick={handleClick} disabled={selectedStays.length !== 2}>
                Comparar
            </Button>

            {/* {selectedStays} */}


        </Container>
    );


}

export default Comparar;