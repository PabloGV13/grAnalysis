import {} from "@ant-design/icons"
import {} from "antd"
import Container  from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import {  useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from 'axios';
import PieChart from "../../Components/Graphics/PieChart";
import randomcolor from 'randomcolor';
import { Pie } from "react-chartjs-2";
 
function Estadisticas(){
    const stay_id = useParams();
    const [stay, setStay] = useState([]); 
    const [numbernights, setnumberNigths] = useState([]);
    const [clienttype, setClientType] = useState([]);
    const [latestReview, setLatestReview] = useState([]);
    const [oldestReview, setOldestReview] = useState([]);
    const [mostpositive, setMostPositive] = useState([]);
    const [mostnegative, setMostNegative] = useState([]);  
    const [positivewords, setPositiveWords] = useState([]);
    const [negativewords, setNegativeWords] = useState([]);
    const [bagofwords, setBagOfWords] = useState([]);
    

    
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
                console.error('Error fetchin reviews', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/reviews/clienttype/'+stay_id.id)
            .then(response => {
                console.log(response)
                setClientType(response.data);
            })
            .catch(error => {
                console.error('Error fetchin reviews', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/reviews/latest/'+stay_id.id)
            .then(response => {
                console.log(response)
                setLatestReview(response.data);
            })
            .catch(error => {
                console.error('Error fetchin reviews', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/reviews/oldest/'+stay_id.id)
            .then(response => {
                console.log(response)
                setOldestReview(response.data);
            })
            .catch(error => {
                console.error('Error fetchin reviews', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/reviews/mostpositive/'+stay_id.id)
            .then(response => {
                console.log(response)
                setMostPositive(response.data);
            })
            .catch(error => {
                console.error('Error fetchin reviews', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/reviews/mostnegative/'+stay_id.id)
            .then(response => {
                console.log(response)
                setMostNegative(response.data);
            })
            .catch(error => {
                console.error('Error fetchin reviews', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/keywords/toppolarity/'+stay_id.id)
            .then(response => {
                console.log(response)
                setPositiveWords(response.data);
            })
            .catch(error => {
                console.error('Error fetchin keywords', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/keywords/lowestpolarity/'+stay_id.id)
            .then(response => {
                console.log(response)
                setNegativeWords(response.data);
            })
            .catch(error => {
                console.error('Error fetchin keywords', error);
            }); 
    }, []);

    useEffect(() => {
        axios.get('/api/keywords/bagofwords/'+stay_id.id)
            .then(response => {
                console.log(response)
                setBagOfWords(response.data);
            })
            .catch(error => {
                console.error('Error fetchin keywords', error);
            }); 
    }, []);



    return(
        
        <Container>
            <Row>
                <Col>
                <h1>{stay.name}</h1>
                {stay.polarity}
                </Col>
                <Col>
                    
                </Col>
            </Row>
            <Row>
                <Col>
                    <h3>Numero de noches</h3>
                    <PieChart data={numbernights}/>
                </Col>
                <Col>
                    <h3>Tipo de clientes</h3>
                    <PieChart data={clienttype}/>
                </Col>
            </Row>
            <Row>
                <Col>
                    <h3>Review mas reciente: </h3>
                    {latestReview.costumer_name}: {latestReview.comment}
                </Col>
                <Col>
                    <h3>Review mas antigua: </h3>
                    {oldestReview.costumer_name}: {oldestReview.comment}
                </Col>
            </Row>
            <Row>
                <Col>
                    <h3>Review mas positiva: </h3>
                    {mostpositive.costumer_name}: {mostpositive.comment}
                </Col>
                <Col>
                    <h3>Review mas negativa: </h3>
                    {mostnegative.costumer_name}: {mostnegative.comment}
                </Col>
            </Row>
            
        </Container>
    );


    
}
export default Estadisticas;


