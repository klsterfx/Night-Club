import React, { useState, useEffect } from 'react';
import './homeCSS.css';


export default function TableComponent (props) {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchData();
  }, [props.url]);

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
            setData(jsonOutput);
          }
    )
    .catch((error) => 
    {
        console.log(error);
        setData([]);
    })  
  }

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 1000);
    return () => clearInterval(interval);
    }, [props.url]);

  return (
    <div>
      <h2>{props.children}</h2>
      <table className="custom-table">
        <thead>
          <tr>
            <th>{props.coloumn1}</th>
            <th>{props.coloumn2}</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item,i) => (
            <tr key={i}>
              <td>{item[0]}</td>
              <td>{item[1]}</td>
              {/* Add more table cells based on your data */}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

