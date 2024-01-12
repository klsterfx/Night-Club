import React, { useEffect, useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Form, FormGroup, Label, Input} from 'reactstrap';
import Dropdown from './DropDown';

export default function AddManagerButton(props) {
  const [modal, setModal] = useState(false);
  var [manager, SetManager]  = useState('');

  function handleSubmit(event) {
    // console.log(manager)
    event.preventDefault();
    const data = [props.club[0], manager];
    props.handler(data);
    
  }

  function handleDropDown(value) {
    // console.log(value)
    SetManager(value);
  }

//   useEffect(){

//   }


  const toggle = () => setModal(!modal);

  return (
    <div>
        <Button color={props.color} className="btn btn-primary btn-lg deleteButton" onClick={toggle} disabled={props.disable}>
        {props.children}
        </Button>
        <Modal isOpen={modal} toggle={toggle} >
            <ModalHeader toggle={toggle}> {props.title}</ModalHeader>
            <ModalBody>
                <Form onSubmit={handleSubmit}> 
                    <FormGroup>
                        {/* <Label for="userName"> User's Email</Label >
                        <Input id="useNamer" name="user" type="text"/> */}
                        <Dropdown url={props.url} index={props.index} default=' ' text='Select User' handler={handleDropDown}> 
                        </Dropdown>
                    </FormGroup>
                    <Button color="primary" type="submit" onClick={toggle}>
                        Add
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