import React, { useContext, useState, useEffect } from "react";
import Input_v1 from "../../components/UI/Input/Input_v1";
import { login } from "../../utils/authTools";
import { AuthContext } from "../../context";
import { useNavigate } from "react-router-dom";

const Login = () => {
    const {isAuth, setIsAuth} = useContext(AuthContext)
    const [isAlert, setIsAlert] = useState(null)
    const redirect = useNavigate()
    const inputContext = [
        {type: 'text', name: 'username', required: true, placeholder: 'Логин'},
        {type: 'password', name: 'password', required: true, placeholder: 'Пароль'},
        {type: 'submit'}
    ]
    let inputs = inputContext.map((item, index) => 
        <Input_v1 key={index} {...item}/>
        )

    useEffect(() => {
        if (isAuth) {
            redirect('/lk')
        }
    })

    async function submitEvent(event) {
        event.preventDefault()
        let target = event.target
        await login(target).then((result) => {
            if (result) {
                setIsAuth(true)
            } else {
                setIsAuth(false)
                setIsAlert(false)
            }
        })
    }
    console.log('ren')

    return (
        <div className="AllContentBox__ContentWorkArea ContentWorkArea">
            <div className="ContentWorkArea__LoginBox LoginBox">
                <div className="LoginBox__title">
                    <p>Авторизация</p>
                </div>
                <div className="LoginBox__Alert">
                    {isAlert == false
                    ? <p>Ошибка авторизации</p>
                    : null}
                </div>
                <div className="LoginBox__form">
                    <form onSubmit={submitEvent}>
                        {inputs}
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Login
