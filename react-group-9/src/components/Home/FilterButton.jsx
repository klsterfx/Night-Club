import React, { useState } from 'react';
import Dropdown from './DropDown';

export default function FilterButton(props) {

const index = props.index;

function handleSubmit(value) {

    // event.preventDefault();
    // const location = event.target.location.value;
    // console.log(value)
    props.handler(value);
    
  }


return (
    <div>
            <Dropdown url='http://localhost:5000/clubs/filter' index={index} default='All' text='Select Location' handler={handleSubmit}> 
            </Dropdown>
    </div>
  );
}
