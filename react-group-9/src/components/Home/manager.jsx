import React, { Component } from 'react';
import { useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Row, Container, Col} from "reactstrap"
import './homeCSS.css';
import ClubDetailsBox from './ClubDetailsBox';
import Modify from './ModifyClub';
import Spacer from './Spacer';
import { useLocation } from 'react-router-dom';
import { Link } from "react-router-dom";
import AddManagerButton from './AddManager';
import DelBouncerButton from './DelBouncer';
import TableComponent from './TableComponent';




export default function Manager() {

  const location = useLocation();
  const [manager, setManager] = useState({
    email: location.state.email ,
    ID: location.state.ID 
  })

  const [clubs, setClubs] = useState([]);

  const [errors, setErrors] = useState({})

  function fetchData() {
        fetch('http://localhost:5000/managers/'+manager.email)
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
                // setURLBouncer('http://localhost:5000/bouncers/'+jsonOutput[0][0])
              }
        )
        .catch((error) => 
        {
            console.log(error);
            setClubs([]);
        })  
      }

  function putData (olddata, newdata){
        const url = 'http://localhost:5000/clubs/'+olddata['name'] ;
        fetch(url, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json', 
          'manager_email': manager.email, 
          'session_id' : manager.ID.toString()
        },
        body: JSON.stringify(newdata)
        })
        .then(res => res.json())
        .then((data) => {updateState(); setErrors({'modify': data});})
        .catch(err => console.log(err));
  }

  function postBouncer(club) {
    fetch('http://localhost:5000/bouncers', {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'manager_email': manager.email, 
      'session_id' : manager.ID.toString()
    },
    body: JSON.stringify(club)
    })
    .then(res => res.json())
    .then((data) => { updateState(); setErrors({'addBouncer': data, 'delBouncer':''});})
    .catch(err => console.log(err));}


    var delBouncerdb = (data) => {
      const url = 'http://localhost:5000/bouncers'
      fetch(url, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'manager_email': manager.email, 
        'session_id' : manager.ID.toString(),
        'email': data[1]
      }
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

  function addBouncer(data){
    // console.log(data);
    var data_dic = {'club': data[0], 'email': data[1]}
    postBouncer(data_dic);
  }

  function delBouncer(data){
    delBouncerdb(data);
  }

  

  function updateClubInfo(oldClubInfo, newClubInfo){
    setErrors({'modify': ""})
    if (newClubInfo[5] >= newClubInfo[3]){
      newClubInfo[6]= true
    }
    else{
      newClubInfo[6]= false
    }
    if (newClubInfo[5] <= 0){
      newClubInfo[7]= true
    }
    else{
      newClubInfo[7]= false
    }
    var olddata = getObject(oldClubInfo)
    var newdata = getObject(newClubInfo)
    putData(olddata,newdata)
  }

  
  
  if (clubs.length === 0){
    return (
      <Container>

    <Row>
      <Col style={{ display: 'flex', justifyContent: 'flex-end' }}> 
        <Link to="/login" className="btn btn-default border w-15 bg-light" style={{ marginLeft: "auto" }}><strong> Sign out </strong></Link>
      </Col>
    </Row>

      <Row xs="1" md="1">

        <h2> Not able to connect to database</h2>

      </Row>        
    </Container>
    );
  }

  return (
    
    
  <Container>
    <Row>
      <Col style={{ display: 'flex', justifyContent: 'flex-end' }}> 
        <Link to="/login" className="btn btn-default border w-15 bg-light" style={{ marginLeft: "auto" }}><strong> Sign out </strong></Link>
      </Col>
    </Row>


    <Row xs="1" md="4">
      {clubs.map((club, i) => (
        
        <Col key={i}> 

          <ClubDetailsBox club={club} /> 
          <div >
            <Modify club={club} handler={updateClubInfo}> </Modify>
            {errors.modify && <span className="text-danger"> {errors.modify} </span>}
            <Spacer height='1em'></Spacer>

            <AddManagerButton  color='primary' title='Add Bouncer' index={3} url='http://localhost:5000/users' club={club} handler={addBouncer} > Add Bouncer</AddManagerButton>
            {errors.addBouncer  && <span className="text-danger"> {errors.addBouncer} </span>}
            <Spacer height='1em'></Spacer>


            <DelBouncerButton color='danger' club={club} handler={delBouncer} url={'http://localhost:5000/bouncers/'+club[0]} >
               Del Bouncer
            </DelBouncerButton>
            {errors.delBouncer && <span className="text-danger"> {errors.delBouncer} </span>}
            <Spacer height='3em'></Spacer>

          </div>
          
        </Col>
        ))
      }

    </Row>

    <Row xs="1" md="1">
      <Col >
        <TableComponent url={'http://localhost:5000/bouncers/'+clubs[0][0]} coloumn1='Club' coloumn2='Bouncers'>Club's Bouncers</TableComponent>
        <Spacer height='3em'></Spacer>
      </Col>
    </Row>




  </Container>
  
  );
}
