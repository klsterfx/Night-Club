import React, { useEffect, useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Form, FormGroup, Label, Input} from 'reactstrap';
import Dropdown from './DropDown';

export default function RemoveCustomerButton(props) {
  const [modal, setModal] = useState(false);
  var [manager, SetManager]  = useState('');

  function handleSubmit(event) {
    event.preventDefault();
    const data = [props.club[0], manager, event.target.amount.value];
    props.handler(data);
    
  }

  function handleDropDown(value) {
    SetManager(value);
  }


  const toggle = () => setModal(!modal);

  return (
    <div>
        <Button color={props.color} className="btn btn-primary btn-lg deleteButton" onClick={toggle} disabled={props.disable}>
        {props.children}
        </Button>
        <Modal isOpen={modal} toggle={toggle} >
            <ModalHeader toggle={toggle}> Remove Customer</ModalHeader>
            <ModalBody>
                <Form onSubmit={handleSubmit}> 
                    <FormGroup>

                        { props.userselection && <Dropdown url={props.url} index={0} default=' ' text='Select User' handler={handleDropDown}> 
                        </Dropdown>}
                        <Label for="amount"> Bill Amount ($)</Label >
                        <Input id="amount" name="amount" type="number" step="any"/>
                    </FormGroup>
                    <Button color="danger" type="submit" onClick={toggle}>
                        Confirm
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