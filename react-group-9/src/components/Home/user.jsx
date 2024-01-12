import React, { Component } from 'react';
import { useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Row, Container, Col} from "reactstrap"
import './homeCSS.css';
import CountButton from './CountButton';
import ClubDetailsBox from './ClubDetailsBox';
import Spacer from './Spacer';
import { useLocation } from 'react-router-dom';
import { Link } from "react-router-dom";
import AddManagerButton from './AddManager';
import TableComponent from './TableComponent';
import ReservationButton from './Reservation';



export default function User() {

  const location = useLocation();
  const [user, setUSer] = useState({
    email: location.state.email ,
    ID: location.state.ID 
  })

  const [clubs, setClubs] = useState([]);

  const [errors, setErrors] = useState({})

  function fetchData() {
        fetch('http://localhost:5000/clubs')
        .then((response) => 
          {
            if (response.status === 200)
                {return (response.json());}
            else
                {console.log("HTTP error:" + response.status + ":" +  response.statusText);
                return ([ ["status ", response.status]]);}
          }
          )//The promise response is returned, then we extract the json data
        .then((jsonOutput) => //jsonOutput now has result of the data extraction
              {
                setClubs(jsonOutput);
              }
        )
        .catch((error) => 
        {
            console.log(error);
            setClubs([]);
        })
      }

function addReservation (data1){
        const url = 'http://localhost:5000/clubs/reservations';
        fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify(data1)
        })
        .then(res => res.json())
        .then((data) => {updateState(); console.log(data); setErrors({'delReservation': "",'club':data1.club, 'makeReservation':data});})
        .catch(err => console.log(err));
  }


  function delReservation (data1){

    const url = 'http://localhost:5000/clubs/reservations';
    fetch(url, {
    method: 'DELETE',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json', 
      'email': data1.email,
      'date1': data1.date,
      'club': data1.club,
   
    },
    })
    .then(res => res.json())
    .then((data) => {updateState();setErrors({'delReservation': data, 'club':data1.club, 'makeReservation':""});})
    .catch(err => console.log(err));
}

  useEffect(() => {
      fetchData();
    }, []);


  function updateState(){
    fetchData();
  }
  

  
  function makeReservation(data){
    // console.log(data);
    var data_dic = {'club': data[0], 'email': user.email, 'date':data[1]};
    addReservation(data_dic);
  }

  function removeReservation(data){
    // console.log(data);
    var data_dic = {'club': data[0], 'email': user.email, 'date':data[1]};
    delReservation(data_dic);
  }

  
  if (clubs.length === 0){
    return (
      <Container>

    <Row xs="1" md="1">
      <Col  style={{ display: 'flex', justifyContent: 'flex-end' }} > 
        <Link to="/login" className="btn btn-default border w-15 bg-light" style={{ marginLeft: "auto" }} ><strong> Sign out </strong></Link>
      </Col>
    </Row>
      

  
      <Row xs="1" md="1">

        <h2> Not connected to database</h2>
  
      </Row>
        
    </Container>
    );
  }

  return (
    
  <Container>
    <Row xs="1" md="1">
      <Col  style={{ display: 'flex', justifyContent: 'flex-end' }} > 
        <Link to="/login" className="btn btn-default border w-15 bg-light" style={{ marginLeft: "auto" }} ><strong> Sign out </strong></Link>
      </Col>
    </Row>
      

    <Row xs="1" md="4">

      {clubs.map((club, i) => (
        
        <Col key={i}> 

          <ClubDetailsBox club={club} /> 
          <div >

            <ReservationButton  color='primary' title='Make Reservation' userselection={false} disable={false} url={'http://localhost:5000/clubs/entry/'+club[0]} club={club} handler={makeReservation} > Reservation </ReservationButton>
            {errors.makeReservation  && errors.club==club[0] && <span className="text-danger"> {errors.makeReservation} </span>}
            <Spacer height='1em'></Spacer>


            <ReservationButton  color='danger' title='Del Reservation' userselection={false} disable={false} url={'http://localhost:5000/clubs/entry/'+club[0]} club={club} handler={removeReservation} > Del Reservation </ReservationButton>
            {errors.delReservation   && errors.club==club[0] && <span className="text-danger"> {errors.delReservation} </span>}
            <Spacer height='3em'></Spacer>

          </div>
          

        </Col>
        ))
      }

    </Row>

  

  </Container>
  
  );
}
