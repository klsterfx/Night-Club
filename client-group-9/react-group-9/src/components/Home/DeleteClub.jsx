import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button} from "reactstrap"

export default function DeleteButton (props) {
  var classes= "btn btn-primary btn-lg deleteButton";

  function handleClick(event) {
    event.preventDefault()
    props.handler(props.club);
  }
  
    return (
      <Button color={props.color} className={classes} onClick={handleClick}>
        {props.children}
      </Button>

    );
  };
  