import React, { useEffect, useState } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';
import { Form, FormGroup, Label, Input} from 'reactstrap';
import Dropdown from './DropDown';

export default function ReseervationButton(props) {
  const [modal, setModal] = useState(false);

  const [formData, setFormData] = useState({
    date: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Timestamp:', formData.date);
    const data = [props.club[0], formData.date];
    props.handler(data);

  };


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

                        {/* <Label for="amount"> Bill Amount ($)</Label >
                        <Input id="amount" name="amount" type="number" step="any"/> */}

                      <label>
                                Timestamp:
                                <input
                                  type="date"
                                  name="date"
                                  value={formData.date}
                                  onChange={handleChange}
                                />
                      </label>
                        
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