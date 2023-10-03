import {} from "@ant-design/icons"
import {} from "antd"
import Container  from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import {  useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from 'axios';
 
function Estadisticas(){
    const stay_id = useParams();
    const [stay, setStay] = useState([])
    const [numbernights, setnumberNigths] = useState([])

    useEffect(() => {
        axios.get('/api/stays/'+stay_id.id)
            .then(response => {
                console.log(response)
                setStay(response.data);
            })
            .catch(error => {
                console.error('Error fetchin stay', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/reviews/numbernights/'+stay_id.id)
            .then(response => {
                console.log(response)
                setnumberNigths(response.data);
            })
            .catch(error => {
                console.error('Error fetchin stay', error);
            }); 
    }, []);


    return(
        
        <Container>
            <Row>
                <Col>{stay.name}</Col>
                <Col>
                    <canvas id="labelChart"></canvas>
                </Col>
            </Row>
            <Row>
                <Col>{stay.polarity}</Col>
                <Col>2 of 3</Col>
            </Row>
        </Container>
    );


    
}
export default Estadisticas;


