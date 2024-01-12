import React, { useState } from 'react'
import { Link } from "react-router-dom";
import validation from "../Utilities/formValidation";
import { useEffect } from 'react';


export function Register() {
    const [values, setValues] = useState({
        email: '',
        name: '',
        password: '',
        age: '', 
        city: ''
    })

    const [errors, setErrors] = useState({'email':" ", 'name':" ", "age":" ", 'password':" " , 'city':" "})

    const handleInput = (event) => {
        setValues(prev => ({
            ...prev, [event.target.name]: event.target.value
        }))
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        setErrors(validation(values));
    }

    useEffect(() => {
        if (errors.city != 'Account is created successfully'){
            if (!errors.email && !errors.name && !errors.age && !errors.password && !errors.city){
                AddUser(values)
            }
        }
        
    }, [errors], values );


    function AddUser(user_info) {
        fetch('http://localhost:5000/users', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(user_info)
        })
        .then(res => res.json())
        .then((data) => {
            setErrors({'city': data})
        })
        .catch(err => console.log(err));
    }

    return (
        <div className="d-flex justify-content-center align-items-center bg-light vh-100">
            <div className="bg-white p-3 rounded w-25">
                <div>
                    <h2> Sign Up </h2>
                </div>
                <form action="" onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="email"><strong>Email ID*</strong></label>
                        <input type="email" className="form-control rounded-1" 
                        onChange={handleInput} placeholder="youremail@emailID.com" id="email" name="email"/>
                        {errors.email && <span className="text-danger"> {errors.email} </span>}
                    </div>
                    <div className="mb-3">
                        <label htmlFor="name"><strong>Name*</strong></label>
                        <input type="text" className="form-control rounded-1" 
                        onChange={handleInput} placeholder="Enter Name" id="name" name="name"/>
                        {errors.name && <span className="text-danger"> {errors.name} </span>}
                    </div>
                    <div className="mb-3">
                        <label htmlFor="password"><strong>Password*</strong></label>
                        <input type="password" className="form-control rounded-1" 
                        onChange={handleInput} placeholder="********" id="password" name="password"/>
                        {errors.password && <span className="text-danger"> {errors.password} </span>}
                    </div>
                    <div className="mb-3">
                        <label><strong>Age*</strong></label>
                        <input type="number" className="form-control rounded-1" 
                        onChange={handleInput} placeholder="Enter Age" id="age" name="age"/>
                        {errors.age && <span className="text-danger"> {errors.age} </span>}
                    </div>
                    <div className="mb-3">
                        <label><strong>City*</strong></label>
                        <input type="text" className="form-control rounded-1" 
                        onChange={handleInput} placeholder="Enter City" id="city" name="city"/>
                        {errors.city && <span className="text-danger"> {errors.city} </span>}
                    </div>
                    <div className="grid gap-3">
                        <div className="p-2 g-col-6">
                            <button type='submit' className="btn btn-success w-100"> <strong> Sign Up </strong></button>
                        </div>
                        <div className="p-2 g-col-6">
                            <Link to="/login" className="btn btn-default border w-100 bg-light"><strong> Login </strong></Link>
                        </div>
                    </div>
                </form>
            </div>
        </div>
      );
  }