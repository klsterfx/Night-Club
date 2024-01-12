function validation(values){
    let error = {}
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+~\-\/\\=,.<>?]).{8,}$/;
    const email = values.email;
    const password = values.password;
    const name = values.name;
    const city = values.city;
    const age = values.age;

    if(email === ""){
        error.email = "Email cannot be empty!!!!"
    } else if(!emailRegex.test(email)){
        error.email = "Email didnt match the pattern!!!!"
    } else {
        error.email = ""
    }

    if(password === ""){
        error.password = "Password cannot be empty!!!!"
    }
    if(age === ""){
        error.age = "Age cannot be empty!!!!"
    }
    if(city === ""){
        error.city = "City cannot be empty!!!!"
    }

    if(name === ""){
        error.name = "Name cannot be empty!!!!"
    } else {
        error.name = ""
    }
    return error;
}

export default validation