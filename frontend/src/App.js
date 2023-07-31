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

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;
axios.defaults.baseURL = "http://127.0.0.1:8000";

function App() {

  const [currentUser, setCurrentUser] = useState(false);
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const handleClick = () => {
    setRegistrationToggle(!registrationToggle);
  };
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    {/* if(user.admin)*/}
    axios.get("/api/user")
    .then(function(res){
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
      setCurrentUser(true);
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
                  <Button type="submit" vatiant="light">Log out</Button>
                </form>
              </Navbar.Text>
            </Navbar.Collapse>
          </Container>
        </Navbar>
          {currentUser && <div className="SideMenuAndPageContent">
            {/*PAGINA PRINCIPAL DEL USUARIO*/}
            <BrowserRouter>
              <SideMenu></SideMenu>
              <PageContent></PageContent> 
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
            <Button onClick={handleClick} variant="light">{ registrationToggle ? "Login" : "Register"}</Button>
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
    {
      registrationToggle ? (
        <div className="center">
          <Form onSubmit={e => sumbitRegistration(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)}/>
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicUsername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="username" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)}/>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)}/>
            </Form.Group>
            <Button variant="priamry" type="submit">
              Register
            </Button>
          </Form>
        </div>

      ) : (
        <div className="center">
          <Form onSubmit={e => sumbitLogin(e)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)}/>
              <Form.Text className="text-muted">
                We'll never share your email with anyone else.
              </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)}/>
            </Form.Group>
            <Button variant="priamry" type="submit">
              Login
            </Button>
          </Form>
        </div>
        
      )
      
    }
    </div>
  );

  
}

export default App;
