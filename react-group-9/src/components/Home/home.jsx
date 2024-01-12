import React, { Component } from 'react';
import { useState, useEffect} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Row, Container, Col} from "reactstrap"
import './homeCSS.css';
import CountButton from './CountButton';
import ClubDetailsBox from './ClubDetailsBox';
import Modify from './ModifyClub';
import DeleteButton from './DeleteClub';
import AddButton from './AddClub';
import Spacer from './Spacer';
import FilterButton from './FilterButton';
import { useLocation } from 'react-router-dom';
import Sidebar from '../NavBar/Sidebar';



export default function Home() {

  const [clubs, setClubs] = useState([]);

  const [FilterClubs, setFilterClubs] = useState([]);

  const [selectedClub, setSelectedClub] = useState("All");

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
                filter(jsonOutput, selectedClub)
              }
        )
        .catch((error) => 
        {
            console.log(error);
            setClubs([]);
            filter(clubs, selectedClub);
        })
    
      }

  function postData(club) {
        fetch('http://localhost:5000/clubs', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(club)
        })
        .then(res => res.json())
        .then((data) => { updateState();})
        .catch(err => console.log(err));
    }

  function putData (olddata, newdata){
        const url = 'http://localhost:5000/clubs/'+olddata['name'] ;
        fetch(url, {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newdata)
        })
        .then(res => res.json())
        .then((data) => { updateState();  })
        .catch(err => console.log(err));
  }

  var DelData = (clubname) => {
        const url = 'http://localhost:5000/clubs/' +clubname
        fetch(url, {
        method: 'DELETE',
      })
      .then(res => res.json())
      .then((data) => { updateState();})
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

  
  function handleIncrement(club){
    var nextClubs = clubs.slice();
    const index = nextClubs.indexOf(club);
    if (nextClubs[index][5] < nextClubs[index][3]){
      nextClubs[index][5] = nextClubs[index][5] +1;
    }
    nextClubs[index] = disableIncrement(nextClubs[index]);
    nextClubs[index] = disableDecrement(nextClubs[index]);
    putData(getObject(clubs[index]),getObject(nextClubs[index]));

  };

  function handleDecrement(club){

    var nextClubs = clubs.slice();
    const index = nextClubs.indexOf(club)

    if (nextClubs[index][5] > 0){
      nextClubs[index][5] = nextClubs[index][5] -1;
    }
    nextClubs[index] = disableIncrement(nextClubs[index]);
    nextClubs[index] = disableDecrement(nextClubs[index]);
    putData(getObject(clubs[index]),getObject(nextClubs[index]));

  };

  function updateClubInfo(oldClubInfo, newClubInfo){
    if (newClubInfo[5] >= newClubInfo[3]){
      newClubInfo[6]= true
    }
    if (newClubInfo[5] <= 0){
      newClubInfo[7]= true
    }
    var olddata = getObject(oldClubInfo)
    var newdata = getObject(newClubInfo)
    putData(olddata,newdata)
  }

  function deleteClub(club){
    DelData(club[0]);
  }

  function addClub(club){
    var data = getObject(club)
    postData(data);
  }

  function filter(allClubs, location){
    if (location === 'All'){
      setFilterClubs(allClubs);
    }
    else {
      var filterClub =[];
      for (let i = 0; i < allClubs.length; i++) {
        if (allClubs[i][1] === location){
          filterClub.push(allClubs[i])
        }
      }
      setFilterClubs(filterClub);
    }

  }

  function setSelectedLocation(location){
    setSelectedClub(location);
    filter(clubs,location);
  }

  
  if (clubs.length === 0){
    return (
      <Container>
        <Sidebar/>

      <Row xs="1" md="1">
        <FilterButton handler={setSelectedLocation}> </FilterButton>
      </Row>
  
      <Row xs="1" md="1">

        <h2> Not able to connect to database</h2>
  
      </Row>
  
      <Spacer height="3rem"> </Spacer>
  
      <Row xs="1" md="1">
  
        <Col>
          <AddButton handler={addClub} ></AddButton>
        </Col>
      </Row>
        
    </Container>
    );
  }

  return (
    
  <Container>
    
    <Sidebar/>

    <Row xs="1" md="1">
      <FilterButton handler={setSelectedLocation}> </FilterButton>
    </Row>

    <Row xs="1" md="4">

      {FilterClubs.map((club, i) => (
        
        <Col key={i}> 

          <ClubDetailsBox club={club} /> 
          <div className="d-flex justify-content-between button">
            <CountButton color="success" disable={club[6]} handler={() =>handleIncrement(club)} >+</CountButton>
            <Modify club={club} handler={updateClubInfo}> </Modify>
            <CountButton color="danger" disable={club[7]} handler={() =>handleDecrement(club)}>-</CountButton>
          </div>
          
          <div style={{paddingTop:'5px', paddingBottom:'5px'}}>
          <DeleteButton color="secondary" club={club} handler={deleteClub}>Delete</DeleteButton>
          </div>

        </Col>
        ))
      }

    </Row>

    <Spacer height="3rem"> </Spacer>

    <Row xs="1" md="1">

      <Col>
        <AddButton handler={addClub} ></AddButton>
      </Col>
    </Row>
      
  </Container>
  
  );
}
