import {} from "@ant-design/icons"
import {} from "antd"
import Container  from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/Row"
import Col from "react-bootstrap/Col"
import Stack from "react-bootstrap/Stack"
import {  useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from 'axios';
import PieChart from "../../Components/Graphics/PieChart";
import randomcolor from 'randomcolor';
import { Pie } from "react-chartjs-2";
import PolarityRating from '../../Components/Graphics/PolarityRating';
import './styles.css';
 
function Estadisticas(){
    const stay_id = useParams();
    const [stay, setStay] = useState([]); 
    const ratingStar = stay.polarity * 5;
    const [numbernights, setnumberNigths] = useState([]);
    const [clienttype, setClientType] = useState([]);
    const [latestReview, setLatestReview] = useState([]);
    const [oldestReview, setOldestReview] = useState([]);
    const [mostpositive, setMostPositive] = useState([]);
    const [mostnegative, setMostNegative] = useState([]);  
    const [positivewords, setPositiveWords] = useState([]);
    const [negativewords, setNegativeWords] = useState([]);
    const [bagofwords, setBagOfWords] = useState([]);
    //const [data, setData] = useState([]);

    const polarity = stay.polarity != null ? stay.polarity : 0
    
    useEffect(() => {
        Promise.all([
            axios.get('/api/stays/'+stay_id.id),
            axios.get('/api/reviews/numbernights/'+stay_id.id),
            axios.get('/api/reviews/clienttype/'+stay_id.id),
            axios.get('/api/reviews/latest/'+stay_id.id),
            axios.get('/api/reviews/oldest/'+stay_id.id),
            axios.get('/api/reviews/mostpositive/'+stay_id.id),
            axios.get('/api/reviews/mostnegative/'+stay_id.id),
            axios.get('/api/keywords/toppolarity/'+stay_id.id),
            axios.get('/api/keywords/lowestpolarity/'+stay_id.id),
            axios.get('/api/keywords/bagofwords/'+stay_id.id)
        ]).then(response => {
            const datas = response.map(r => r.data);
            setStay(datas[0]);
            console.log(datas);
            setnumberNigths(datas[1]);
            setClientType(datas[2]);
            setLatestReview(datas[3]);
            setOldestReview(datas[4]);
            setMostPositive(datas[5]);
            setMostNegative(datas[6]);
            setPositiveWords(datas[7]);
            setNegativeWords(datas[8]);
            setBagOfWords(datas[9]);
           
            // setData(response.data);
        }).catch(error => {
            console.error('Error fetching data', error);
        })
    }, []);
    
    // useEffect(() => {
    //     axios.get('/api/stays/'+ stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setStay(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin stay', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/reviews/numbernights/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setnumberNigths(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin reviews', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/reviews/clienttype/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setClientType(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin reviews', error);
    //         });
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/reviews/latest/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setLatestReview(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin reviews', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/reviews/oldest/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setOldestReview(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin reviews', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/reviews/mostpositive/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setMostPositive(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin reviews', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/reviews/mostnegative/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setMostNegative(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin reviews', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/keywords/toppolarity/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setPositiveWords(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin keywords', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/keywords/lowestpolarity/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setNegativeWords(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin keywords', error);
    //         }); 
    // }, []);

    // useEffect(() => {
    //     axios.get('/api/keywords/bagofwords/'+stay_id.id)
    //         .then(response => {
    //             console.log(response);
    //             setBagOfWords(response.data);
    //         })
    //         .catch(error => {
    //             console.error('Error fetchin keywords', error);
    //         }); 
    // }, []);

    return(
        <Container fluid style={{ padding: '20px' }}>
            <h1>{stay.name}</h1>
            <PolarityRating polarity={polarity} />
            <Row style ={{ alignItems : 'stretch'}}>
                <Col>
                    <Stack>
                        <div className="chart-section">
                            <h3>Número de noches</h3>
                            <PieChart align="center" data={numbernights}/>
                        </div>
                        <div className="chart-section">
                            <h3>Comentario más reciente: </h3>
                            {latestReview.costumer_name}: {latestReview.comment}
                        </div>
                        <div className="chart-section">
                            <h3>Comentario más positivo: </h3>
                            {mostpositive.costumer_name}: {mostpositive.comment}
                        </div>
                        <div className="chart-section">
                            <h3>Palabras más positivas: </h3>
                            <ul className="chart-list">
                                {positivewords.map((positiveword, index) => (
                                    <li key={index}>{positiveword.word}: {positiveword.polarity}</li>
                                ))}
                            </ul>
                        </div>
                    </Stack>
                </Col>
                <Col>
                    <Stack>
                        <div className="chart-section">
                            <h3>Tipo de clientes</h3>
                            <PieChart data={clienttype}/>
                        </div>
                        <div className="chart-section">
                            <h3>Comentario más antiguo: </h3>
                            {oldestReview.costumer_name}: {oldestReview.comment}
                        </div>
                        <div className="chart-section">
                            <h3>Comentario más negativo: </h3>
                            {mostnegative.costumer_name}: {mostnegative.comment}
                        </div>
                        <div className="chart-section">
                            <h3>Palabras más negativas: </h3>
                            <ul className="chart-list">
                                {negativewords.map((negativeword, index) => (
                                    <li key={index}>{negativeword.word}: {negativeword.polarity}</li>
                                ))}
                            </ul>
                        </div>
                    </Stack>
                </Col>
            </Row>
            <Row>
                <h3>Palabras más frecuentes: </h3>
                <ul className="chart-list">
                    {bagofwords.map((keyword, index) => (
                        <li key={index}>{keyword.word}: {keyword.frecuency + 1}</li>
                    ))}
                </ul>
            </Row>
            {/* <Row>
                <Col>
                    <h3>Numero de noches</h3>
                    <PieChart data={numbernights}/>
                </Col>
                <Col>
                    <h3>Tipo de clientes</h3>
                    <PieChart data={clienttype}/>
                </Col>
            </Row> */}
            {/* <Row>
                <Col>
                    <h3>Review mas reciente: </h3>
                    {latestReview.costumer_name}: {latestReview.comment}
                </Col>
                <Col>
                    <h3>Review mas antigua: </h3>
                    {oldestReview.costumer_name}: {oldestReview.comment}
                </Col>
            </Row> */}
            {/* <Row>
                <Col>
                    <h3>Review mas positiva: </h3>
                    {mostpositive.costumer_name}: {mostpositive.comment}
                </Col>
                <Col>
                    <h3>Review mas negativa: </h3>
                    {mostnegative.costumer_name}: {mostnegative.comment}
                </Col>
            </Row>
            <Row>
                <Col>
                
                </Col>
                <Col>
                </Col>
            </Row>  */}


            
        </Container>
    );


    
}
export default Estadisticas;


