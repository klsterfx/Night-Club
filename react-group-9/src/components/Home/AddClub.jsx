import React, { useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Form, FormGroup, Label, Input} from 'reactstrap';

export default function AddButton(props) {
  const [modal, setModal] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();
    const newClubInfo = [event.target.name.value, event.target.location.value, event.target.music.value, 
        parseInt(event.target.capacity.value), parseInt(event.target.yellow.value), parseInt(event.target.current.value), false, false];
    props.handler(newClubInfo);
    
  }

  const toggle = () => setModal(!modal);

  return (
    <div>
        <Button color="info" className="btn btn-primary btn-lg" onClick={toggle}>
        Add Club
        </Button>
        <Modal isOpen={modal} toggle={toggle} >
            <ModalHeader toggle={toggle}> Add Club</ModalHeader>
            <ModalBody>
                <Form onSubmit={handleSubmit}> 
                    <FormGroup>
                        <Label for="clubName"> Name</Label >
                        <Input id="clubName" name="name" type="text"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubLocation"> Location</Label>
                        <Input id="clubLocation" name="location" type="select">
                          <option> ROC </option>
                          <option> NYC </option>
                          <option> NJ </option>
                          <option> PENN</option>
                        </Input>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubMusic"> Music Genre </Label>
                        <Input id="clubMusic" name="music" type="select">
                          <option> pop </option>
                          <option> rock </option>
                          <option> metal </option>
                        </Input>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubCapacity"> Capacity</Label >
                        <Input id="clubCapacity" name="capacity" defaultValue='100' type="number"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubYellow"> Yellow Threshold</Label>
                        <Input id="clubYellow" name="yellow" defaultValue='70'type="number"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubCurrent"> Current Count</Label>
                        <Input id="clubCurrent" name="current" defaultValue='0' type="number"/>
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