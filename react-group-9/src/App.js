import React, { Component } from 'react'; // Importing React and Component from react
import { useState, useEffect} from 'react'; // Importing useState and useEffect hooks from react
import 'bootstrap/dist/css/bootstrap.min.css'; // Importing Bootstrap for styling
import { Row, Container, Col} from "reactstrap" // Importing specific components from reactstrap
import './App.css'; // Importing App-specific CSS
import { Route, Routes, } from 'react-router-dom'; // Importing Route and Routes for routing
import { Login } from './components/Login/login'; // Importing Login component
import { Register } from './components/Register/register'; // Importing Register component
import Home from './components/Home/home'; // Importing Home component
import Manager from './components/Home/manager'; // Importing Manager component
import Admin from './components/Home/admin'; // Importing Admin component
import Bouncer from './components/Home/bouncer'; // Importing Bouncer component
import Customer from './components/Home/customer'; // Importing Customer component
import User from './components/Home/user'; // Importing User component

export default function App(){
  return (
    // Defining Routes for the application
    <Routes>
        <Route path='/' element={<Login/>} />
        <Route path='/login' element={<Login/>} />
        <Route path='/signup' element={<Register/>} />
        <Route path='/manager' element={<Manager/>} />
        <Route path='/bouncer' element={<Bouncer/>} />
        <Route path='/admin' element={<Admin/>} />
        <Route path='/customer' element={<Customer/>} />
        <Route path='/user' element={<User/>} />
        <Route path='/home' element={<Home/>} />
    </Routes>
  )
}
