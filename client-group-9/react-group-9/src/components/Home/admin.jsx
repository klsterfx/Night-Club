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
import AddManagerButton from './AddManager';
import DelManagerButton from './DelManager';
import TableComponent from './TableComponent';
import Spacer from './Spacer';
import FilterButton from './FilterButton';
import { useLocation } from 'react-router-dom';
import { Link } from "react-router-dom";




export default function Admin() {

  const location = useLocation();
  const [admin, setAdmin] = useState({
    email: location.state.email ,
    ID: location.state.ID 
  })

  const [errors, setErrors] = useState({})

  const [clubs, setClubs] = useState([]);

  const [minValue, setMinValue] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedPopulation, setSelectedPopulation] = useState('');

  var data = {'date':'', 'club':'', 'population':''}


  const [FilterClubs, setFilterClubs] = useState([]);

  const [FilterClubsEarning, setFilterClubsEarnings] = useState([]);

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


    function fetchFilteredData(data) {
      fetch('http://localhost:5000/clubs/filterAll', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
      })
      .then(res => res.json())
      .then((data) => { setClubs(data); filter(data, selectedClub);})
      .catch(err => console.log(err));
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
        .then((data) => { updateState(); setErrors({'addClub': data})})
        .catch(err => console.log(err));
    }

function postManager(club) {
      fetch('http://localhost:5000/managers', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(club)
      })
      .then(res => res.json())
      .then((data) => { updateState(); setErrors({'addManager': data, 'club':club.club, 'delManager':""});})
      .catch(err => console.log(err));
  }

  var DelData = (clubname) => {
        const url = 'http://localhost:5000/clubs/' +clubname
        fetch(url, {
        method: 'DELETE',
      })
      .then(res => res.json())
      .then((data) => { updateState();  setErrors({'addClub': data})})
      .catch((err) => {console.log(err);});
    }

    var delManagerdb = (clubname) => {
      const url = 'http://localhost:5000/managers'
      fetch(url, {
      method: 'DELETE',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'clubname': clubname
      }
    })
    .then(res => res.json())
    .then((data) => { updateState(); setErrors({'addManager': "", 'club':clubname, 'delManager':data});})
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
      fetchData()
      // fetchFilteredData(data)
    },[]);


  function updateState(){
    // fetchData();
    var data = {'date':selectedDate, 'earning':minValue, 'population':selectedPopulation}
    fetchFilteredData(data)
  }
  

  function deleteClub(club){
    DelData(club[0]);
  }

  function addClub(club){
    var data = getObject(club)
    postData(data);
  }


  function addManager(data){
    // console.log(data);
    var data_dic = {'club': data[0], 'email': data[1]}
    postManager(data_dic);
  }

  function delManager(data){
    delManagerdb(data);
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
      // setFilterClubsEarnings(filterClub)
    }

  }

  function setSelectedLocation(location){
    setSelectedClub(location);
    filter(clubs,location);
  }


  const handleMinValueChange = (e) => {
    setMinValue(e.target.value);
  };

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const handlePopulationChange = (e) => {
    setSelectedPopulation(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    var data = {'date':selectedDate, 'earning':minValue, 'population':selectedPopulation}
    fetchFilteredData(data);
  };

  
  if (clubs.length === 0){
    return (
      <Container>

    <Row>
      <Col style={{ display: 'flex', justifyContent: 'flex-end' }}> 
        <Link to="/login" className="btn btn-default border w-15 bg-light" style={{ marginLeft: "auto" }}><strong> Sign out </strong></Link>
      </Col>
    </Row>

      <Row xs="1" md="1">
        <FilterButton handler={setSelectedLocation}> </FilterButton>
     
    </Row>
    <Row xs="1" md="4">
        <form onSubmit={handleSubmit} className="filter-form">
        <div className="form-group">
          <label htmlFor="minValue">Minimum Earning:</label>
          <input
            type="number"
            value={minValue}
            onChange={handleMinValueChange}
            id="minValue"
          />
        </div>
        <div className="form-group">
          <label htmlFor="selectedPopulation">Minimum Population:</label>
          <input
            type="number"
            value={selectedPopulation}
            onChange={handlePopulationChange}
            id="selectedPopulation"
          />
        
      </div>

        <div className="form-group">
          <label htmlFor="selectedDate">Date:</label>
          <input
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            id="selectedDate"
          />
        
        <button type="submit">Filter</button>

        </div>
      </form>
    </Row>



      <Row xs="1" md="1">

        <h2> Not data to show </h2>
  
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

    <Row>
      <Col style={{ display: 'flex', justifyContent: 'flex-end' }}> 
        <Link to="/login" className="btn btn-default border w-15 bg-light" style={{ marginLeft: "auto" }}><strong> Sign out </strong></Link>
      </Col>
    </Row>

    <Row xs="1" md="2">
      <Col> <FilterButton index={0} handler={setSelectedLocation}> </FilterButton> </Col>

    </Row>
    <Row xs="1" md="4">
        <form onSubmit={handleSubmit} className="filter-form">
        <div className="form-group">
          <label htmlFor="minValue">Minimum Earning:</label>
          <input
            type="number"
            value={minValue}
            onChange={handleMinValueChange}
            id="minValue"
          />
        </div>
        <div className="form-group">
          <label htmlFor="selectedPopulation">Minimum Population:</label>
          <input
            type="number"
            value={selectedPopulation}
            onChange={handlePopulationChange}
            id="selectedPopulation"
          />
        
      </div>

        <div className="form-group">
          <label htmlFor="selectedDate">Date:</label>
          <input
            type="date"
            value={selectedDate}
            onChange={handleDateChange}
            id="selectedDate"
          />
        
        <button type="submit">Filter</button>

        </div>
      </form>
    </Row>


    <Row xs="1" md="4">

      {FilterClubs.map((club, i) => (
        
        <Col key={i}> 

          <ClubDetailsBox club={club} /> 
          
          <div style={{paddingTop:'5px', paddingBottom:'5px'}}>

          <DeleteButton color="danger" club={club} handler={deleteClub}>Delete Club</DeleteButton>
          <Spacer height='1em'></Spacer>

          <AddManagerButton  color='primary' index={3} title='Add Manager' url='http://localhost:5000/users' club={club} handler={addManager}>Add Manager</AddManagerButton>
          {errors.addManager && errors.club===club[0] && <span className="text-danger"> {errors.addManager} </span>}
          <Spacer height='1em'></Spacer>

          <DelManagerButton club={club} handler={delManager} >Delete Manager </DelManagerButton>
          {errors.delManager && errors.club===club[0] && <span className="text-danger"> {errors.delManager} </span>}
          <Spacer height='1em'></Spacer>

          </div>

        </Col>
        ))
      }

    </Row>

    <Spacer height="3rem"> </Spacer>

    <Row xs="1" md="1">

      <Col>
        <AddButton handler={addClub} ></AddButton>
        {errors.addClub  && <span className="text-danger"> {errors.addClub} </span>}
        <Spacer height='3em'></Spacer>
      </Col>
    </Row>

    <Row xs="1" md="1">
      <Col>
        <TableComponent url='http://localhost:5000/managers' coloumn1='Club' coloumn2='Manager'>Club's Managers</TableComponent>
        <Spacer height='3em'></Spacer>
      </Col>
    </Row>
      
  </Container>

  );
}
