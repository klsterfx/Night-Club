import React, { useEffect, useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Form, FormGroup, Label, Input} from 'reactstrap';
import Dropdown from './DropDown';

export default function DelBouncerButton(props) {
  const [modal, setModal] = useState(false);
  var [bouncer, SetBouncer]  = useState('');
  

  function handleSubmit(event) {
    event.preventDefault();
    const data = [props.club[0], bouncer];
    // console.log(data)
    props.handler(data);
    
  }

  function handleDropDown(value) {
    // console.log(value)
    SetBouncer(value);
  }

//   useEffect(){

//   }


  const toggle = () => setModal(!modal);

  return (
    <div>
        <Button color={props.color} className="btn btn-primary btn-lg deleteButton" onClick={toggle}>
        {props.children}
        </Button>
        <Modal isOpen={modal} toggle={toggle} >
            <ModalHeader toggle={toggle}> Add Club</ModalHeader>
            <ModalBody>
                <Form onSubmit={handleSubmit}> 
                    <FormGroup>
                        {/* <Label for="userName"> User's Email</Label >
                        <Input id="useNamer" name="user" type="text"/> */}
                        <Dropdown url={props.url} index={1} default=' ' text='Select User' handler={handleDropDown}> 
                        </Dropdown>
                    </FormGroup>
                    <Button color="danger" type="submit" onClick={toggle}>
                        Delete
                    </Button>{' '}
                    <Button color="secondary" onClick={toggle}>
                        Cancel
                    </Button>
                </Form>
            </ModalBody>
            <ModalFooter>
            </ModalFooter>
        </Modal>
    </div>
  );
}