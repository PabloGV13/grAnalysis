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

function Comparacion() {
  
    const firstStayId = useParams();
    const [stay1, setStay1] = useState([]); 
    const [numbernights1, setnumberNigths1] = useState([]);
    const [clienttype1, setClientType1] = useState([]);
    const [latestReview1, setLatestReview1] = useState([]);
    const [oldestReview1, setOldestReview1] = useState([]);
    const [mostpositive1, setMostPositive1] = useState([]);
    const [mostnegative1, setMostNegative1] = useState([]);  
    const [positivewords1, setPositiveWords1] = useState([]);
    const [negativewords1, setNegativeWords1] = useState([]);
    const [bagofwords1, setBagOfWords1] = useState([]);
    
    useEffect(() => {
        Promise.all([
            axios.get('/api/stays/'+firstStayId.id),
            axios.get('/api/reviews/numbernights/'+firstStayId.id),
            axios.get('/api/reviews/clienttype/'+firstStayId.id),
            axios.get('/api/reviews/latest/'+firstStayId.id),
            axios.get('/api/reviews/oldest/'+firstStayId.id),
            axios.get('/api/reviews/mostpositive/'+firstStayId.id),
            axios.get('/api/reviews/mostnegative/'+firstStayId.id),
            axios.get('/api/keywords/toppolarity/'+firstStayId.id),
            axios.get('/api/keywords/lowestpolarity/'+firstStayId.id),
            //axios.get('/api/keywords/bagofwords/'+stay_id.id)
        ]).then(response => {
            const datas = response.map(r => r.data);
            setStay1(datas[0]);
            console.log(datas);
            setnumberNigths1(datas[1]);
            setClientType1(datas[2]);
            setLatestReview1(datas[3]);
            setOldestReview1(datas[4]);
            setMostPositive1(datas[5]);
            setMostNegative1(datas[6]);
            setPositiveWords1(datas[7]);
            setNegativeWords1(datas[8]);
            //setBagOfWords(datas[10]);
           
            // setData(response.data);
        }).catch(error => {
            console.error('Error fetching data', error);
        })
    }, []);

    return(
        <Container>
            <h1>{stay1.name}</h1>
            {/* {stay.polarity} */}
            <Row>
                <Col>
                    <Stack>
                        <div>
                            <h3>Numero de noches</h3>
                            <PieChart data={numbernights1}/>
                        </div>
                        <div>
                            <h3>Review mas reciente: </h3>
                            {latestReview1.costumer_name}: {latestReview1.comment}
                        </div>
                        <div>
                            <h3>Review mas positiva: </h3>
                            {mostpositive1.costumer_name}: {mostpositive1.comment}
                        </div>
                        <div>
                            <h3>Tipo de clientes</h3>
                            <PieChart data={clienttype1}/>
                        </div>
                        <div>
                            <h3>Review mas antigua: </h3>
                            {oldestReview1.costumer_name}: {oldestReview1.comment}
                        </div>
                        <div>
                            <h3>Review mas negativa: </h3>
                            {mostnegative1.costumer_name}: {mostnegative1.comment}
                        </div>

                    </Stack>
                </Col>
                
            </Row>
        </Container>
    );
}
export default Comparacion;