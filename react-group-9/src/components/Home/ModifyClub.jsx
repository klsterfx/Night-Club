import React, { useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Form, FormGroup, Label, Input} from 'reactstrap';

export default function Modify(props) {
  const [modal, setModal] = useState(false);

  function handleSubmit(event) {
    event.preventDefault()
    const newClubInfo = [event.target.name.value, event.target.location.value, event.target.music.value, 
        parseInt(event.target.capacity.value), parseInt(event.target.yellow.value), props.club[5], false, false];
    props.handler(props.club, newClubInfo);
    
  }

  const toggle = () => setModal(!modal);

  return (
    <div>
        <Button color="primary" className="btn btn-primary btn-lg" onClick={toggle}>
        Modify
        </Button>
        <Modal isOpen={modal} toggle={toggle} >
            <ModalHeader toggle={toggle}> Modify Club Information</ModalHeader>
            <ModalBody>
                <Form onSubmit={handleSubmit}> 
                    <FormGroup>
                        <Label for="clubName"> Name</Label >
                        <Input id="clubName" name="name" defaultValue={props.club[0]} type="text"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubLocation"> Location</Label>
                        <Input id="clubLocation" name="location" defaultValue={props.club[1]} type="text"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubMusic"> Music Genre </Label>
                        <Input id="clubMusic" name="music" defaultValue={props.club[2]} type="text"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubCapacity"> Capacity</Label >
                        <Input id="clubCapacity" name="capacity" defaultValue={props.club[3]} type="number"/>
                    </FormGroup>
                    <FormGroup>
                        <Label for="clubYellow"> Yellow Threshold</Label>
                        <Input id="clubYellow" name="yellow" defaultValue={props.club[4]} type="number"/>
                    </FormGroup>
                    <Button color="primary" type="submit" onClick={toggle}>
                        Modify
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

