import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button} from "reactstrap"

export default function DelManagerButton (props) {
  var classes= "btn btn-primary btn-lg deleteButton";

  function handleClick(event) {
    event.preventDefault()
    props.handler(props.club[0]);
  }
  
    return (
        <div>
            <Button color="danger" className={classes} onClick={handleClick}>
                {props.children}
            </Button>
        </div>


    );
  };
  