import './App.css';
import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import PageContent from './Components/PageContent';
import SideMenu from './Components/SideMenu';
import { BrowserRouter } from "react-router-dom";
import { Alert } from 'react-bootstrap';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://127.0.0.1:8000";

function App() {

  const [currentUser, setCurrentUser] = useState(false);
  const [currentUserisAdmin, setCurrentUserAdmin] = useState(false)
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const handleClick = () => {
    setRegistrationToggle(!registrationToggle);
  };
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(null);

  useEffect(() => {
    {/* if(user.admin)*/}
    axios.get("/api/user")
    .then(function(res){
      if(res.data.user.is_staff && !currentUser){
        setCurrentUserAdmin(true)
      } else {
        setCurrentUserAdmin(false)
      };
      setCurrentUser(true);
    })
    .catch(function(error){
      setCurrentUser(false)
    })
  }, [])

    

  function sumbitRegistration(e) {
    e.preventDefault();
    axios.post(
      "/api/register",
      {
        email: email,
        username: username,
        password: password
      }
    ).then(function(res){
      axios.post(
        "/api/login",
        {
          email: email,
          password: password
        }
      ).then(function(res) {
        setCurrentUser(true)
        if(res.data.is_admin){
          setCurrentUserAdmin(true)
        }else{
          setCurrentUserAdmin(false)
        };       
      }).catch(function(error){
        const errorMessage = error.response?.data?.message || 'Correo invalido o ya registrado.';
        setMessage({ text: errorMessage, type: 'danger' });
    });
    });
  }

  function sumbitLogin(e) {
    e.preventDefault();
    {/* if(user.admin)*/}
    axios.post(
      "/api/login",
      {
        email: email,
        password: password
      }
    ).then(function(res) {
      setCurrentUser(true)
      console.log(res.data)
      if(res.data.is_admin){
        setCurrentUserAdmin(true)
      } else{
        setCurrentUserAdmin(false)
      };   
    }).catch(function(error){
      const errorMessage = error.response?.data?.message || 'Correo o contraseña incorrecta.';
      setMessage({ text: errorMessage, type: 'danger' });
  });

  }

  function sumbitLogout(e) {
    e.preventDefault();
    axios.post(
      "/api/logout",
      {withCredentials: true}
    ).then(function(res) {
      setCurrentUser(false);
    });
  }
  
  if (currentUser) {
    return (
      <div className="App">
        <Navbar bg="dark" variant='dark'>
          <Container>
            <Navbar.Brand>grAnalysis</Navbar.Brand>
            <Navbar.Toggle/>
            <Navbar.Collapse className="justify-content-end">
              <Navbar.Text>
                <form onSubmit={e => sumbitLogout(e)}>
                  <Button type="submit" vatiant="light">Cerrar sesión</Button>
                </form>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
          {currentUser && <div className="SideMenuAndPageContent">
            <BrowserRouter>
              <SideMenu isAdmin={currentUserisAdmin} />
              <PageContent/>
            </BrowserRouter>
          </div>}
      </div>
    );
  }
  return (
    <div>
    <Navbar bg="dark" variant= "dark">
      <Container>
        <Navbar.Brand>grAnalysis</Navbar.Brand>
        <Navbar.Toggle/>
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            <Button onClick={handleClick} variant="light">{ registrationToggle ? "Inicio de sesión" : "Registro"}</Button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>

    {message && (
      <Alert variant={message.type} onClose={() => setMessage(null)} dismissible>
          {message.text}
      </Alert>
    )}

    {registrationToggle ? (
        <div className="center">
          <Form onSubmit={e => sumbitRegistration(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Correo electrónico</Form.Label>
              <Form.Control type="email" placeholder="Introducir correo" value={email} onChange={e => setEmail(e.target.value)}/>
              <Form.Text className="text-muted">
                No se compartirá el correo con nadie.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicUsername">
              <Form.Label>Nombre de usuario</Form.Label>
              <Form.Control type="username" placeholder="Introducir usuario" value={username} onChange={e => setUsername(e.target.value)}/>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Contraseña</Form.Label>
              <Form.Control type="password" placeholder="Introducir contraseña" value={password} onChange={e => setPassword(e.target.value)}/>
            </Form.Group>
            <Button variant="secondary" type="submit">
              Registrar
            </Button>
          </Form>
        </div>

      ) : (
        <div className="center">
          <Form onSubmit={e => sumbitLogin(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Correo electrónico</Form.Label>
              <Form.Control type="email" placeholder="Introducir correo" value={email} onChange={e => setEmail(e.target.value)}/>
              <Form.Text className="text-muted">
                No se compartirá el correo con nadie.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Contraseña</Form.Label>
              <Form.Control type="password" placeholder="Introducir contraseña" value={password} onChange={e => setPassword(e.target.value)}/>
            </Form.Group>
            <Button variant="secondary" type="submit">
              Iniciar sesión
            </Button>
          </Form>
        </div>
        
      )
      
    }
    </div>
  );

  
}

export default App;
