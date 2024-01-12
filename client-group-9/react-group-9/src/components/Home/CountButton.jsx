import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button} from "reactstrap"

export default function CountButton (props) {
  var classes= "btn btn-primary btn-lg countButton";
  
    if (props.disable === true){
      return (
        <Button color={props.color} className={classes} onClick={props.handler} disabled>
          {props.children}
        </Button>
      )
    }
    return (
      <Button color={props.color} className={classes} onClick={props.handler}>
        <strong> {props.children} </strong>
      </Button>

    );
  };
  