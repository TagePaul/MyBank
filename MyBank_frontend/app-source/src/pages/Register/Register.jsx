import React, { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";

import Input_v1 from "../../components/UI/Input/Input_v1";
import { registerDataIsValid } from '../../utils/registerTools'
import { AuthContext } from "../../context";

const Register = () => {
    const [submitResult, setSubmitResult] = useState(null)
    const {isAuth, setIsAuth} = useContext(AuthContext)
    const redirect = useNavigate()
    useEffect(() => {
        if (isAuth) {
            redirect('/lk')
        }
    })
    const inputContext = [
        {type: 'text', name: 'username', 
         required: true, placeholder: 'Логин'},
        {type: 'text', name: 'first_name', 
         required: true, placeholder: 'Имя'},
        {type: 'text', name: 'last_name', 
         required: true, placeholder: 'Фамилия'},
        {type: 'text', name: 'city', 
         required: true, placeholder: 'Город'},
        {type: 'email', name: 'email', 
         required: true, placeholder: 'email'},
        {type: 'text', name: 'phone_number', 
         required: true, placeholder: 'Номер телефона', 
         pattern: "[0-9]{11}"},
        {type: 'password', name: 'password', 
         required: true, placeholder: 'Пароль'},
        {type: 'password', name: 're_password', 
         required: true, placeholder: 'Повторите пароль'},
        {type: 'submit'},
    ]

    let inputs = inputContext.map((item, index) => 
        <Input_v1 key={index} {...item} />
        )  

    async function submitEvent(event) {
        event.preventDefault()
        let target = event.target
        await registerDataIsValid(target).then((result) => {
            setSubmitResult(result)
        })
    }
    return (
        <div className="AllContentBox__ContentWorkArea ContentWorkArea">
            <div className='ContentWorkArea__RegisterBox RegisterBox'>
                <div className="RegisterBox__title">
                    <p>Регистрация</p>
                </div>
                <div className="RegisterBox__alert">
                    {submitResult !== null
                    ? <p>{submitResult.description}</p>
                    : null}
                </div>
                <div className="RegisterBox__form">
                    <form onSubmit={submitEvent}>
                        {inputs}
                    </form>
                </div>
            </div>    
        </div>
    )
}

export default Register