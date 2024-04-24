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
  
    var {firstStayId,secondStayId} = useParams();
  

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
    const [stay2, setStay2] = useState([]); 
    const [numbernights2, setnumberNigths2] = useState([]);
    const [clienttype2, setClientType2] = useState([]);
    const [latestReview2, setLatestReview2] = useState([]);
    const [oldestReview2, setOldestReview2] = useState([]);
    const [mostpositive2, setMostPositive2] = useState([]);
    const [mostnegative2, setMostNegative2] = useState([]);  
    const [positivewords2, setPositiveWords2] = useState([]);
    const [negativewords2, setNegativeWords2] = useState([]);
    const [bagofwords2, setBagOfWords2] = useState([]);
    
    useEffect(() => {

        console.log(secondStayId)
        Promise.all([
            axios.get('/api/stays/'+firstStayId),
            axios.get('/api/reviews/numbernights/'+firstStayId),
            axios.get('/api/reviews/clienttype/'+firstStayId),
            axios.get('/api/reviews/latest/'+firstStayId),
            axios.get('/api/reviews/oldest/'+firstStayId),
            axios.get('/api/reviews/mostpositive/'+firstStayId),
            axios.get('/api/reviews/mostnegative/'+firstStayId),
            axios.get('/api/keywords/toppolarity/'+firstStayId),
            axios.get('/api/keywords/lowestpolarity/'+ firstStayId),
            //axios.get('/api/keywords/bagofwords/'+stay_id.id)
            axios.get('/api/stays/'+secondStayId),
            axios.get('/api/reviews/numbernights/'+secondStayId),
            axios.get('/api/reviews/clienttype/'+secondStayId),
            axios.get('/api/reviews/latest/'+secondStayId),
            axios.get('/api/reviews/oldest/'+secondStayId),
            axios.get('/api/reviews/mostpositive/'+secondStayId),
            axios.get('/api/reviews/mostnegative/'+secondStayId),
            axios.get('/api/keywords/toppolarity/'+secondStayId),
            axios.get('/api/keywords/lowestpolarity/'+ secondStayId),
            //axios.get('/api/keywords/bagofwords/'+stay_id.id)
        ]).then(response => {
            const datas = response.map(r => r.data);
            console.log(datas);
            setStay1(datas[0]);
            setnumberNigths1(datas[1]);
            setClientType1(datas[2]);
            setLatestReview1(datas[3]);
            setOldestReview1(datas[4]);
            setMostPositive1(datas[5]);
            setMostNegative1(datas[6]);
            setPositiveWords1(datas[7]);
            setNegativeWords1(datas[8]);
            //setBagOfWords(datas[10]);
            setStay2(datas[9]);
            setnumberNigths2(datas[10]);
            setClientType2(datas[11]);
            setLatestReview2(datas[12]);
            setOldestReview2(datas[13]);
            setMostPositive2(datas[14]);
            setMostNegative2(datas[15]);
            setPositiveWords2(datas[16]);
            setNegativeWords2(datas[17]);
            //setBagOfWords(datas[10]);
           
            // setData(response.data);
        }).catch(error => {
            console.error('Error fetching data', error);
        })
    }, []);

    return(
        <Container>
            
            <Row>
                <Col>
                    <h1>{stay1.name}</h1>
                    <h1>{stay1.polarity} </h1>
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

                </Col>               
                <Col>
                    <h1>{stay2.name}</h1>
                    <h1>{stay2.polarity} </h1>
                    <div>
                        <h3>Numero de noches</h3>
                        <PieChart data={numbernights2}/>
                    </div>
                    <div>
                        <h3>Review mas reciente: </h3>
                        {latestReview2.costumer_name}: {latestReview2.comment}
                    </div>
                    <div>
                        <h3>Review mas positiva: </h3>
                        {mostpositive2.costumer_name}: {mostpositive2.comment}
                    </div>
                    <div>
                        <h3>Tipo de clientes</h3>
                        <PieChart data={clienttype2}/>
                    </div>
                    <div>
                        <h3>Review mas antigua: </h3>
                        {oldestReview2.costumer_name}: {oldestReview2.comment}
                    </div>
                    <div>
                        <h3>Review mas negativa: </h3>
                        {mostnegative2.costumer_name}: {mostnegative2.comment}
                    </div>

                </Col>
                
                
            </Row>
        </Container>
    );
}
export default Comparacion;