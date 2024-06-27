import React from "react";
import { useEffect, useState } from "react";
import axios from 'axios';
import Container from "react-bootstrap/esm/Container";
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { Link } from "react-router-dom";
import { FileSearchOutlined } from "@ant-design/icons";
import Button from "react-bootstrap/esm/Button";




function Mapa() {

    const ref = React.useRef();
    const [height, setHeight] = React.useState("0px");

    const onLoad = () => {
        setHeight(ref.current.contentWindow.document.body.scrollHeight + "px");
    };

    return(
        <iframe
            ref={ref}
            title="Mapa de Alojamientos"
            src="http://127.0.0.1:8000/api/stays/map"
            style={{width: "190vh ", overflow: "auto", height: "80vh"}}
        ></iframe>
    );


}

export default Mapa;