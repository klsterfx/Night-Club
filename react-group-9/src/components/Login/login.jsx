import React,{Component,useState} from "react";
import { useEffect } from 'react';
import { Link } from "react-router-dom";
import "./loginCss.css";
import validation from "../Utilities/formValidation";
import { useNavigate } from "react-router-dom";
import Sidebar from "../NavBar/Sidebar";


export function Login() {

        const navigate = useNavigate();

        const [values, setValues] = useState({
            email: '',
            password: ''
        })

        const [session, setSession] = useState({
            ID: '',
            role: ''
        })
        
        const [errors, setErrors] = useState({})

        const handleInput = (event) => {
            setValues(prev => ({
                ...prev, [event.target.name]: event.target.value
            }))
        }

        const handleSubmit = (event) => {
            event.preventDefault();
            setErrors(validation(values));
            LoginCheck(values);
        }
        // {'email':event.target.email.value, 'password':event.target.password.value}

        function LoginCheck(login_info) {
            
            fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(login_info)
            })
            .then(res => res.json())
            .then((data) => {
                if (data==='email or password is incorrect'){
                    setErrors({'login': data})
                }
                else{
                    setSession({'ID': data[0], 'role': data[1]});
                }
            })
            .catch(err => console.log(err));
        }

        useEffect(() => {
                if (session.role === 'admin') { navigate("/admin" , { state: { email: values.email, ID:session.ID}});}
                else if (session.role === 'manager') {navigate("/manager", {state: { email: values.email, ID:session.ID}});}
                else if (session.role === 'bouncer') {navigate("/bouncer",{state: { email: values.email, ID:session.ID}});}
                else if (session.role === 'customer') {navigate("/customer",{state: { email: values.email, ID:session.ID}});}
                else if (session.role === 'user') {navigate("/user",{state: { email: values.email, ID:session.ID}});}

            }, [session] );
        
        return(
            <div>
            <Sidebar/>
                <div className="d-flex justify-content-center align-items-center bg-light vh-100">
                    <div className="bg-white p-3 rounded w-25">
                    <div>
                        <h2> Sign In </h2>
                    </div>
                        <form action="" onSubmit={handleSubmit}>
                            <div className="mb-3">
                                <label htmlFor="email"><strong>Email ID</strong></label>
                                <input type="email" className="form-control rounded-1" 
                                    onChange={handleInput} placeholder="youremail@emailID.com" 
                                    id="email" name="email"/>
                                {errors.email && <span className="text-danger"> {errors.email} </span>}
                            </div>
                            <div className="mb-3">
                                <label><strong>Password</strong></label>
                                <input type="password" className="form-control rounded-1" 
                                    onChange={handleInput} placeholder="********" id="password" name="password"/>
                                    {errors.login && <span className="text-danger"> {errors.login} </span>}
                            </div>
                            <div className="grid gap-3">
                                <div className="p-2 g-col-6">
                                    <button type="submit" className="btn btn-success w-100"> <strong> Log In </strong></button>
                                </div>
                                <div className="p-2 g-col-6">
                                    <Link to="/signup" className="btn btn-default border w-100 bg-light"><strong> Create Account </strong></Link>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
}