import React, { useState, useEffect } from 'react';
import { Button} from "reactstrap"

export default function DropdownComponent(props) {

  const text = props.text;
  const index = props.index;
  const [options, setOptions] = useState([]); // State to hold dropdown options

  useEffect(() => {
    fetchData();
  }, []);

  function fetchData() {
    fetch(props.url)
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
            setOptions(jsonOutput);
          }
    )
    .catch((error) => 
    {
        console.log(error);
        setOptions([]);
    })  
  }


  function handleDropdownChange(event) {
    event.preventDefault();
    const value = event.target.value;
    // console.log('here');
    // console.log(value);
    props.handler(value);
    
  }

  return (
    <div style={{height: '50px'}}>
      <label className="dropdown-label" ><strong> {text} </strong></label>
      <select onChange={handleDropdownChange} className="dropdown-bar">
        {props.default && <option value={props.default}>{props.default}</option>}
        {options.map((option, i) => (
          <option key={i} value={option[index]}>
            {option[index]}
          </option>
        ))}
      </select>

    </div>
  );
};


