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
import RemoveCustomerButton from './RemoveCustomer';



export default function Customer() {

  const location = useLocation();
  const [customer, setCustomer] = useState({
    email: location.state.email ,
    ID: location.state.ID 
  })

  const [clubs, setClubs] = useState([]);

  const [errors, setErrors] = useState({})

  function fetchData() {
        fetch('http://localhost:5000/customers/'+customer.email)
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

      function putData (newdata){
        const url = 'http://localhost:5000/customers/leave';
        fetch(url, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify(newdata)
        })
        .then(res => res.json())
        .then((data) => {updateState(); console.log(data);setErrors({'modify': data});})
        .catch(err => console.log(err));
  }



    var delCustomerdb = (data) => {
      const url = 'http://localhost:5000/clubs/entry'
      fetch(url, {
      method: 'PUT',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
      },
      body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then((data) => { updateState(); console.log(data); setErrors({'addBouncer': "", 'delBouncer':data});})
    .catch((err) => {console.log(err);});
  }


  function getObject(club){
    var data = {'name':club[0], 
    'city':club[1], 
    'music':club[2], 
    'capacity':club[3], 
    'yellow_threshold':club[4], 
    'count':club[5], 
    'increment':club[6], 
    'decrement':club[7]};
    
    return data;
  }

  useEffect(() => {
      fetchData();
    }, []);


  function updateState(){
    fetchData();
  }
  

  function disableIncrement(club){
    var nextClubs = clubs.slice();
    const index = clubs.indexOf(club)

    if (nextClubs[index][5] < nextClubs[index][3]){
      nextClubs[index][6] = false;
    }

    if (nextClubs[index][5] === nextClubs[index][3]){
      nextClubs[index][6] = true;
    }
    return nextClubs[index]
  };

  function disableDecrement(club){
    var nextClubs = clubs.slice();
    const index = clubs.indexOf(club)

    if (nextClubs[index][5] >0){
      nextClubs[index][7] = false;
    }

    if (nextClubs[index][5] === 0){
      nextClubs[index][7] = true;
    }
    return nextClubs[index]

  };

  
  function handleDecrement(club){

    var nextClubs = clubs.slice();
    const index = nextClubs.indexOf(club)

    if (nextClubs[index][5] > 0){
      nextClubs[index][5] = nextClubs[index][5] -1;
    }
    nextClubs[index] = disableIncrement(nextClubs[index]);
    nextClubs[index] = disableDecrement(nextClubs[index]);
    putData(getObject(nextClubs[index]));

  };

  function delCustomer(data){
    // console.log(data);
    handleDecrement(clubs[0]);
    var data_dic = {'club': data[0], 'email': customer.email, 'amount_spent':data[2]};
    delCustomerdb(data_dic);
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

        <h2> Not present in any club</h2>
  
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

            <RemoveCustomerButton  color='danger' userselection={false} disable={false} url={'http://localhost:5000/clubs/entry/'+club[0]} club={club} handler={delCustomer} > Pay and Leave</RemoveCustomerButton>
            {errors.delCustomer  && <span className="text-danger"> {errors.delCustomer} </span>}
            <Spacer height='3em'></Spacer>

          </div>
          

        </Col>
        ))
      }

    </Row>

  

  </Container>
  
  );
}
